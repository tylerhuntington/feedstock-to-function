# Generated by Django 3.0.3 on 2020-10-02 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chem', '0025_auto_20201001_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='chemical',
            name='added_tstamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='chemical',
            name='tea_lca_tool_alias',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
