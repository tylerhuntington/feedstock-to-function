"""
Makes initial DB fixtures (JSON) for models in the chem app
"""

import os
from pathlib import PurePath, Path
import json
import simplejson as sjson
import logging
import pandas as pd
from django.core.management import call_command

from chem import (
    PROP_ESTIMATOR_MODELS_DIR,
    PROP_DESCRIPTORS_DIR,
    INIT_FIXTURES_DIR,
    RAW_DATA_DIR,
    PROD_DATA_DIR,
    PRED_PROP_CODES,
    CHEMS_IN_TEA_LCA_APP
)

from chem.models import PropertyEstimator, Chemical, Source

# config logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(name)s] %(message)s', datefmt='%m-%d %H:%M'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def get_mordred_desc_names(df):
    """
    Returns column names of dataframe prefixed with 'mordred_desc_
    indicating that the column contains data for a Mordred-generated
    descriptor.

    :param df: pd.DataFrame with Mordred descriptors
    :return:
    """

    return [c for c in df.columns if 'mordred_desc_' in c]


def make_property_estimator_fixtures():
    """
    Makes initial DB fixtures (JSON) for PropertyEstimator class
    :return:
    """

    objs = []
    model_fns = os.listdir(PROP_ESTIMATOR_MODELS_DIR)

    for i, fn in enumerate(model_fns, 1):
        obj = {}
        obj['pk'] = i
        obj['model'] = 'chem.PropertyEstimator'
        fields = {}
        fields['train_fit_serial_mod_fn'] = fn
        fields['full_fit_serial_mod_fn'] = fn.replace('.joblib', '_full.joblib')
        fields['uid'] = fn.replace('.joblib', '')
        prop = fn.split('_')[0]
        # get creation time id for pipeline
        tid = fn.split('_')[1].replace('.joblib', '')
        fields['prop'] = prop
        desc_fp = Path(
            PROP_DESCRIPTORS_DIR, f'{prop}_{tid}_descriptors.csv'
        )
        desc_df = pd.read_csv(desc_fp)
        fields['feat_names'] = get_mordred_desc_names(desc_df)

        # load descriptor values for chems in our dataset
        labl_col = [c for c in desc_df.columns if '_coalesced' in c][0]
        # fields['features'] = desc_df[fields['feat_names']].values.tolist()
        # fields['labels'] = desc_df[labl_col].values.tolist()
        fields['ids'] = desc_df['smiles'].values.tolist()
        obj['fields'] = fields
        objs.append(obj)

    outpath = PurePath(INIT_FIXTURES_DIR, 'PropertyEstimator.json')

    with open(outpath.as_posix(), 'w') as f:
        json.dump(objs, f)


def make_chemical_synonym_fixtures():
    """
    Makes initial DB fixtures (JSON) for ChemicalSynonym class
    :return:
    """
    syns_df = pd.read_csv(
        Path(
            PROD_DATA_DIR,
            'chemicalsynonyms_fixture_data.csv'
        )
    )
    objs = []
    for i in range(syns_df.shape[0]):
        syn = syns_df.loc[i, 'synonym']
        smiles = syns_df.loc[i, 'smiles']
        obj = {}
        fields = {}
        obj['model'] = 'chem.ChemicalSynonym'
        obj['pk'] = i + 1
        if syn != None:
            fields['name'] = syn
            fields['chem'] = Chemical.objects.get(smiles=smiles).pk
            obj['fields'] = fields
            objs.append(obj)

    # add synonym records for molecular names and iupac names from master data
    chems = pd.read_csv(Path(PROD_DATA_DIR, 'chemical_fixtures_data.csv'))
    for i in range(chems.shape[0]):
        for col in ['iupac', 'name']:
            syn = chems.loc[i, col]
            smiles = chems.loc[i, 'smiles']
            obj = {}
            fields = {}
            obj['model'] = 'chem.ChemicalSynonym'
            obj['pk'] = i + 1
            fields['name'] = syn
            fields['chem'] = Chemical.objects.get(smiles=smiles).pk
            obj['fields'] = fields
            objs.append(obj)

    outpath = PurePath(INIT_FIXTURES_DIR, 'ChemicalSynonym.json')

    with open(outpath.as_posix(), 'w') as f:
        json.dump(objs, f)


def make_chemical_fixtures():
    """
    Makes initial DB fixtures (JSON) for Chemical class
    :return:
    """

    # get estimator UIDs for each property for use populating fixture items
    est_pks = {}
    for p in PRED_PROP_CODES:
        # get the estimator
        est = PropertyEstimator.objects.filter(prop=p).latest('added_tstamp')
        est_pks[p] = est.pk

    chems = pd.read_csv(Path(PROD_DATA_DIR, 'chemical_fixtures_data.csv'))

    # make fixture objs
    objs = []
    for i in range(chems.shape[0]):
        # for i in range(10):
        obj = {}
        fields = {}
        chem = chems.iloc[i, :]
        smiles = chem['smiles']
        obj['model'] = 'chem.Chemical'
        # use i + 1 for primary key to avoid pk of 0 in django data model
        obj['pk'] = i + 1
        fields['name'] = chem['name']
        fields['smiles'] = smiles
        fields['inchi'] = chem['inchikey']
        fields['formula'] = chem['molecular formula']
        fields['iupac'] = chem['iupac']
        fields['pubchem_cid'] = chem['pubchem_cid']
        if smiles in CHEMS_IN_TEA_LCA_APP:
            fields['tea_lca_tool_alias'] = CHEMS_IN_TEA_LCA_APP[smiles]
        # property specific fields
        for p in PRED_PROP_CODES:
            # generate string for prop with unit
            p_u = f'{p}_c' if p in ['mp', 'bp', 'fp'] else p
            fields[f'{p}_exp'] = chem[f'{p_u}_coalesced']
            srcs = [s for s in str(chem[f'{p_u}_source']).split(', ')]
            srcs_pks = []
            for s in srcs:
                try:
                    src_pk = Source.objects.get(name=s).pk
                    srcs_pks.append(src_pk)
                except Exception as e:
                    continue

            fields[f'{p}_exp_srcs'] = srcs_pks
            fields[f'{p}_pred'] = chem[f'{p}_pred']
            # foreign key fields
            fields[f'{p}_estimator'] = est_pks[p]
        obj['fields'] = fields
        objs.append(obj)

    out_fp = PurePath(INIT_FIXTURES_DIR, 'Chemical.json')

    with open(out_fp.as_posix(), 'w') as f:
        sjson.dump(objs, f, ignore_nan=True)


