python manage.py runscript blend_data_csv_to_json \
    --script-args " \
    " \
&&
    cp chem/data/prod/blend_data.json frontend/src/
# OTHER ARGS:
