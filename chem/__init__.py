import os
import json
from pathlib import Path, PosixPath, Path
from django.conf import settings
from fuzzywuzzy import fuzz

APP_NAME = 'chem'

# App specific globals
# universal abbreviations for properties predicted by the tool
PRED_PROP_CODES = ['mp', 'bp', 'fp', 'cn', 'dcn', 'ysi']

# search settings
MIN_FUZZY_SEARCH_SCORE = -1
MAX_FUZZY_SEARCH_RESULTS = 30
FUZZY_SEARCH_SCORER = fuzz.token_sort_ratio

# TEA LCA integrations settings
CHEMS_IN_TEA_LCA_APP = {
    'CCO': 'Ethanol',
    'C=C(C)C1CC=C(C)CC1': 'Limonene',
    'CC1CCC(CC1)C(C)CCCC(C)C': 'Bisabolane',
    'CC1=CCC(=C(C)CCC=C(C)C)CC1': 'Bisabolene',
}

# Paths
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
MIGRATIONS_DIR = Path(BASE_DIR, 'migrations')
INIT_FIXTURES_DIR = Path(BASE_DIR, 'init_fixtures')
DATA_DIR = Path(BASE_DIR, 'data')
RAW_DATA_DIR = Path(DATA_DIR, 'raw')
PROD_DATA_DIR = Path(DATA_DIR, 'prod')
PROP_DESCRIPTORS_DIR = Path(PROD_DATA_DIR, 'descriptors')
PROP_ESTIMATOR_MODELS_DIR = Path(settings.FILESTORE_ROOT, 'ml_models')
CHEM_STATIC_DIR = Path('chem', 'static', 'chem')
CHEM_STRUCT_IMG_DIR = Path(CHEM_STATIC_DIR, 'img', 'structs')
CHEM_UPLOAD_TEMPLATES_DIR = Path(CHEM_STATIC_DIR, 'upload_templates')
CHEM_SUBMISSION_TEMPLATE_FP = Path(
    CHEM_UPLOAD_TEMPLATES_DIR, 'chem_submission_template.csv'
)
BLEND_SUBMISSION_TEMPLATE_FP = Path(
    CHEM_UPLOAD_TEMPLATES_DIR, 'blend_submission_template.csv'
)

BLEND_DATA_CSV_FP = Path(RAW_DATA_DIR, 'blend_data.csv')
BLEND_DATA_JSON_FP = Path(PROD_DATA_DIR, 'blend_data.json')

CHEMICAL_OBJECTS_UPDATE_CSV_FP = Path(
    PROD_DATA_DIR,
    'chemical_objects_updates_11_15_21.csv'
)

ESTIMATORS_JOBLIB_DIR = Path(BASE_DIR, 'estimators')
DESCRIPTORS_DIR = Path(PROD_DATA_DIR, 'descriptors')

with open(CHEM_SUBMISSION_TEMPLATE_FP, 'r') as f:
    CHEM_SUBMISSION_TEMPLATE = f.read()

with open(BLEND_SUBMISSION_TEMPLATE_FP, 'r') as f:
    BLEND_SUBMISSION_TEMPLATE = f.read()

MODEL_INIT_FIXTURES_FPS = {
    'PropertyEstimator': Path(INIT_FIXTURES_DIR, 'PropertyEstimator.json'),
    'Chemical': Path(INIT_FIXTURES_DIR, 'Chemical.json'),
}


APP_INIT_FIXTURES = {}
for classname, fixtures_fp in MODEL_INIT_FIXTURES_FPS.items():
    if fixtures_fp.is_file():
        with open(fixtures_fp, 'r') as f:
            APP_INIT_FIXTURES[classname] = json.load(f)
