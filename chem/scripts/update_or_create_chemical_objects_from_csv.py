"""
Makes initial DB fixtures (JSON) for models in the chem app
"""

import os
from pathlib import PurePath, Path
import json
import simplejson as sjson
import logging
import pandas as pd
import numpy as np
from django.core.management import call_command
from chem import CHEMICAL_OBJECTS_UPDATE_CSV_FP
from chem.models import Chemical


def update_or_create_chemical_objects(in_csv_fp):
    df = pd.read_csv(in_csv_fp)
    for index, row in df.iterrows():
        smiles = row['smiles']
        qs = Chemical.objects.filter(smiles=smiles)
        if len(qs) > 1:
            raise Exception(f'More than one chemical found for: {smiles}')
        elif len(qs) == 0:
            chem = Chemical(smiles=smiles)
        else:
            chem = qs[0]


        # Set experimental property attributes
        if not np.isnan(row['bp_c_exp']):
            chem.bp_exp = row['bp_c_exp']
        if not np.isnan(row['mp_c_exp']):
            chem.mp_exp = row['mp_c_exp']
        if not np.isnan(row['fp_c_exp']):
            chem.fp_exp = row['fp_c_exp']
        if not np.isnan(row['hoc_exp']):
            chem.hoc_exp = row['hoc_exp']
        if not np.isnan(row['ysi_exp']):
            chem.ysi_exp = row['ysi_exp']

        # Set predicted property attributes
        chem.bp_pred = row['bp_c_pred']
        chem.bp_pred_err_low = row['bp_c_lower']
        chem.bp_pred_err_up = row['bp_c_upper']
        chem.mp_pred = row['mp_c_pred']
        chem.mp_pred_err_low = row['mp_c_lower']
        chem.mp_pred_err_up = row['mp_c_upper']
        chem.fp_pred = row['fp_c_pred']
        chem.fp_pred_err_low = row['fp_c_lower']
        chem.fp_pred_err_up = row['fp_c_upper']
        chem.ysi_pred = row['ysi_pred']
        chem.ysi_pred_err_low = row['ysi_lower']
        chem.ysi_pred_err_up = row['ysi_upper']
        chem.hoc_pred = row['hoc_pred']
        chem.hoc_pred_err_low = row['hoc_lower']
        chem.hoc_pred_err_up = row['hoc_upper']

        chem.save()

def run(*args):
    update_or_create_chemical_objects(
        in_csv_fp=CHEMICAL_OBJECTS_UPDATE_CSV_FP
    )
