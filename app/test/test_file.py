from app.pipeline.extractor import *
from app.pipeline.validator import *
from app.pipeline.cleaner import *
from app.pipeline.transformer import *
from app.models.dataset import Dataset

# app\test_files\people-1000000.csv
file_path = "app/test_files/people-100.csv"
df = extract_file(file_path)
validate_f = validate(df)
cleaner = clean(df, validate_f)
transf = transform(cleaner)

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
loader = load(transf, dataset_id=1)
# print(transf)
