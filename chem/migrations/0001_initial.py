# Generated by Django 3.0.3 on 2021-04-28 22:34

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('perc', models.CharField(blank=True, max_length=200, null=True)),
                ('src', models.CharField(blank=True, max_length=500, null=True)),
                ('fp_exp', models.FloatField(blank=True, null=True)),
                ('fp_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('fzp_exp', models.FloatField(blank=True, null=True)),
                ('fzp_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('net_ht_cmbst_exp', models.FloatField(blank=True, null=True)),
                ('net_ht_cmbst_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_exp_0', models.FloatField(blank=True, null=True)),
                ('bp_exp_10', models.FloatField(blank=True, null=True)),
                ('bp_exp_50', models.FloatField(blank=True, null=True)),
                ('bp_exp_90', models.FloatField(blank=True, null=True)),
                ('bp_exp_100', models.FloatField(blank=True, null=True)),
                ('bp_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_15_exp', models.FloatField(blank=True, null=True)),
                ('dens_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_n20_exp', models.FloatField(blank=True, null=True)),
                ('visc_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('arom_exp', models.FloatField(blank=True, null=True)),
                ('arom_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('slfr_mass_exp', models.FloatField(blank=True, null=True)),
                ('slfr_wt_exp', models.FloatField(blank=True, null=True)),
                ('slfr_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('naph_exp', models.FloatField(blank=True, null=True)),
                ('naph_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('hydgn_mass_exp', models.FloatField(blank=True, null=True)),
                ('hydgn_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('olef_exp', models.FloatField(blank=True, null=True)),
                ('olef_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('lbrc_exp', models.FloatField(blank=True, null=True)),
                ('lbrc_tst', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlendSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('cas', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_1_name', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_2_name', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_3_name', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_4_name', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_5_name', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_6_name', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_7_name', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_8_name', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_9_name', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_10_name', models.CharField(blank=True, max_length=500, null=True)),
                ('comp_1_perc', models.FloatField(blank=True, null=True)),
                ('comp_2_perc', models.FloatField(blank=True, null=True)),
                ('comp_3_perc', models.FloatField(blank=True, null=True)),
                ('comp_4_perc', models.FloatField(blank=True, null=True)),
                ('comp_5_perc', models.FloatField(blank=True, null=True)),
                ('comp_6_perc', models.FloatField(blank=True, null=True)),
                ('comp_7_perc', models.FloatField(blank=True, null=True)),
                ('comp_8_perc', models.FloatField(blank=True, null=True)),
                ('comp_9_perc', models.FloatField(blank=True, null=True)),
                ('comp_10_perc', models.FloatField(blank=True, null=True)),
                ('bp_exp_0', models.FloatField(blank=True, null=True)),
                ('bp_exp_10', models.FloatField(blank=True, null=True)),
                ('bp_exp_50', models.FloatField(blank=True, null=True)),
                ('bp_exp_90', models.FloatField(blank=True, null=True)),
                ('bp_exp_100', models.FloatField(blank=True, null=True)),
                ('bp_src_0', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_tst_0', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_notes_0', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_src_10', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_tst_10', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_notes_10', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_src_50', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_tst_50', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_notes_50', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_src_90', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_tst_90', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_notes_90', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_src_100', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_tst_100', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_notes_100', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_temp_oth', models.FloatField(blank=True, null=True)),
                ('bp_exp_oth', models.FloatField(blank=True, null=True)),
                ('bp_src_oth', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_tst_oth', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_notes_oth', models.CharField(blank=True, max_length=500, null=True)),
                ('frzp_exp', models.FloatField(blank=True, null=True)),
                ('frzp_src', models.CharField(blank=True, max_length=500, null=True)),
                ('frzp_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('frzp_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('fp_exp', models.FloatField(blank=True, null=True)),
                ('fp_src', models.CharField(blank=True, max_length=500, null=True)),
                ('fp_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('fp_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('arom_exp', models.FloatField(blank=True, null=True)),
                ('arom_src', models.CharField(blank=True, max_length=500, null=True)),
                ('arom_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('arom_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('slfr_exp', models.FloatField(blank=True, null=True)),
                ('slfr_src', models.CharField(blank=True, max_length=500, null=True)),
                ('slfr_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('slfr_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('net_ht_cmbst_exp', models.FloatField(blank=True, null=True)),
                ('net_ht_cmbst_src', models.CharField(blank=True, max_length=500, null=True)),
                ('net_ht_cmbst_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('net_ht_cmbst_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('naph_exp', models.FloatField(blank=True, null=True)),
                ('naph_src', models.CharField(blank=True, max_length=500, null=True)),
                ('naph_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('naph_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('lbrc_exp', models.FloatField(blank=True, null=True)),
                ('lbrc_src', models.CharField(blank=True, max_length=500, null=True)),
                ('lbrc_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('lbrc_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_15_exp', models.FloatField(blank=True, null=True)),
                ('dens_15_src', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_15_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_15_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_x_exp', models.FloatField(blank=True, null=True)),
                ('dens_x_temp', models.FloatField(blank=True, null=True)),
                ('dens_x_src', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_x_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_x_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_n20_exp', models.FloatField(blank=True, null=True)),
                ('visc_n20_src', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_n20_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_n20_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_x_exp', models.FloatField(blank=True, null=True)),
                ('visc_x_temp', models.FloatField(blank=True, null=True)),
                ('visc_x_src', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_x_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_x_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_1_name', models.FloatField(blank=True, null=True)),
                ('oth_prop_1_exp', models.FloatField(blank=True, null=True)),
                ('oth_prop_1_src', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_1_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_1_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_3_name', models.FloatField(blank=True, null=True)),
                ('oth_prop_3_exp', models.FloatField(blank=True, null=True)),
                ('oth_prop_3_temp', models.FloatField(blank=True, null=True)),
                ('oth_prop_3_src', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_3_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_3_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('contrib_name', models.CharField(blank=True, max_length=500, null=True)),
                ('contrib_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contrib_affil', models.CharField(blank=True, max_length=500, null=True)),
                ('comments', models.TextField(blank=True, max_length=1000, null=True)),
                ('csv_submission', models.FileField(blank=True, null=True, upload_to='blend_csv_submissions')),
            ],
        ),
        migrations.CreateModel(
            name='Chemical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('smiles', models.CharField(max_length=500, unique=True)),
                ('formula', models.CharField(blank=True, max_length=500, null=True)),
                ('inchi', models.CharField(blank=True, max_length=500, null=True)),
                ('iupac', models.CharField(blank=True, max_length=500, null=True)),
                ('pubchem_cid', models.IntegerField(blank=True, null=True)),
                ('added_tstamp', models.DateTimeField(auto_now=True, null=True)),
                ('tea_lca_tool_alias', models.CharField(blank=True, max_length=200, null=True)),
                ('bp_exp', models.FloatField(blank=True, null=True)),
                ('mp_exp', models.FloatField(blank=True, null=True)),
                ('fp_exp', models.FloatField(blank=True, null=True)),
                ('ysi_exp', models.FloatField(blank=True, null=True)),
                ('cn_exp', models.FloatField(blank=True, null=True)),
                ('dcn_exp', models.FloatField(blank=True, null=True)),
                ('bp_pred', models.FloatField(blank=True, null=True)),
                ('mp_pred', models.FloatField(blank=True, null=True)),
                ('fp_pred', models.FloatField(blank=True, null=True)),
                ('ysi_pred', models.FloatField(blank=True, null=True)),
                ('cn_pred', models.FloatField(blank=True, null=True)),
                ('dcn_pred', models.FloatField(blank=True, null=True)),
                ('bp_pred_perc_err', models.FloatField(blank=True, default=4.7, null=True)),
                ('mp_pred_perc_err', models.FloatField(blank=True, default=7.7, null=True)),
                ('fp_pred_perc_err', models.FloatField(blank=True, default=5.2, null=True)),
                ('ysi_pred_perc_err', models.FloatField(blank=True, default=13.0, null=True)),
                ('cn_pred_perc_err', models.FloatField(blank=True, default=21.0, null=True)),
                ('dcn_pred_perc_err', models.FloatField(blank=True, default=39.3, null=True)),
                ('_struct_img', models.FilePathField(blank=True, null=True, verbose_name='chem/static/chem/img/structs')),
            ],
        ),
        migrations.CreateModel(
            name='ChemicalSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('smiles', models.CharField(blank=True, max_length=500, null=True)),
                ('formula', models.CharField(blank=True, max_length=500, null=True)),
                ('inchi', models.CharField(blank=True, max_length=500, null=True)),
                ('iupac', models.CharField(blank=True, max_length=500, null=True)),
                ('cas', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_exp', models.FloatField(blank=True, null=True)),
                ('mp_exp', models.FloatField(blank=True, null=True)),
                ('fp_exp', models.FloatField(blank=True, null=True)),
                ('ysi_exp', models.FloatField(blank=True, null=True)),
                ('cn_exp', models.FloatField(blank=True, null=True)),
                ('dcn_exp', models.FloatField(blank=True, null=True)),
                ('bp_src', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('bp_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('mp_src', models.CharField(blank=True, max_length=500, null=True)),
                ('mp_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('mp_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('fp_src', models.CharField(blank=True, max_length=500, null=True)),
                ('fp_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('fp_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('cn_src', models.CharField(blank=True, max_length=500, null=True)),
                ('cn_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('cn_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('dcn_src', models.CharField(blank=True, max_length=500, null=True)),
                ('dcn_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('dcn_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('ysi_src', models.CharField(blank=True, max_length=500, null=True)),
                ('ysi_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('ysi_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_x_val', models.FloatField(blank=True, null=True)),
                ('dens_x_temp', models.FloatField(blank=True, null=True)),
                ('dens_x_src', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_x_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_x_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_y_val', models.FloatField(blank=True, null=True)),
                ('dens_y_temp', models.FloatField(blank=True, null=True)),
                ('dens_y_src', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_y_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_y_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_z_val', models.FloatField(blank=True, null=True)),
                ('dens_z_temp', models.FloatField(blank=True, null=True)),
                ('dens_z_src', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_z_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('dens_z_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_x_val', models.FloatField(blank=True, null=True)),
                ('visc_x_temp', models.FloatField(blank=True, null=True)),
                ('visc_x_src', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_x_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_x_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_y_val', models.FloatField(blank=True, null=True)),
                ('visc_y_temp', models.FloatField(blank=True, null=True)),
                ('visc_y_src', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_y_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_y_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_z_val', models.FloatField(blank=True, null=True)),
                ('visc_z_temp', models.FloatField(blank=True, null=True)),
                ('visc_z_src', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_z_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('visc_z_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('net_ht_cmbst_val', models.FloatField(blank=True, null=True)),
                ('net_ht_cmbst_src', models.CharField(blank=True, max_length=500, null=True)),
                ('net_ht_cmbst_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('net_ht_cmbst_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_1_name', models.FloatField(blank=True, null=True)),
                ('oth_prop_1_val', models.FloatField(blank=True, null=True)),
                ('oth_prop_1_src', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_1_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_1_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_3_name', models.FloatField(blank=True, null=True)),
                ('oth_prop_3_val', models.FloatField(blank=True, null=True)),
                ('oth_prop_3_src', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_3_tst', models.CharField(blank=True, max_length=500, null=True)),
                ('oth_prop_3_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('contrib_name', models.CharField(blank=True, max_length=500, null=True)),
                ('contrib_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contrib_affil', models.CharField(blank=True, max_length=500, null=True)),
                ('comments', models.CharField(blank=True, max_length=1000, null=True)),
                ('csv_submission', models.FileField(blank=True, null=True, upload_to='chem_csv_submissions')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyEstimator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=300, unique=True)),
                ('prop', models.CharField(max_length=500)),
                ('added_tstamp', models.DateTimeField(auto_now=True, null=True)),
                ('feat_names', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('features', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None), blank=True, null=True, size=None)),
                ('labels', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None)),
                ('ids', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None)),
                ('train_fit_serial_mod_fn', models.FilePathField(verbose_name='filestore/ml_models')),
                ('full_fit_serial_mod_fn', models.FilePathField(verbose_name='filestore/ml_models')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('link', models.URLField(blank=True, default='#', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChemicalSynonym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('chem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='synonyms', to='chem.Chemical')),
            ],
        ),
        migrations.AddField(
            model_name='chemical',
            name='bp_estimator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bp_estimator', to='chem.PropertyEstimator'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='bp_exp_srcs',
            field=models.ManyToManyField(blank=True, related_name='bp_exp_srcs', to='chem.Source'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='cn_estimator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cn_estimator', to='chem.PropertyEstimator'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='cn_exp_srcs',
            field=models.ManyToManyField(blank=True, related_name='cn_exp_srcs', to='chem.Source'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='dcn_estimator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dcn_estimator', to='chem.PropertyEstimator'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='dcn_exp_srcs',
            field=models.ManyToManyField(blank=True, related_name='dcn_exp_srcs', to='chem.Source'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='fp_estimator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fp_estimator', to='chem.PropertyEstimator'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='fp_exp_srcs',
            field=models.ManyToManyField(blank=True, related_name='fp_exp_srcs', to='chem.Source'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='mp_estimator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mp_estimator', to='chem.PropertyEstimator'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='mp_exp_srcs',
            field=models.ManyToManyField(blank=True, related_name='mp_exp_srcs', to='chem.Source'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='ysi_estimator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ysi_estimator', to='chem.PropertyEstimator'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='ysi_exp_srcs',
            field=models.ManyToManyField(blank=True, related_name='ysi_exp_srcs', to='chem.Source'),
        ),
        migrations.CreateModel(
            name='BlendComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fraction', models.FloatField()),
                ('chem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chem.Chemical')),
            ],
        ),
    ]