def make_blend_fixtures():
    """
    Makes initial DB fixtures (JSON) for Chemical class
    :return:
    """

    blnds = pd.read_csv(Path(RAW_DATA_DIR, 'blends_property_data.csv'))
    # init fixture items accumulator

    syns_df = pd.read_csv(Path(RAW_DATA_DIR, 'molecule_reduced_synonyms.csv'))
    syns_dict = {}
    for s in syns_df.smiles.unique():
        syns = [s for s in syns_df[syns_df.smiles == s].synonym.values]
        syns_dict[s] = syns

    # define mappings from column names in CSV to model field names
    field_col_map = {
        'name': 'Blend',
        'perc': 'Percentage',
        'src': 'Source',
        'fp_exp': 'Flash Point',
        'fp_tst': 'Flash Point Test',
        'fzp_exp': 'Freezing Point',
        'fzp_tst': 'Freezing Point Test',
        'net_ht_cmbst_exp': 'Net Heat of Combustion',
        'net_ht_cmbst_tst': 'Net Heat of Combustion Test',
        'bp_exp_0': 'Boiling Point_0',
        'bp_exp_10': 'Boiling Point_10',
        'bp_exp_50': 'Boiling Point_50',
        'bp_exp_90': 'Boiling Point_90',
        'bp_exp_100': 'Boiling Point_100',
        'bp_tst': 'Boiling Point Test',
        'dens_15_exp': 'Density_15C (g/m2)',
        'dens_tst': 'Density Test',
        'visc_n20_exp': 'Viscosity_-20C',
        'visc_tst': 'Viscosity Test',
        'arom_exp': 'Aromatics',
        'arom_tst': 'Aromatics Test',
        'slfr_mass_exp': 'Sulfur (% mass)',
        'slfr_wt_exp': 'Sulfur (% weight)',
        'slfr_tst': 'Sulfur Test',
        'naph_exp': 'Naphthalene (% vol)',
        'naph_tst': 'Naphthalene Test',
        'hydgn_mass_exp': 'Hydrogen (%mass)',
        'hydgn_tst': 'Hydrogen Test',
        'olef_exp': 'Olefins (% vol)',
        'olef_tst': 'Olefins Test',
        'lbrc_exp': 'Lubricity (mm)',
        'lbrc_tst': 'Lubricity Test',
    }
    # make fixture objs
    objs = []
    for i in range(blnds.shape[0]):
        # for i in range(10):
        obj = {}
        fields = {}
        blnd = blnds.iloc[i, :]
        obj['model'] = 'chem.Blend'
        # use i + 1 for primary key to avoid pk of 0 in django data model
        obj['pk'] = i + 1
        for field, col in field_col_map.items():
            fields[field] = blnd[col]

        # property specific fields
        obj['fields'] = fields
        objs.append(obj)

    out_fp = PurePath(INIT_FIXTURES_DIR, 'Blend.json')

    with open(out_fp.as_posix(), 'w') as f:
        sjson.dump(objs, f, ignore_nan=True)


def make_load_blend_fixtures():
    make_blend_fixtures()
    call_command('loaddata', 'chem/init_fixtures/Blend.json')


def make_load_property_estimator_fixtures():
    make_property_estimator_fixtures()
    call_command('loaddata', 'chem/init_fixtures/PropertyEstimator.json')


def make_load_chemical_fixtures():
    make_chemical_fixtures()
    call_command('loaddata', 'chem/init_fixtures/Chemical.json')


def make_load_chemical_synonym_fixtures():
    make_chemical_synonym_fixtures()
    call_command('loaddata', 'chem/init_fixtures/ChemicalSynonym.json')


def make_load_source_fixtures():
    call_command('loaddata', 'chem/init_fixtures/Source.json')


def run(*args):
    # make_load_blend_fixtures()
    # make_load_source_fixtures()
    # make_load_chemical_fixtures()
    # make_load_chemical_synonym_fixtures()
    call_command('loaddata', 'chem/init_fixtures/Blend.json')
    make_load_property_estimator_fixtures()
    call_command('loaddata', 'chem/init_fixtures/Source.json')
    call_command('loaddata', 'chem/init_fixtures/Chemical.json')
    call_command('loaddata', 'chem/init_fixtures/ChemicalSynonym.json')
