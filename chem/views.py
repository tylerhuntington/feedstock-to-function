from django.db.models import Q
from numpy import inf
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from collections import defaultdict
import re
import json
from urllib.parse import urlencode
from rdkit.Chem import MolToSmiles, MolFromSmiles
from rdkit.Chem.Draw import MolToFile
from django.urls import reverse
from django.shortcuts import render
import requests
from fuzzywuzzy import process
import csv
import copy
from django.contrib import messages
from django.shortcuts import render
from chem.serializers import ChemicalSerializer
from chem import (
    PRED_PROP_CODES,
    MIN_FUZZY_SEARCH_SCORE,
    MAX_FUZZY_SEARCH_RESULTS,
    FUZZY_SEARCH_SCORER,
    CHEM_STRUCT_IMG_DIR,
    ESTIMATORS_JOBLIB_DIR,
    DESCRIPTORS_DIR,
)

from chem.models import Chemical, ChemicalSynonym, PropertyEstimator
from chem.forms import (
    ChemicalSearchForm, ChemicalSubmissionForm, BlendSubmissionForm
)
from chem import CHEM_SUBMISSION_TEMPLATE, BLEND_SUBMISSION_TEMPLATE
from django.views.generic import (
    View, FormView, ListView, TemplateView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import FileResponse, Http404, HttpResponseNotFound, \
    HttpResponse, \
    JsonResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from fuzzywuzzy import process
from chem.serializers import ChemicalSerializer
import pandas as pd
from django.shortcuts import redirect
from django.urls import reverse_lazy
from mordred import Calculator, descriptors
from rdkit.Chem import MolFromSmiles, MolToSmiles
from pathlib import Path
import regex as re
import logging

from chem.utils import pred_props_and_errs_of_smiles, kelvin_to_celsius

# config logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(name)s] %(message)s', datefmt='%m-%d %H:%M'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class DownloadChemCSVToClient(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):

        chem = Chemical.objects.get(pk=pk)
        dict = ChemicalSerializer(chem).data
        df = pd.DataFrame.from_dict(dict, orient='index').T
        csv = pd.DataFrame.to_csv(df, index=False)
        try:
            # with open(fpath, 'rb') as f:
            #     file_data = f.read()
            response = HttpResponse(
                csv, content_type='application/octet-stream'
            )
            response['Content-Disposition'] = \
                f'attachment; filename = "chemical_pk_{pk}.csv"'

        except IOError:
            # handle case where file does not exist
            response = HttpResponseNotFound(
                f'<h2>File does not exist</h2>'
            )

        return response


class DownloadChemSubmissionTemplate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            # with open(fpath, 'rb') as f:
            #     file_data = f.read()
            print('template')
            print(CHEM_SUBMISSION_TEMPLATE)
            response = HttpResponse(
                CHEM_SUBMISSION_TEMPLATE,
                content_type='application/octet-stream'
            )
            # response = FileResponse(
            #     CHEM_SUBMISSION_TEMPLATE,
            #     content_type='application/octet-stream'
            # )
            response['Content-Disposition'] = \
                f'attachment; filename = "chemical_submission_template.csv"'
        except IOError:
            # handle case where file does not exist
            response = HttpResponseNotFound(
                f'<h2>File does not exist</h2>'
            )
        return response


class DownloadBlendSubmissionTemplate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            response = HttpResponse(
                BLEND_SUBMISSION_TEMPLATE,
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = \
                f'attachment; filename = "blend_submission_template.csv"'
        except IOError:
            # handle case where file does not exist
            response = HttpResponseNotFound(
                f'<h2>File does not exist</h2>'
            )
        return response


class ChemicalDetail(LoginRequiredMixin, FormMixin, DetailView):
    model = Chemical
    form_class = ChemicalSearchForm
    template_name = 'chemical_detail.html'
    context_object_name = 'chem'

    @staticmethod
    def check_for_jmol_struct(smiles):
        jmol_base_url = "https://chemapps.stolaf.edu/jmol/jmol.php?model="
        # smiles = 'Cc1c([N+](=O)[O-])c(C)c([N+](=O)[O-])c(C(C)(C)C)c1[N+](=O)[O-]'
        req_url = f'{jmol_base_url}{smiles}'
        rv = requests.get(req_url)
        cont = str(rv.content)
        nih_err_substr = 'ERROR opening'
        jmol_err_substr = """
            The proxy server could not handle the request GET /jmol/jmol.php
        """
        if nih_err_substr in cont or jmol_err_substr in cont:
            return False
        return True

    def get_context_data(self, **kwargs):
        context = super(ChemicalDetail, self).get_context_data(**kwargs)
        context['form'] = self.form_class(
            initial={
                'search_type': self.kwargs.get('search_type'),
                'search_term': self.kwargs.get('search_term'),
            }
        )
        smiles = context['object'].smiles
        jmol_struct = ChemicalDetail.check_for_jmol_struct(smiles=smiles)
        if not jmol_struct:
            fn = f'struct_smiles_{smiles}.png'
            fp = Path(CHEM_STRUCT_IMG_DIR, fn)
            mol = MolFromSmiles(smiles)
            try:
                MolToFile(mol, fp)
            except (ValueError, IOError) as e:
                print('rdkit cant make image', e)
            context['struct_img'] = fn

        context['jmol_struct'] = jmol_struct
        return context

    def dispatch(self, *args, **kwargs):
        qdict = self.request.GET.dict()
        if 'search_type' in qdict and 'search_term' in qdict:
            qs = f'?{urlencode(qdict)}'
            return redirect(reverse('chem:search') + qs)
        return super(ChemicalDetail, self).dispatch(*args, **kwargs)


class ChemicalSearchResultsAJAXView(View):
    context_object_name = 'results'
    results_template_name = 'chemical_list.html'
    detail_template_name = 'chemical_detail_standalone.html'

    # TODO: split out a JSON view for retuning the JSON and other two for HTML
    def get(self, request, *args, **kwargs):
        params = {k: v[0] for k, v in dict(request.GET).items()}
        search_type = params['searchType']
        search_term = params['searchTerm']
        if search_type == 'smiles':
            rv = self.search_by_smiles(request, search_term)
        else:
            rv = self.search_non_smiles(request, params)
        return JsonResponse(rv)

    def search_non_smiles(self, request, params, *args, **kwargs):
        search_type = params['searchType']
        search_term = params['searchTerm']

        # First, get all search results for the provided search type and term.
        results = self.search_by_id(search_type, search_term)

        # Parse the search filters.
        filters = self._parse_property_filters(params)

        # Apply the search filters to the original results set.
        filtered_res = self._filter_results(results, filters)

        # Get the properties for which filters were used in the search
        filter_props = [k for k, v in filters.items()]

        context = {
            self.context_object_name: filtered_res,
            'search_type': search_type,
            'search_term': search_term,
            'filter_props': filter_props
        }
        res = render(request, self.results_template_name, context=context)
        html = res.content.decode('utf-8')
        return {'html': html}

    def _parse_property_filters(self, params):
        filters = defaultdict(dict)
        for k, v in params.items():
            # TODO: handle these checks using form validation in React
            if v != 'null':
                if k.endswith('Min'):
                    prop = f"{k.replace('Min', '')}"
                    filters[prop]['min'] = float(v)
                elif k.endswith('Max'):
                    prop = f"{k.replace('Max', '')}"
                    filters[prop]['max'] = float(v)
                elif k.endswith('AllowPreds'):
                    prop = f"{k.replace('AllowPreds', '')}"
                    if v == 'true':
                        filters[prop]['allow_preds'] = True
                    else:
                        filters[prop]['allow_preds'] = False
        return filters

    def _filter_results(self, results, filters, return_all_syns=False):
        filtered_results = []
        # Iterate over un-filtered Chemical results
        for r in results:
            # Get the Chemical object in case `r` is a ChemicalSynonym
            c = r.chem if isinstance(r, ChemicalSynonym) else r

            # Initialize flag for whether to keep a result (True) or filter it
            # out (False) based on property filters passed by caller.
            keep_result = True

            # Iterate over property filters and apply to current Chemical
            for prop, crit in filters.items():
                allow_preds = False
                if 'allow_preds' in crit:
                    allow_preds = crit['allow_preds']
                sfxs = ['exp', 'pred'] if allow_preds else ['exp']
                if 'min' in crit or 'max' in crit:
                    min_val = crit['min']
                    max_val = crit['max']
                    # If a Chemical does not meet the min/max criteria of a
                    # filter, `keep_result` will be set to False here.
                    keep_result = self._apply_min_max_filter(
                        c,
                        prop=prop,
                        min_val=min_val,
                        max_val=max_val,
                        sfxs=sfxs
                    )
                    # If keep_result is set to False, we know immediately
                    # this Chemical can be "filtered out"
                    # (i.e. not included in the filtered result set) so we break
                    # out of the inner for-loop to bypass unnecessary checks
                    # agains other filters.
                    if not keep_result:
                        break
            # If keep_results is never set to False, we know the Chemical passed
            # all the filter criteria and thus should be included in the
            # filtered result set so we append it.
            if keep_result:
                filtered_results.append(r)
            if return_all_syns:
                for syn in c.synonyms.all():
                    if syn.name != 'nan':
                        filtered_results.append(syn)

        return filtered_results

    def _apply_min_max_filter(
            self, obj, prop, sfxs, min_val=-inf, max_val=inf
        ):
        """
        Returns True if the passed `obj` meets filter criteria
        (i.e. should be included) from result set based on whether its value
        is between `min_val` and `max_val` (inclusive).
        """

        # Always prioritize experimental values when applying the filter if
        # present for a chemical.
        if 'exp' in sfxs:
            prop_str = f'{prop}_exp'
            if getattr(obj, prop_str):
                if getattr(obj, prop_str) >= min_val:
                    if getattr(obj, prop_str) <= max_val:
                        return True
        if 'pred' in sfxs:
            prop_str = f'{prop}_pred'
            if getattr(obj, prop_str):
                if getattr(obj, prop_str) >= min_val:
                    if getattr(obj, prop_str) <= max_val:
                        return True
        return False

    def search_by_smiles(self, request, search_term):
        """
        Searches Chemical objects by SMILES string.
        """
        # Standardize the SMILES string.
        search_term = MolToSmiles(MolFromSmiles(search_term))

        # Perform the search.
        chems = self.query_by_smiles(search_term)

        # Check that at least one result was found.
        if len(chems) == 1:
            chem = chems[0]
            return {'chem_pk': chem.pk}

        # If no results, perform dummy search by name to get the HTML template
        # for a "No results..." message in the results section.
        else:
            params = {
                'searchType': 'name',
                'searchTerm': 'abcdefghijklmnopqrztuvwxyx'
            }
            return self.search_non_smiles(request, params)

    def search_by_id(self, search_type, search_term):
        """
        Searches Chemical objects by a non-SMILES identifier (molecular name,
        IUPAC Name, chemical formula, or INCHI code).

        TODO: use artificial primary keys for Chemical objects
        https://en.wikipedia.org/wiki/International_Chemical_Identifier
        """
        # Only perform the search if a non-empty string was provided as the
        # search term.
        if search_term:
            if search_type == 'name':
                return self.query_by_name(search_term)
            elif search_type == 'iupac':
                return self.query_by_iupac(search_term)
            elif search_type == 'formula':
                return self.query_by_formula(search_term)
            elif search_type == 'inchi':
                return self.query_by_inchi(search_term)
            elif search_type == 'all':
                # TODO: optimize the 'Search All Molecules' which currently gets
                #  all Chemical objects and then applies search filters.
                #  This is a very slow O(n) operation (where n is the number
                #  of Chemical records in the database) which will not scale
                #  well with the addition of many more Chemicals to the DB.
                return Chemical.objects.all()
        # Return an empty list (i.e. no results) if no search term provided.
        else:
            return []

    def query_by_inchi(self, term):
        """
        Queries Chemical objects by INCHI code.
        """

        # First try searching chemicals by molecular name field
        chems = Chemical.objects.filter(
            inchi__iexact=term
        )
        # if no iexact matches for search term, try fuzzy search
        if len(chems) == 0:
            chems = Chemical.objects.filter(
                inchi__icontains=term,
            )
            # handle case where there are no fuzzy search results
            if len(chems) == 0:
                return []
            inchis = [chem.inchi for chem in chems]

            # Get best fuzzy search results as list of tuples of the form:
            # ({IUPAC}, {SCORE})
            # TODO: look into postgres' full text search functionality as an
            #   alternative to fuzzywuzzy
            best = process.extract(
                term,
                inchis,
                limit=20,
                scorer=FUZZY_SEARCH_SCORER
            )
            # check for max fuzzy match score
            max_score = max([m[1] for m in best])
            if max_score > MIN_FUZZY_SEARCH_SCORE:
                res = [Chemical.objects.get(inchi__iexact=s[0]) for s in best]
                return [x for x in res if x != 'nan']
        return chems

    def query_by_formula(self, term):
        """
        Queries Chemical objects by chemical formula.
        """
        # first try searching chemicals by molecular name field
        chems = Chemical.objects.filter(
            formula__iexact=term
        )
        # if no iexact matches for search term, try fuzzy search
        if len(chems) == 0:
            chems = Chemical.objects.filter(
                formula__icontains=term,
            )
            # handle case where there are no fuzzy search results
            if len(chems) == 0:
                return []
            formulas = [chem.formula for chem in chems]
            # get best fuzzy search results as list of tuples of the form:
            # ({IUPAC}, {SCORE})
            best = process.extract(
                term,
                formulas,
                limit=20,
                scorer=FUZZY_SEARCH_SCORER
            )
            # check for max fuzzy match score
            max_score = max([m[1] for m in best])
            if max_score > MIN_FUZZY_SEARCH_SCORE:
                res = []
                for s in best:
                    for c in Chemical.objects.filter(formula__iexact=s[0]):
                        res.append(c)
                return [x for x in res if x != 'nan']
        return chems

    def query_by_iupac(self, iupac):
        """
        Queries Chemical objects by IUPAC name.
        """
        # first try searching chemicals by molecular name field
        chems = Chemical.objects.filter(
            iupac__iexact=iupac
        )
        # if no iexact matches for search term, try fuzzy search
        if len(chems) == 0:
            # TODO: implement this for other search types
            #  https://docs.djangoproject.com/en/4.0/ref/models/querysets/#q-objects
            #  https://docs.djangoproject.com/en/4.0/topics/db/queries/#complex-lookups-with-q

            # q = Q(bp_exp__range=[0,100])|Q(bp_exp__isnull=True, bp_pred__range=[0,100])
            # chems = Chemical.objects.filter(
            #     q, iupac__icontains=iupac
            # )
            # handle case where there are no fuzzy search results
            if len(chems) == 0:
                return []
            iupacs = [chem.iupac for chem in chems]
            # get best fuzzy search results as list of tuples of the form:
            # ({IUPAC}, {SCORE})
            best = process.extract(
                iupac,
                iupacs,
                limit=20,
                scorer=FUZZY_SEARCH_SCORER
            )
            # check for max fuzzy match score
            max_score = max([m[1] for m in best])
            if max_score > MIN_FUZZY_SEARCH_SCORE:
                res = [Chemical.objects.get(iupac__iexact=s[0]) for s in best]
                return [x for x in res if x != 'nan']
        return chems

    def query_by_name(self, name=''):
        """
        Queries Chemical objects by molecular name.
        """
        # first try searching chemicals by molecular name field
        chems = Chemical.objects.filter(
            name__iexact=name
        )
        # handle case where there are one or more iexact name matches
        if len(chems) >= 1:
            # get related chem for synonym matches and return as result set
            return [c for c in chems if c.name != 'nan']

        # handle case where there are no iexact molecular name matches
        # in this case, we look up synonyms for the search term and return
        # those as the result set
        return self.query_by_name_via_synonyms(name)

    def query_by_name_via_synonyms(self, name):
        # Init accumulator of unique Chemical objects to return
        chems = []
        # find synonymns that are case-insensitive exact match the search term
        syns = ChemicalSynonym.objects.filter(
            name__icontains=name,
        )
        # filter out chems with 'nan' names (i.e. no molecular name on record)
        syns = [s for s in syns if s.name != 'nan']
        # determine best subset of fuzzy search results to return
        syn_names_dict = {syn.name: syn for syn in syns}
        syn_names = [syn.name for syn in syns]
        best = process.extract(
            name,
            syn_names,
            limit=MAX_FUZZY_SEARCH_RESULTS,
            scorer=FUZZY_SEARCH_SCORER
        )
        # check for max fuzzy match score
        max_score = max([m[1] for m in best]) if best else 0
        syns = []
        if max_score > MIN_FUZZY_SEARCH_SCORE:
            syns = [syn_names_dict[s[0]] for s in best]
        for s in syns:
            if s.chem not in chems:
                chems.append(s.chem)
        return chems

    def query_pubchem_by_name(self, name):
        return self.make_chem_from_pubchem_api_query(name=name)

    def query_pubchem_by_smiles(self, smiles):
        return self.make_chem_from_pubchem_api_query(smiles=smiles)

    def query_by_smiles(self, smiles):

        # TODO: handle case insensitivity for SMILES strings
        chems = Chemical.objects.filter(
            smiles__iexact=smiles
        )

        # Handle case of no results in QuerySet
        if len(chems) == 0:
            chems = self.make_new_chems_from_smiles([smiles])

        # Make sure no more than one chemical is returned for the query SMILES
        if len(chems) > 1:
            e = (
                f"""
            {len(chems)} case-insensitive SMILES matches for: {smiles}.
            Returning chemical with case-matching SMILES.
            """
            )
            logger.info(e)
            chems = Chemical.objects.filter(
                smiles=smiles
            )

        return chems

    def make_new_chems_from_smiles(self, smiles_list):
        """

        :param smiles: list of smiles strings for which Chemical instances
            should be created
        :return:
        """
        new_chems = []
        try:
            res = pred_props_and_errs_of_smiles(
                smiles_list,
                path_to_descr=f'{str(DESCRIPTORS_DIR)}/',
                path_to_mods=f'{str(ESTIMATORS_JOBLIB_DIR)}/',
            )

            for smiles, pred_props_errs in res.items():
                new_chem = Chemical()
                new_chem.smiles = smiles
                new_chem.bp_pred = kelvin_to_celsius(
                    pred_props_errs['bp_k_pred']
                )
                new_chem.bp_pred_err_up = kelvin_to_celsius(
                    pred_props_errs['bp_k_upper']
                )
                new_chem.bp_pred_err_low = kelvin_to_celsius(
                    pred_props_errs['bp_k_lower']
                )
                new_chem.fp_pred = kelvin_to_celsius(
                    pred_props_errs['fp_k_pred']
                )
                new_chem.fp_pred_err_up = kelvin_to_celsius(
                    pred_props_errs['fp_k_upper']
                )
                new_chem.fp_pred_err_low = kelvin_to_celsius(
                    pred_props_errs['fp_k_lower']
                )
                new_chem.mp_pred = kelvin_to_celsius(
                    pred_props_errs['mp_k_pred']
                )
                new_chem.mp_pred_err_up = kelvin_to_celsius(
                    pred_props_errs['mp_k_upper']
                )
                new_chem.mp_pred_err_low = kelvin_to_celsius(
                    pred_props_errs['mp_k_lower']
                )
                new_chem.hoc_pred = pred_props_errs['hoc_pred']
                new_chem.hoc_pred_err_up = pred_props_errs['hoc_upper']
                new_chem.hoc_pred_err_low = pred_props_errs['hoc_lower']
                new_chem.ysi_pred = pred_props_errs['ysi_pred']
                new_chem.ysi_pred_err_up = pred_props_errs['ysi_upper']
                new_chem.ysi_pred_err_low = pred_props_errs['ysi_lower']
                new_chem.save()
                new_chems.append(new_chem)


        except Exception as e:
            print(e)

        return new_chems

    def get_pubchem_cmpd_by_smiles(self, smiles):
        """if our names database does not contain this molecule's info,
        try getting it from pubchem API"""
        chem_data = {'smiles': smiles}
        noAPIresults = False
        try:  # add a try/except in case pubchem server failure
            data = requests.get(
                f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'
                f'smiles/{smiles}/property/MolecularFormula,'
                f'IUPACName,InChIKey/JSON'
            )
            data = data.json()
        except BaseException as e:
            print('pubchem not responsive', e)
            pass

        try:  # to deal with CCC12 type examples where pubchem has multiple hits
            data = data['PropertyTable']['Properties'][0]
            cid = data['CID']

            name = requests.get(
                f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data'
                f'/compound/{cid}/JSON'
            )
            name = name.json()

            chem_data["formula"] = data['MolecularFormula']
            chem_data["inchi"] = data['InChIKey']
            chem_data["iupac"] = data['IUPACName']
            chem_data["pubchem_cid"] = data['CID']

        except KeyError as e:
            print('not in pubchem', e)
            pass

        try:  # molecule names come in two different forms in the pubchem api
            chem_data["name"] = name['Record']['Reference'][0]['Name']
        except (NameError, KeyError) as e:
            print('couldnt get pubchem name', e)
            try:
                chem_data["name"] = name['Record']['RecordTitle']
            except (NameError, KeyError) as e:
                print('couldnt get pubchem name', e)

        # get synonyms
        syns = []
        try:  # add a try/except in case pubchem server failure
            synonyms = requests.get(
                f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
                f"compound/smiles/{smiles}/synonyms/JSON"
            )
            synonyms = synonyms.json()
            syns = synonyms['InformationList']['Information'][0]['Synonym']
            matches = process.extract(chem_data['name'], syns, limit=7)
            manual_syns = [chem_data['name'], chem_data['iupac']]
            syns = list(set(manual_syns + [m[0] for m in matches]))
            syns = [s for s in syns if s != 'nan']

        except BaseException as e:
            print('pubchem synonyms not responsive', e)
            pass

        # if the api didn't fill in the formula then there were no results
        if 'formula' not in chem_data:
            print(f'No results from pubchem API for smiles: {smiles}')
        # if we get here,
        # the api hit was successful store this new entry in our database

        return (chem_data, syns)

    def make_chem_from_pubchem_api_query(self, name=None, smiles=None):
        """

        :param name:
        :param smiles:
        :return: [] if unable to get a valid compound from pubchem
        """
        if name is not None:
            try:
                chem_data, syns = self.get_pubchem_cmpd_by_name(name)
            except Exception as e:
                print(e)
                return []
        elif smiles is not None:
            try:
                chem_data, syns = self.get_pubchem_cmpd_by_smiles(smiles)
            except Exception as e:
                print(e)
                return []

        # generate descriptors and predict properties
        try:
            mordred_desc = self.gen_mordred_descriptors(chem_data['smiles'])
        except Exception as e:
            print(e)
            print(f'Unable to generate descriptors for SMILES {name}')
            return []

        for p in PRED_PROP_CODES:
            # get the estimator
            est = PropertyEstimator.objects.filter(prop=p).latest(
                'added_tstamp'
            )
            pred = est.pred_from_full_mordred_desc_df(mordred_desc)
            chem_data[f'{p}_pred'] = pred
            chem_data[f'{p}_estimator'] = est

        chem = Chemical(**chem_data)
        chem.save()

        for s in syns:
            obj = ChemicalSynonym(name=s, chem=chem)
            obj.save()

        return [chem]

    def gen_mordred_descriptors(self, smiles):
        print('CALCULATING MOLECULAR DESCRIPTORS')
        mol = MolFromSmiles(smiles)
        calc = Calculator(descriptors)
        result = calc.pandas([mol])
        pairs = zip(
            result.columns,
            ['mordred_desc_' + i for i in result.columns]
        )
        col_rename_dict = {i: j for i, j in pairs}
        result = result.rename(columns=col_rename_dict)
        result['smiles'] = MolToSmiles(mol)
        return result

    def get_pubchem_cmpd_by_name(self, name):
        smiles = self.get_pubchem_smiles_from_name(name)
        if not smiles:
            raise Exception(f'No valid PubChem compounds matching {name}')
        return self.get_pubchem_cmpd_by_smiles(smiles)

    def get_pubchem_smiles_from_name(self, name):

        """if our names database does not contain this molecule's info,
        try getting it from pubchem API"""
        print('hitting pubchem api for names - names db doesnt have it')
        smiles = ""
        try:
            # add a try/except in case pubchem server failure
            data = requests.get(
                f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/'
                f'name/{name}/property/CanonicalSMILES/JSON'
            )
            data = data.json()
            smiles = data["PropertyTable"]["Properties"][0]["CanonicalSMILES"]
        except BaseException as e:
            print('pubchem not responsive', e)
        return smiles


class ChemicalSearchView(LoginRequiredMixin, TemplateView):

    template_name = 'chemical_search.html'
    component = 'ChemicalSearchPage.js'

    def get_context_data(self, **kwargs):
        return {'component': self.component}

    # TODO: override get_context_data() instead and use base class get()
    # def get(self, request):
    #     context = {
    #         'component': self.component,
    #     }
    #
    #     return render(request, self.template, context)


class ChemicalBlendView(LoginRequiredMixin, TemplateView):
    template = 'chemical_blend.html'
    component = 'ChemicalBlendPage.js'

    def get(self, request):
        context = {
            'component': self.component,
        }

        return render(request, self.template, context)


class ChemicalSubmissionFormView(LoginRequiredMixin, FormView, TemplateView):
    form_class = ChemicalSubmissionForm
    template_name = 'submit_chem_data.html'
    success_url = reverse_lazy('chem:submit_data_success')
    success_msg = "Chemical successfully submitted"

    def form_valid(self, form):
        """
        #TODO: validation to ensure that either manual entry or CSV was provided
        #TODO: validation to ensure that CSV is valid format
        :param form:
        :return:
        """

        # messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            send_chem_or_blend_submission_notification_email()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class SubmitDataSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'submit_data_success.html'


class BlendSubmissionFormView(LoginRequiredMixin, FormView, TemplateView):
    form_class = BlendSubmissionForm
    template_name = 'submit_blend_data.html'
    success_url = reverse_lazy('chem:submit_data_success')

    def form_valid(self, form):
        """
        #TODO: validation to ensure that either manual entry or CSV was provided
        #TODO: validation to ensure that CSV is valid format
        :param form:
        :return:
        """

        # messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            send_chem_or_blend_submission_notification_email()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


# helper functions
def send_chem_or_blend_submission_notification_email():
    mail_subject = 'New FTF Data Submission'
    message = render_to_string('data_submission_notify_email.html', {
        'domain': settings.SITE_DOMAIN,
    })
    # to_email = form.cleaned_data.get('email')
    to_email = settings.EMAIL_HOST_USER
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
