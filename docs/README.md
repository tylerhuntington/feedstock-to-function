# Documentation for FTF Django Site


### Abbreviations Defined

#### Properties
[//]: # (TODO: populate the rest of this list based on models.py files)
`bp`: boiling point
`mp`: melting point
`cn`: cetane number
`dcn`: derived cetane number
`fp`: flash point
`fzp`: freezing point
`ysi`: yield sooting index
`dens`: density
`naph`: naphthalene percentage by volume
`lbrc`: lubricity
`net_ht_cmbst`: net heat of combustion
`arom`: aromatics

#### Common Measurement Annotations
`exp`: experimentally determined value
`pred`: predicted value
`wt`: weight
`ht`: heat
`perc`: percentage
`tst`: test


#### Elements
`hydgn`: hydrogen


#### Workflows

##### Updating Property Prediction Models
- Replace `.joblib` files in `chem/estimators/` directory with new serialized models following same naming convention of existing `.joblib` files.

- Replace `.txt` files in `chem/data/prod/descriptors/` directory with new descriptors following same naming convention of existing `.joblib` files.

- Add batch updating CSV for existing Chemical objects to `chem/data/prod/` directory following naming pattern: `chemical_objects_updates_{MM_DD_YY}.csv`.

- Update `CHEMICAL_OBJECTS_UPDATE_CSV_FP` in `chem/__init__.py` with name of newly added batch update csv.

- Run `./scripts/update_or_create_chemical_objects_from_csv.sh`
