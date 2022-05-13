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
from chem import BLEND_DATA_CSV_FP, BLEND_DATA_JSON_FP


from chem import (
    PROP_ESTIMATOR_MODELS_DIR,
    PROP_DESCRIPTORS_DIR,
    INIT_FIXTURES_DIR,
    RAW_DATA_DIR,
    PROD_DATA_DIR,
    PRED_PROP_CODES,
    CHEMS_IN_TEA_LCA_APP
)

def blend_csv_to_json(in_csv_fp, out_json_fp):
    df = pd.read_csv(in_csv_fp)
    df.index = df['name']
    df.drop('name', axis=1, inplace=True)
    data = df.to_dict(orient='index')
    with open(out_json_fp, 'w') as f:
        sjson.dump(data, f, ignore_nan=True)



def run(*args):
    blend_csv_to_json(
        in_csv_fp=BLEND_DATA_CSV_FP,
        out_json_fp=BLEND_DATA_JSON_FP
    )
