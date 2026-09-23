import pandas as pd
import numpy as np  
def load_file(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading file , {e}")
        print("File path must contain valid file. (i.e: zameen-property-data.csv)")
        return
    print(f"Initial DataSet shape: {df.shape[0]} rows , and {df.shape[1]} columns.")
    return df

def clean_csv_data(df): 
    df.columns = df.columns.str.strip().str.lower()
    purpose_col = "purpose" if "purpose" in df.columns else "property_purpose"
    type_col = "property_type" if "property_type" in df.columns else ("type" if "type" in df.columns else None)
    area = "area" if "area" in df.columns else "size"
    price = "price" if "price" in df.columns else "property_price"
    df[purpose_col]=df[purpose_col].astype(str).str.strip().str.lower()
    df[type_col]=df[type_col].astype(str).str.strip().str.lower()
    filtered_df = df[(df[purpose_col]=="for sale")&(df[type_col]=="house")].copy()
    clean_df = filtered_df[[area,price]]
    return clean_df
    
def convert_to_marla(text_value):

    if pd.isna(text_value):
        return None
    
    text_clean = str(text_value).lower().strip()
    
    parts = text_clean.split()
    if len(parts) == 0:
        return None
        
    try:
        number = float(parts[0])
    except ValueError:
        return None

    if 'kanal' in text_clean:
        return number * 20
    else:
        return number

print("Conversion function created successfully!")



