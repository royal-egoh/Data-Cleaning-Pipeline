from app.pipeline.extractor import *
from app.pipeline.validator import *
from app.pipeline.cleaner import *
from app.pipeline.transformer import *
from app.models.dataset import Dataset
import time
# from app.routers.pipeline import 
from app.workers.pipeline_worker import data_pipeline
# app\test_files\people-1000000.csv
file_path = "app/test_files/people-100.csv"

print(data_pipeline.delay(file_path, "ab671256-8a59-40a9-8d12-d58c7a4ebfa2"))

# start_ext = time.time()

# df = extract_file(file_path)
# end_ext = time.time()
# elapsed_ext = end_ext-start_ext
# print(f"The elapsed function: {elapsed_ext:.4f}")

# start_val = time.time()
# validate_f = validate(df)
# end_val = time.time()
# elapsed_val = end_val-start_val
# print(f"The validate function: {elapsed_val:.4f}")

# # startcl = time.time()
# # cleaner = clean(df, validate_f)
# # endcl = time.time()
# # elapsedcl = endcl-startcl
# # print(f"The clean function: {elapsedcl:.4f}")

# # 1. Drop Duplicates
# start_dup = time.time()
# df = drop_duplicates(df, validate_f)
# end_dup = time.time()
# print(f"⏱️ Drop Duplicates:    {end_dup - start_dup:.4f} seconds")

# # 2. Drop Invalid Rows
# start_inv = time.time()
# df = drop_invaldid_rows(df, validate_f)
# end_inv = time.time()
# print(f"⏱️ Drop Invalid Rows:  {end_inv - start_inv:.4f} seconds")

# # 3. Fill Nulls
# start_null = time.time()
# df = fill_nulls(df, validate_f)
# end_null = time.time()
# print(f"⏱️ Fill Nulls Cells:  {end_null - start_null:.4f} seconds")

# # 4. Standardise Date
# start_date = time.time()
# df = standardise_date(df)
# end_date = time.time()
# print(f"⏱️ Standardise Date:  {end_date - start_date:.4f} seconds")

# # 5. Standardise Sex
# start_sex = time.time()
# df = standardise_sex(df)
# end_sex = time.time()
# print(f"⏱️ Standardise Sex:   {end_sex - start_sex:.4f} seconds")

# # 6. Standardise Phone
# start_phone = time.time()
# df = standardise_phone(df)
# end_phone = time.time()
# print(f"⏱️ Standardise Phone: {end_phone - start_phone:.4f} seconds")
# startt = time.time()
# transf = transform(df)
# endt = time.time()
# elapsedt = endt-startt
# print(f"The transfrm function: {elapsedt:.4f}")
# pd.set_option('display.max_rows', None)
# loader = load(transf, "44f79a59-9223-48a0-8fd9-bbd5584bdcb0")
# print(df["Phone"])



# # pd.set_option('display.max_columns', None)
# # loader = load(transf, dataset_id=1)
# print(transf)
