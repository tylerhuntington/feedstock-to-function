# Generated by Django 3.0.3 on 2020-09-30 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chem', '0020_auto_20200930_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blendsubmission',
            name='cas',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
