# Generated by Django 3.1.1 on 2021-12-02 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chem', '0007_auto_20210716_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='chemical',
            name='hoc_exp',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chemical',
            name='bp_pred_perc_err',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chemical',
            name='cn_pred_perc_err',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chemical',
            name='dcn_pred_perc_err',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chemical',
            name='fp_pred_perc_err',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chemical',
            name='mp_pred_perc_err',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chemical',
            name='ysi_pred_perc_err',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
