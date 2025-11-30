# load_csv.py (improved)
import os
import sys
import django
import pandas as pd

# --- Django environment setup ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)  # ensure relative paths are from project root
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate_chatbot.settings')
django.setup()

# import models AFTER django.setup()
from analysis.models import RealEstateData

# --- helper utils ---
def normalize_cols(df):
    # lower-case, strip and replace multiple spaces with single space
    df = df.rename(columns={c: c.strip().lower() for c in df.columns})
    return df

def read_table(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.xls', '.xlsx'):
        # requires openpyxl installed
        return pd.read_excel(path, engine='openpyxl')
    elif ext == '.csv':
        # try default encoding, fallback to latin1 if unicode errors occur
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding='latin1')
    else:
        raise ValueError(f'Unsupported file extension: {ext}')

def load_data(file_path):
    if not os.path.exists(file_path):
        print(f"ERROR: file not found -> {file_path}")
        sys.exit(1)

    print("Reading file:", file_path)
    df = read_table(file_path)
    print("Rows:", len(df))
    df = normalize_cols(df)
    print("Columns found:", list(df.columns)[:50])
    print("Sample rows:\n", df.head().to_string(index=False))

    # Clear existing data (optional)
    RealEstateData.objects.all().delete()

    # column mapping: dataframe_col_name -> model_field_name
    col_map = {
        'final location': 'final_location',
        'year': 'year',
        'city': 'city',
        'loc_lat': 'loc_lat',
        'loc_lng': 'loc_lng',
        'total_sales - igr': 'total_sales_igr',
        'total sold - igr': 'total_sold_igr',
        'flat_sold - igr': 'flat_sold_igr',
        'office_sold - igr': 'office_sold_igr',
        'others_sold - igr': 'others_sold_igr',
        'shop_sold - igr': 'shop_sold_igr',
        'commercial_sold - igr': 'commercial_sold_igr',
        'other_sold - igr': 'other_sold_igr',
        'residential_sold - igr': 'residential_sold_igr',
        'flat - weighted average rate': 'flat_weighted_avg_rate',
        'office - weighted average rate': 'office_weighted_avg_rate',
        'others - weighted average rate': 'others_weighted_avg_rate',
        'shop - weighted average rate': 'shop_weighted_avg_rate',
        'flat - most prevailing rate - range': 'flat_prevailing_rate_range',
        'office - most prevailing rate - range': 'office_prevailing_rate_range',
        'others - most prevailing rate - range': 'others_prevailing_rate_range',
        'shop - most prevailing rate - range': 'shop_prevailing_rate_range',
        'total units': 'total_units',
        'total carpet area supplied (sqft)': 'total_carpet_area_supplied',
        'flat total': 'flat_total',
        'shop total': 'shop_total',
        'office total': 'office_total',
        'others total': 'others_total'
    }

    data_objects = []
    # use .get on df row with default None or 0 where suitable
    for _, row in df.iterrows():
        kwargs = {}
        for df_col, model_field in col_map.items():
            # use None if not present or NaN -> allow model defaults to handle if set
            if df_col in row.index:
                val = row[df_col]
                # optional: replace nan with None
                if pd.isna(val):
                    val = None
            else:
                val = None
            kwargs[model_field] = val

        # Example: if model expects numeric fields, you might want to cast types here
        data_objects.append(RealEstateData(**kwargs))

    if data_objects:
        RealEstateData.objects.bulk_create(data_objects)
        print(f"Successfully created {len(data_objects)} records.")
    else:
        print("No records to create.")

if __name__ == '__main__':
    # change this to the actual filename you have
    # e.g. 'Sample_data.xlsx' or 'Sample_data.csv' (must be in project root or provide absolute path)
    FILE = 'Sample_data.xlsx'
    load_data(FILE)
