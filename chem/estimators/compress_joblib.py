import joblib

fp = 'mp_k_uncompressed.joblib'

mod = joblib.load(fp)

joblib.dump(mod, 'mp_k_compress1.joblib', compress=1)

print(mod)
