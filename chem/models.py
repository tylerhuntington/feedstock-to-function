import numpy as np
import joblib
import json
from django.conf import settings
from pathlib import Path
from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField
from django.contrib.postgres.fields import ArrayField
from chem import PROP_ESTIMATOR_MODELS_DIR, CHEM_STRUCT_IMG_DIR, CHEMS_IN_TEA_LCA_APP
from rdkit.Chem import MolToSmiles, MolFromSmiles
from rdkit.Chem.Draw import MolToFile


class Source(models.Model):
    name = models.CharField(max_length=500)
    link = models.URLField(default='#', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class PropertyEstimator(models.Model):

    uid = models.CharField(max_length=300, unique=True)
    prop = models.CharField(max_length=500)
    added_tstamp = models.DateTimeField(auto_now=True, blank=True, null=True)
    feat_names = JSONField(default=list)
    features = ArrayField(
        ArrayField(models.FloatField()),
        blank=True, null=True
    )
    labels = ArrayField(models.FloatField(), blank=True, null=True)
    ids = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    train_fit_serial_mod_fn = models.FilePathField(
        PROP_ESTIMATOR_MODELS_DIR.as_posix()
    )
    full_fit_serial_mod_fn = models.FilePathField(
        PROP_ESTIMATOR_MODELS_DIR.as_posix()
    )

    def pred_from_full_mordred_desc_df(self, desc_df):
        try:
            df = desc_df[self.feat_names]
            arr = np.array(df.values.flatten().reshape(1, -1))
            # est = self.mod_fit_to_full_set
            pred = self.mod_fit_to_train_set.predict(arr)
            return pred
        except Exception as e:
            print(f'Could not predict prop: {self.prop}')
            print(e)
            return

    def _fit_mod_to_full_set_and_serialize(self):

        m = self.mod_fit_to_train_set
        m.fit(self.features, self.labels)
        joblib.dump(
            m,
            Path(
                PROP_ESTIMATOR_MODELS_DIR,
                self.train_fit_serial_mod_fn.replace('.joblib', '_full.joblib')
            )
        )

    @property
    def mod_fit_to_train_set(self):
        fp = Path(PROP_ESTIMATOR_MODELS_DIR, self.train_fit_serial_mod_fn)
        m = joblib.load(fp)
        return m

    @property
    def mod_fit_to_full_set(self):
        full_fit_mod_fp = Path(
            PROP_ESTIMATOR_MODELS_DIR,
            self.train_fit_serial_mod_fn.replace('.joblib', '_full.joblib')
        )
        if not full_fit_mod_fp.is_file():
            self._fit_mod_to_full_set_and_serialize()
        fp = Path(PROP_ESTIMATOR_MODELS_DIR, self.full_fit_serial_mod_fn)
        m = joblib.load(fp)
        return m


class ChemicalSubmission(models.Model):

    name = models.CharField(max_length=500, blank=True, null=True)
    smiles = models.CharField(max_length=500, blank=True, null=True)
    formula = models.CharField(max_length=500, blank=True, null=True)
    inchi = models.CharField(max_length=500, blank=True, null=True)
    iupac = models.CharField(max_length=500, blank=True, null=True)
    cas = models.CharField(max_length=500, blank=True, null=True)

    bp_exp = models.FloatField(blank=True, null=True)
    mp_exp = models.FloatField(blank=True, null=True)
    fp_exp = models.FloatField(blank=True, null=True)
    ysi_exp = models.FloatField(blank=True, null=True)
    cn_exp = models.FloatField(blank=True, null=True)
    dcn_exp = models.FloatField(blank=True, null=True)

    bp_src = models.CharField(max_length=500, blank=True, null=True)
    bp_tst = models.CharField(max_length=500, blank=True, null=True)
    bp_notes = models.CharField(max_length=500, blank=True, null=True)

    mp_src = models.CharField(max_length=500, blank=True, null=True)
    mp_tst = models.CharField(max_length=500, blank=True, null=True)
    mp_notes = models.CharField(max_length=500, blank=True, null=True)

    fp_src = models.CharField(max_length=500, blank=True, null=True)
    fp_tst = models.CharField(max_length=500, blank=True, null=True)
    fp_notes = models.CharField(max_length=500, blank=True, null=True)

    cn_src = models.CharField(max_length=500, blank=True, null=True)
    cn_tst = models.CharField(max_length=500, blank=True, null=True)
    cn_notes = models.CharField(max_length=500, blank=True, null=True)

    dcn_src = models.CharField(max_length=500, blank=True, null=True)
    dcn_tst = models.CharField(max_length=500, blank=True, null=True)
    dcn_notes = models.CharField(max_length=500, blank=True, null=True)

    ysi_src = models.CharField(max_length=500, blank=True, null=True)
    ysi_tst = models.CharField(max_length=500, blank=True, null=True)
    ysi_notes = models.CharField(max_length=500, blank=True, null=True)


    # density at user-specified temp
    dens_x_val = models.FloatField(blank=True, null=True)
    dens_x_temp = models.FloatField(blank=True, null=True)
    dens_x_src = models.CharField(max_length=500, blank=True, null=True)
    dens_x_tst = models.CharField(max_length=500, blank=True, null=True)
    dens_x_notes = models.CharField(max_length=500, blank=True, null=True)

    # density at user-specified temp
    dens_y_val = models.FloatField(blank=True, null=True)
    dens_y_temp = models.FloatField(blank=True, null=True)
    dens_y_src = models.CharField(max_length=500, blank=True, null=True)
    dens_y_tst = models.CharField(max_length=500, blank=True, null=True)
    dens_y_notes = models.CharField(max_length=500, blank=True, null=True)

    # density at user-specified temp
    dens_z_val = models.FloatField(blank=True, null=True)
    dens_z_temp = models.FloatField(blank=True, null=True)
    dens_z_src = models.CharField(max_length=500, blank=True, null=True)
    dens_z_tst = models.CharField(max_length=500, blank=True, null=True)
    dens_z_notes = models.CharField(max_length=500, blank=True, null=True)

    # viscity at user-specified temp
    visc_x_val = models.FloatField(blank=True, null=True)
    visc_x_temp = models.FloatField(blank=True, null=True)
    visc_x_src = models.CharField(max_length=500, blank=True, null=True)
    visc_x_tst = models.CharField(max_length=500, blank=True, null=True)
    visc_x_notes = models.CharField(max_length=500, blank=True, null=True)

    # viscity at user-specified temp
    visc_y_val = models.FloatField(blank=True, null=True)
    visc_y_temp = models.FloatField(blank=True, null=True)
    visc_y_src = models.CharField(max_length=500, blank=True, null=True)
    visc_y_tst = models.CharField(max_length=500, blank=True, null=True)
    visc_y_notes = models.CharField(max_length=500, blank=True, null=True)

    # viscity at user-specified temp
    visc_z_val = models.FloatField(blank=True, null=True)
    visc_z_temp = models.FloatField(blank=True, null=True)
    visc_z_src = models.CharField(max_length=500, blank=True, null=True)
    visc_z_tst = models.CharField(max_length=500, blank=True, null=True)
    visc_z_notes = models.CharField(max_length=500, blank=True, null=True)

    # net heat of combustion
    net_ht_cmbst_val = models.FloatField(blank=True, null=True)
    net_ht_cmbst_src = models.CharField(max_length=500, blank=True, null=True)
    net_ht_cmbst_tst = models.CharField(max_length=500, blank=True, null=True)
    net_ht_cmbst_notes = models.CharField(max_length=500, blank=True, null=True)

    # user-specified property 1
    oth_prop_1_name = models.FloatField(blank=True, null=True)
    oth_prop_1_val = models.FloatField(blank=True, null=True)
    oth_prop_1_src = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_1_tst = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_1_notes = models.CharField(max_length=500, blank=True, null=True)

    # user-specified property 2
    oth_prop_1_name = models.FloatField(blank=True, null=True)
    oth_prop_1_val = models.FloatField(blank=True, null=True)
    oth_prop_1_src = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_1_tst = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_1_notes = models.CharField(max_length=500, blank=True, null=True)

    # user-specified property 1
    oth_prop_3_name = models.FloatField(blank=True, null=True)
    oth_prop_3_val = models.FloatField(blank=True, null=True)
    oth_prop_3_src = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_3_tst = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_3_notes = models.CharField(max_length=500, blank=True, null=True)

    # contributor info
    contrib_name = models.CharField(max_length=500, blank=True, null=True)
    contrib_email = models.EmailField(blank=False, null=True)
    contrib_affil = models.CharField(max_length=500, blank=True, null=True)
    comments = models.CharField(max_length=1000, blank=True, null=True)

    csv_submission = models.FileField(upload_to='chem_csv_submissions',
        blank=True, null=True
    )


    @property
    def bp_unit(self):
        return 'C'

    @property
    def mp_unit(self):
        return 'C'

    @property
    def fp_unit(self):
        return 'C'


class Chemical(models.Model):

    name = models.CharField(max_length=500, blank=True, null=True)
    smiles = models.CharField(max_length=500, unique=True)
    formula = models.CharField(max_length=500, blank=True, null=True)
    inchi = models.CharField(max_length=500, blank=True, null=True)
    iupac = models.CharField(max_length=500, blank=True, null=True)
    pubchem_cid = models.IntegerField(blank=True, null=True)
    added_tstamp = models.DateTimeField(auto_now=True, blank=True, null=True)
    tea_lca_tool_alias = models.CharField(max_length=200, blank=True, null=True)

    bp_exp = models.FloatField(blank=True, null=True)
    mp_exp = models.FloatField(blank=True, null=True)
    fp_exp = models.FloatField(blank=True, null=True)
    ysi_exp = models.FloatField(blank=True, null=True)
    cn_exp = models.FloatField(blank=True, null=True)
    dcn_exp = models.FloatField(blank=True, null=True)
    hoc_exp = models.FloatField(blank=True, null=True)

    bp_pred = models.FloatField(blank=True, null=True)
    mp_pred = models.FloatField(blank=True, null=True)
    fp_pred = models.FloatField(blank=True, null=True)
    ysi_pred = models.FloatField(blank=True, null=True)
    cn_pred = models.FloatField(blank=True, null=True)
    dcn_pred = models.FloatField(blank=True, null=True)
    hoc_pred = models.FloatField(blank=True, null=True)

    bp_pred_err_up = models.FloatField(blank=True, null=True)
    bp_pred_err_low = models.FloatField(blank=True, null=True)
    mp_pred_err_up = models.FloatField(blank=True, null=True)
    mp_pred_err_low = models.FloatField(blank=True, null=True)
    fp_pred_err_up = models.FloatField(blank=True, null=True)
    fp_pred_err_low = models.FloatField(blank=True, null=True)
    ysi_pred_err_up = models.FloatField(blank=True, null=True)
    ysi_pred_err_low = models.FloatField(blank=True, null=True)
    hoc_pred_err_up = models.FloatField(blank=True, null=True)
    hoc_pred_err_low = models.FloatField(blank=True, null=True)

    fp_pred_perc_err = models.FloatField(blank=True, null=True)
    ysi_pred_perc_err = models.FloatField(blank=True, null=True)
    cn_pred_perc_err = models.FloatField(blank=True, null=True)
    dcn_pred_perc_err = models.FloatField(
        blank=True, null=True, default=39.3
    )

    # TODO: refactor these fields into PropertyEstimator class and implement
    # corresponding @property accessor methods for Chemical class
    bp_pred_perc_err = models.FloatField(blank=True, null=True)
    mp_pred_perc_err = models.FloatField(blank=True, null=True)
    fp_pred_perc_err = models.FloatField(blank=True, null=True)
    ysi_pred_perc_err = models.FloatField(blank=True, null=True)
    cn_pred_perc_err = models.FloatField(blank=True, null=True)
    dcn_pred_perc_err = models.FloatField(
        blank=True, null=True
    )

    bp_estimator = models.ForeignKey(
        PropertyEstimator, on_delete=models.CASCADE, related_name='bp_estimator',
        null=True,
    )
    mp_estimator = models.ForeignKey(
        PropertyEstimator, on_delete=models.CASCADE, related_name='mp_estimator',
        null=True,
    )
    fp_estimator = models.ForeignKey(
        PropertyEstimator, on_delete=models.CASCADE, related_name='fp_estimator',
        null=True,
    )
    ysi_estimator = models.ForeignKey(
        PropertyEstimator,
        on_delete=models.CASCADE,
        related_name='ysi_estimator',
        null=True,
    )
    cn_estimator = models.ForeignKey(
        PropertyEstimator, on_delete=models.CASCADE, related_name='cn_estimator',
        null=True,
    )
    dcn_estimator = models.ForeignKey(
        PropertyEstimator,
        on_delete=models.CASCADE,
        related_name='dcn_estimator',
        null=True,
    )

    bp_exp_srcs = models.ManyToManyField(
        Source, related_name='bp_exp_srcs', blank=True,
    )
    mp_exp_srcs = models.ManyToManyField(
        Source, related_name='mp_exp_srcs', blank=True,
    )
    fp_exp_srcs = models.ManyToManyField(
        Source, related_name='fp_exp_srcs', blank=True,
    )
    ysi_exp_srcs = models.ManyToManyField(
        Source, related_name='ysi_exp_srcs', blank=True,
    )
    cn_exp_srcs = models.ManyToManyField(
        Source, related_name='cn_exp_srcs', blank=True,
    )
    dcn_exp_srcs = models.ManyToManyField(
        Source, related_name='dcn_exp_srcs', blank=True,
    )

    _struct_img = models.FilePathField(
                  CHEM_STRUCT_IMG_DIR.as_posix(),
                  blank=True, null=True
    )

    @property
    def struct_img(self):
        """ generates rdkit image and stores it as
        static/images/molecule.png"""
        return

    @property
    def hoc_unit(self):
        return 'MJ/kg'

    @property
    def bp_unit(self):
        return 'C'

    @property
    def mp_unit(self):
        return 'C'

    @property
    def fp_unit(self):
        return 'C'

    @property
    def syns_list(self):
        # TODO implement query for syns from ChemicalSynonyms class
        syns = [s.name for s in self.synonyms.all() if s.name != 'nan']
        syns = set(syns)
        return syns

    @property
    def names_str(self):
        # TODO implement query for syns from ChemicalSynonyms class
        syns = [s.name for s in ChemicalSynonym.objects.filter(chem=self.pk)]
        syns = [s for s in syns if s != 'nan']
        syns = [self.name] + syns
        syns_str = '; '.join(syns)
        return syns_str

    @property
    def bp_pred_abs_err(self):
        try:
            return abs(self.bp_pred_perc_err * self.bp_pred / 100)
        except Exception as e:
            print(e)
            return

    @property
    def mp_pred_abs_err(self):
        try:
            return abs(self.mp_pred_perc_err * self.mp_pred / 100)
        except Exception as e:
            print(e)
            return

    @property
    def fp_pred_abs_err(self):
        try:
            return abs(self.fp_pred_perc_err * self.fp_pred / 100)
        except Exception as e:
            print(e)
            return

    @property
    def ysi_pred_abs_err(self):
        try:
            return abs(self.ysi_pred_perc_err * self.ysi_pred / 100)
        except Exception as e:
            print(e)
            return

    @property
    def dcn_pred_abs_err(self):
        try:
            return abs(self.dcn_pred_perc_err * self.dcn_pred / 100)
        except Exception as e:
            print(e)
            return

    @property
    def cn_pred_abs_err(self):
        try:
            return abs(self.cn_pred_perc_err * self.cn_pred / 100)
        except Exception as e:
            print(e)
            return



    # @property
    # def srcs_dict(self):
    #     for obj in self.sr
    #     {'name': }

class ChemicalSynonym(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    chem = models.ForeignKey(
        Chemical, on_delete=models.CASCADE, related_name='synonyms'
    )
    def __str__(self):
        return f'{self.name}'

class BlendComponent(models.Model):
    chem = models.ForeignKey(Chemical, on_delete=models.CASCADE)
    fraction = models.FloatField()

class Blend(models.Model):
    """
    TODO: implement this class whose instances are created upon parsing and
    validation of BlendSubmission objects generated by users when they
    submit the corresponding BlendSubmissionForm.
    """
    name = models.CharField(max_length=500, blank=True, null=True)
    perc = models.CharField(max_length=200, blank=True, null=True)
    src = models.CharField(max_length=500, blank=True, null=True)

    fp_exp = models.FloatField(blank=True, null=True)
    fp_tst = models.CharField(max_length=500, blank=True, null=True)
    fzp_exp = models.FloatField(blank=True, null=True)
    fzp_tst = models.CharField(max_length=500, blank=True, null=True)
    net_ht_cmbst_exp = models.FloatField(blank=True, null=True)
    net_ht_cmbst_tst = models.CharField(max_length=500, blank=True, null=True)

    bp_exp_0 = models.FloatField(blank=True, null=True)
    bp_exp_10 = models.FloatField(blank=True, null=True)
    bp_exp_50 = models.FloatField(blank=True, null=True)
    bp_exp_90 = models.FloatField(blank=True, null=True)
    bp_exp_100 = models.FloatField(blank=True, null=True)
    bp_tst = models.CharField(max_length=500, blank=True, null=True)

    # density at 15 C
    dens_15_exp = models.FloatField(blank=True, null=True)
    dens_tst = models.CharField(max_length=500, blank=True, null=True)

    # viscosity at -15 C
    visc_n20_exp = models.FloatField(blank=True, null=True)
    visc_tst = models.CharField(max_length=500, blank=True, null=True)

    # aromatics
    arom_exp = models.FloatField(blank=True, null=True)
    arom_tst = models.CharField(max_length=500, blank=True, null=True)

    # sulfur
    slfr_mass_exp = models.FloatField(blank=True, null=True)
    slfr_wt_exp = models.FloatField(blank=True, null=True)
    slfr_tst = models.CharField(max_length=500, blank=True, null=True)

    # naphthalene
    naph_exp = models.FloatField(blank=True, null=True)
    naph_tst = models.CharField(max_length=500, blank=True, null=True)

    # hydrogen
    hydgn_mass_exp = models.FloatField(blank=True, null=True)
    hydgn_tst = models.CharField(max_length=500, blank=True, null=True)

    # olefins percentage by volume
    olef_exp = models.FloatField(blank=True, null=True)
    olef_tst = models.CharField(max_length=500, blank=True, null=True)

    # lubricity (mm)
    lbrc_exp = models.FloatField(blank=True, null=True)
    lbrc_tst = models.CharField(max_length=500, blank=True, null=True)


    # TODO finish implementing unit properties
    @property
    def lbrc_unit(self):
        """
        Lubricity unit
        :return:
        """
        return 'mm'

    @property
    def olef_unit(self):
        """
        Olefins unit
        :return:
        """
        return '% vol'

    @property
    def naph_unit(self):
        """
        Naphthalene unit
        :return:
        """
        return '% vol'


class BlendSubmission(models.Model):

    name = models.CharField(max_length=500, blank=True, null=True)
    cas = models.CharField(max_length=500, blank=True, null=True)

    # blend component names
    comp_1_name = models.CharField(max_length=500, blank=True, null=True)
    comp_2_name = models.CharField(max_length=500, blank=True, null=True)
    comp_3_name = models.CharField(max_length=500, blank=True, null=True)
    comp_4_name = models.CharField(max_length=500, blank=True, null=True)
    comp_5_name = models.CharField(max_length=500, blank=True, null=True)
    comp_6_name = models.CharField(max_length=500, blank=True, null=True)
    comp_7_name = models.CharField(max_length=500, blank=True, null=True)
    comp_8_name = models.CharField(max_length=500, blank=True, null=True)
    comp_9_name = models.CharField(max_length=500, blank=True, null=True)
    comp_10_name = models.CharField(max_length=500, blank=True, null=True)

    # blend component fractions
    comp_1_perc = models.FloatField(blank=True, null=True)
    comp_2_perc = models.FloatField(blank=True, null=True)
    comp_3_perc = models.FloatField(blank=True, null=True)
    comp_4_perc = models.FloatField(blank=True, null=True)
    comp_5_perc = models.FloatField(blank=True, null=True)
    comp_6_perc = models.FloatField(blank=True, null=True)
    comp_7_perc = models.FloatField(blank=True, null=True)
    comp_8_perc = models.FloatField(blank=True, null=True)
    comp_9_perc = models.FloatField(blank=True, null=True)
    comp_10_perc = models.FloatField(blank=True, null=True)

    bp_exp_0 = models.FloatField(blank=True, null=True)
    bp_exp_10 = models.FloatField(blank=True, null=True)
    bp_exp_50 = models.FloatField(blank=True, null=True)
    bp_exp_90 = models.FloatField(blank=True, null=True)
    bp_exp_100 = models.FloatField(blank=True, null=True)

    bp_src_0 = models.CharField(max_length=500, blank=True, null=True)
    bp_tst_0 = models.CharField(max_length=500, blank=True, null=True)
    bp_notes_0 = models.CharField(max_length=500, blank=True, null=True)

    bp_src_10 = models.CharField(max_length=500, blank=True, null=True)
    bp_tst_10 = models.CharField(max_length=500, blank=True, null=True)
    bp_notes_10 = models.CharField(max_length=500, blank=True, null=True)
    bp_src_50 = models.CharField(max_length=500, blank=True, null=True)
    bp_tst_50 = models.CharField(max_length=500, blank=True, null=True)
    bp_notes_50 = models.CharField(max_length=500, blank=True, null=True)
    bp_src_90 = models.CharField(max_length=500, blank=True, null=True)
    bp_tst_90 = models.CharField(max_length=500, blank=True, null=True)
    bp_notes_90 = models.CharField(max_length=500, blank=True, null=True)
    bp_src_100 = models.CharField(max_length=500, blank=True, null=True)
    bp_tst_100 = models.CharField(max_length=500, blank=True, null=True)
    bp_notes_100 = models.CharField(max_length=500, blank=True, null=True)


    bp_temp_oth = models.FloatField(blank=True, null=True)
    bp_exp_oth = models.FloatField(blank=True, null=True)
    bp_src_oth = models.CharField(max_length=500, blank=True, null=True)
    bp_tst_oth = models.CharField(max_length=500, blank=True, null=True)
    bp_notes_oth = models.CharField(max_length=500, blank=True, null=True)


    frzp_exp = models.FloatField(blank=True, null=True)
    frzp_src = models.CharField(max_length=500, blank=True, null=True)
    frzp_tst = models.CharField(max_length=500, blank=True, null=True)
    frzp_notes = models.CharField(max_length=500, blank=True, null=True)

    fp_exp = models.FloatField(blank=True, null=True)
    fp_src = models.CharField(max_length=500, blank=True, null=True)
    fp_tst = models.CharField(max_length=500, blank=True, null=True)
    fp_notes = models.CharField(max_length=500, blank=True, null=True)

    # aromatics
    arom_exp = models.FloatField(blank=True, null=True)
    arom_src = models.CharField(max_length=500, blank=True, null=True)
    arom_tst = models.CharField(max_length=500, blank=True, null=True)
    arom_notes = models.CharField(max_length=500, blank=True, null=True)

    # sulfer percentage by weight
    slfr_exp = models.FloatField(blank=True, null=True)
    slfr_src = models.CharField(max_length=500, blank=True, null=True)
    slfr_tst = models.CharField(max_length=500, blank=True, null=True)
    slfr_notes = models.CharField(max_length=500, blank=True, null=True)

    # net heat of combustion
    net_ht_cmbst_exp = models.FloatField(blank=True, null=True)
    net_ht_cmbst_src = models.CharField(max_length=500, blank=True, null=True)
    net_ht_cmbst_tst = models.CharField(max_length=500, blank=True, null=True)
    net_ht_cmbst_notes = models.CharField(max_length=500, blank=True, null=True)

    # naph percentage by volume
    naph_exp = models.FloatField(blank=True, null=True)
    naph_src = models.CharField(max_length=500, blank=True, null=True)
    naph_tst = models.CharField(max_length=500, blank=True, null=True)
    naph_notes = models.CharField(max_length=500, blank=True, null=True)

    # lubricity
    lbrc_exp = models.FloatField(blank=True, null=True)
    lbrc_src = models.CharField(max_length=500, blank=True, null=True)
    lbrc_tst = models.CharField(max_length=500, blank=True, null=True)
    lbrc_notes = models.CharField(max_length=500, blank=True, null=True)

    # density at 15 degrees C
    dens_15_exp = models.FloatField(blank=True, null=True)
    dens_15_src = models.CharField(max_length=500, blank=True, null=True)
    dens_15_tst = models.CharField(max_length=500, blank=True, null=True)
    dens_15_notes = models.CharField(max_length=500, blank=True, null=True)

    # density at user-specified temp
    dens_x_exp = models.FloatField(blank=True, null=True)
    dens_x_temp = models.FloatField(blank=True, null=True)
    dens_x_src = models.CharField(max_length=500, blank=True, null=True)
    dens_x_tst = models.CharField(max_length=500, blank=True, null=True)
    dens_x_notes = models.CharField(max_length=500, blank=True, null=True)

    # viscosity at -20 degrees C
    visc_n20_exp = models.FloatField(blank=True, null=True)
    visc_n20_src = models.CharField(max_length=500, blank=True, null=True)
    visc_n20_tst = models.CharField(max_length=500, blank=True, null=True)
    visc_n20_notes = models.CharField(max_length=500, blank=True, null=True)

    # viscocity at user-specified temp
    visc_x_exp = models.FloatField(blank=True, null=True)
    visc_x_temp = models.FloatField(blank=True, null=True)
    visc_x_src = models.CharField(max_length=500, blank=True, null=True)
    visc_x_tst = models.CharField(max_length=500, blank=True, null=True)
    visc_x_notes = models.CharField(max_length=500, blank=True, null=True)

    # user-specified property 1
    oth_prop_1_name = models.FloatField(blank=True, null=True)
    oth_prop_1_exp = models.FloatField(blank=True, null=True)
    oth_prop_1_src = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_1_tst = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_1_notes = models.CharField(max_length=500, blank=True, null=True)

    # user-specified property 2
    oth_prop_1_name = models.FloatField(blank=True, null=True)
    oth_prop_1_exp = models.FloatField(blank=True, null=True)
    oth_prop_1_src = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_1_tst = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_1_notes = models.CharField(max_length=500, blank=True, null=True)

    # user-specified property 1
    oth_prop_3_name = models.FloatField(blank=True, null=True)
    oth_prop_3_exp = models.FloatField(blank=True, null=True)
    oth_prop_3_temp = models.FloatField(blank=True, null=True)
    oth_prop_3_src = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_3_tst = models.CharField(max_length=500, blank=True, null=True)
    oth_prop_3_notes = models.CharField(max_length=500, blank=True, null=True)

    # contributor info
    contrib_name = models.CharField(max_length=500, blank=True, null=True)
    contrib_email = models.EmailField(blank=False, null=True)
    contrib_affil = models.CharField(max_length=500, blank=True, null=True)
    comments = models.TextField(max_length=1000, blank=True, null=True)

    csv_submission = models.FileField(upload_to='blend_csv_submissions',
                                      blank=True, null=True
                                      )

for smiles, alias in CHEMS_IN_TEA_LCA_APP.items():
    try:
        objs = Chemical.objects.filter(smiles__iexact=smiles)
        for obj in objs:
            obj.tea_lca_tool_alias = alias
            obj.save()
    except Exception:
        print(
            """
            Failed to register chemicals in TEA/LCA app. Make sure the
            database is up to date with current migrations
            """
        )














