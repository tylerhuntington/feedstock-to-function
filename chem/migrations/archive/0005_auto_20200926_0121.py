# Generated by Django 3.0.3 on 2020-09-26 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chem', '0004_auto_20200926_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='chemical',
            name='bp_pred_err',
            field=models.FloatField(blank=True, default=4.7, null=True),
        ),
        migrations.AddField(
            model_name='chemical',
            name='cn_pred_err',
            field=models.FloatField(blank=True, default=21.0, null=True),
        ),
        migrations.AddField(
            model_name='chemical',
            name='dcn_pred_err',
            field=models.FloatField(blank=True, default=39.3, null=True),
        ),
        migrations.AddField(
            model_name='chemical',
            name='fp_pred_err',
            field=models.FloatField(blank=True, default=5.2, null=True),
        ),
        migrations.AddField(
            model_name='chemical',
            name='mp_pred_err',
            field=models.FloatField(blank=True, default=7.7, null=True),
        ),
        migrations.AddField(
            model_name='chemical',
            name='ysi_pred_err',
            field=models.FloatField(blank=True, default=13.0, null=True),
        ),
    ]
