"""
Utility classes and functions for the chem module
"""
import joblib
import pandas as pd
import numpy as np
import sklearn
import xgboost
import mordred
import rdkit.Chem as Chem
import rdkit.Chem.AllChem as AllChem
import argparse

from rdkit.Chem import MolFromSmiles, MolToSmiles
from mordred import Calculator
from mordred import descriptors as mordred_descriptors

def generate_all_descriptors(smiles):
    calc = Calculator(mordred_descriptors)
    mols =[Chem.AddHs(MolFromSmiles(i)) for i in smiles]
    for mol in mols:
        AllChem.EmbedMolecule(mol,randomSeed=1)
    descriptors = calc.pandas([mol for mol in mols])
    descriptors['og_smiles'] = [smiles]
    descriptors['smiles'] = [MolToSmiles(MolFromSmiles(i)) for i in smiles]
    return descriptors

def get_prediction(descriptors,property,model,property_descr_dict):
    X = descriptors[[c for c in property_descr_dict[property]]]
    preds = model.predict(X)
    all_trees_df=pd.DataFrame()
    for tree in model[0].estimators_:
        tree_pred = pd.Series(tree.predict(X))
        all_trees_df = pd.concat([all_trees_df,tree_pred],axis=1)
    final_quants_preds=pd.DataFrame()
    final_quants_preds['smiles'] = [i for i in descriptors['smiles']]
    final_quants_preds['og_smiles'] = [i for i in descriptors['og_smiles']]
    final_quants_preds['pred'] = [i for i in preds]
    for q in [0.1,0.9]:
        quants = all_trees_df.quantile(q=q,axis=1)
        final_quants_preds = pd.concat([final_quants_preds,quants],axis=1,sort=False)
    return final_quants_preds

def pred_props_and_errs_of_smiles(smiles, path_to_mods, path_to_descr):
    descriptors = generate_all_descriptors(smiles)
    properties=['bp_k','fp_k','hoc','mp_k','ysi']
    models=[joblib.load(path_to_mods+prop+'.joblib') for prop in properties]
    property_descr_dict={}
    for prop in properties:
        descr_file = open(path_to_descr+prop+'_descriptors.txt','r')
        descs = descr_file.read()
        property_descr_dict[prop] =[i.replace("'","").replace(' ',"") for i in descs.split(',')]

    preds_and_errors = [get_prediction(descriptors,property,model,property_descr_dict) for property,model in zip(properties,models)]
    results_dict = {i: j for i, j in zip(smiles, [{} for i in range(len(smiles))])}
    for num in range(len(smiles)):
        results_dict[smiles[num]] = {i + '_pred': j.values[0] for i, j in zip(properties, [df.loc[df[df['smiles'] == smiles[num]].index, 'pred'] for df in preds_and_errors])}
        results_dict[smiles[num]].update({i + '_lower': j.values[0] for i, j in zip(properties, [df.loc[df[df['smiles'] == smiles[num]].index, 0.1] for df in preds_and_errors])})
        results_dict[smiles[num]].update({i + '_upper': j.values[0] for i, j in zip(properties, [df.loc[df[df['smiles'] == smiles[num]].index, 0.9] for df in preds_and_errors])})

    return results_dict

def kelvin_to_celsius(val):
    """
    Convert temperature value in Kelvin to Celsius.
    :param val:
    :return:
    """
    return val - 273.15

def celsius_to_kelvin(val):
    """
    Convert temperature value in Celsius to Kelvin.
    :param val:
    :return:
    """
    return  val + 273.15



