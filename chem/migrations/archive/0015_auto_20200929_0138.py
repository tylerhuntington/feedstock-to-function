# Generated by Django 3.0.3 on 2020-09-29 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chem', '0014_auto_20200929_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chemical',
            name='_struct_img',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
