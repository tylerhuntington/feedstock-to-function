"""
Preprocesses data precursors required for initial fixtures for models in
the chem app
"""


from pathlib import Path
import numpy as np
import logging
import pandas as pd

from chem import (
    PROP_DESCRIPTORS_DIR,
    RAW_DATA_DIR,
    PROD_DATA_DIR
)

from chem.models import PropertyEstimator


# config logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(name)s] %(message)s', datefmt='%m-%d %H:%M'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def preprocess_init_fixture_data_chemical():
    """
    Preprocesses data precursors required for initial fixtures for the
    for Chemical class
    :return:
    """

    # start with chemical names dataset
    chems = pd.read_csv(Path(RAW_DATA_DIR, 'moleculenames.csv'))
    chems = chems.drop('synonyms_reduced', axis=1)

    # load sources dataset and merge to chems
    srcs = pd.read_csv(Path(RAW_DATA_DIR, 'sources_df.csv'))
    chems = chems.merge(srcs, on='smiles', how='left')

    props = ['mp', 'bp', 'fp', 'cn', 'dcn', 'ysi']

    # load full descriptor dataset
    full_desc_df = pd.read_csv(Path(PROP_DESCRIPTORS_DIR, 'full_set.csv'))

    # make predictions for predicted properties
    for p in props:
        # get the estimator
        est = PropertyEstimator.objects.filter(prop=p).latest('added_tstamp')
        feat_cols = [c.replace('mordred_desc_', '') for c in est.feat_names]
        pred_df = full_desc_df[feat_cols + ['smiles']]
        pred_df.loc[:, feat_cols] = pred_df.loc[:, feat_cols].replace(
            to_replace=r'.*[a-zA-Z].*', value=np.nan, regex=True
        )
        pred_df = pred_df.dropna()
        feats = pred_df[feat_cols].values
        preds = est.mod_fit_to_full_set.predict(feats)
        preds_col = f'{p}_pred'
        pred_df[preds_col] = preds
        pred_df = pred_df[[preds_col, 'smiles']]
        chems = chems.merge(pred_df, on='smiles', how='left')

    chems.to_csv(Path(PROD_DATA_DIR, 'chemical_fixtures_data.csv'))


def preprocess_init_fixture_data_chemicalsynonym():
    """
    Preprocesses data precursors required for initial fixtures for the
    for Chemical class
    :return:
    """

    # start with chemical names dataset
    df = pd.read_csv(Path(RAW_DATA_DIR, 'molecule_reduced_synonyms.csv'))
    df = df.drop_duplicates()
    df.to_csv(Path(PROD_DATA_DIR, 'chemicalsynonyms_fixture_data.csv'))


def run(*args):

    # preprocess_init_fixture_data_chemical()
    preprocess_init_fixture_data_chemicalsynonym()


