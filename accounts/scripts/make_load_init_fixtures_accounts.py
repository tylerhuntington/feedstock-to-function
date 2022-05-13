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

from chem import (
    PROP_ESTIMATOR_MODELS_DIR,
    PROP_DESCRIPTORS_DIR,
    INIT_FIXTURES_DIR,
    RAW_DATA_DIR,
    PROD_DATA_DIR,
    PRED_PROP_CODES
)

from chem.models import PropertyEstimator, Chemical, Source

# config logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(name)s] %(message)s', datefmt='%m-%d %H:%M'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def load_socialaccount_fixtures():
    call_command('loaddata', 'accounts/init_fixtures/socialaccount.json')


def run(*args):
    load_socialaccount_fixtures()

