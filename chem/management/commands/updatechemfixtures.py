import secrets
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from django.conf import settings
from django.core.mail import EmailMessage
import logging
import pandas as pd
import numpy as np
from django.core.management import call_command
from chem import CHEMICAL_OBJECTS_UPDATE_CSV_FP
from chem.models import Chemical

# config logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(name)s] %(message)s', datefmt='%m-%d %H:%M'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):

    def handle(self, *args, **options):
        in_csv_fp = CHEMICAL_OBJECTS_UPDATE_CSV_FP
        df = pd.read_csv(in_csv_fp)
        logger.info(f"Updating/creating {df.shape[0]} Chemical objects...")
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
        logger.info(f"Updated/created {df.shape[0]} Chemical objects")
