# Zameen.com Dataset Cleaning Script
# This script filters data for Houses for Sale, cleans and parses the Area column into Marlas, and isolates Price and Area.

import pandas as pd
import numpy as np

def clean_zameen_data(file_path, output_path="cleaned_zameen_data.csv"):
    print("🔄 Loading dataset...")
    # Load dataset (supports both csv and parquet depending on your file)
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        print("💡 Please make sure the file path is correct and includes the extension (e.g., 'zameen_dataset.csv').")
        return

    print(f"📋 Initial dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")

    # Step 1: Standardize column names to lowercase to prevent typos
    df.columns = df.columns.str.strip().str.lower()
    
    # Identify key columns dynamically or fallback
    purpose_col = 'purpose' if 'purpose' in df.columns else 'property_purpose'
    type_col = 'property_type' if 'property_type' in df.columns else ('type' if 'type' in df.columns else None)
    price_col = 'price'
    area_col = 'area'
    
    if not type_col or area_col not in df.columns or price_col not in df.columns:
        print(f"❌ Missing critical columns. Found columns: {list(df.columns)}")
        print("💡 Please rename your columns to 'purpose', 'property_type' (or 'type'), 'price', and 'area'.")
        return

    # Step 2: Keep only rows where purpose is 'For Sale' and property_type is 'House'
    print("🧹 Filtering rows for Purpose='For Sale' and Type='House'...")
    
    # Clean text to ensure exact matches
    df[purpose_col] = df[purpose_col].astype(str).str.strip().str.lower()
    df[type_col] = df[type_col].astype(str).str.strip().str.lower()
    
    filtered_df = df[(df[purpose_col] == 'for sale') & (df[type_col] == 'house')].copy()
    print(f"📉 Rows remaining after filtering: {filtered_df.shape[0]}")

    # Step 3: Keep only Price and Area columns
    filtered_df = filtered_df[[price_col, area_col]]

    # Step 4: Check and clean the Area column
    print("🔢 Checking and parsing the 'area' column...")
    
    # Case A: If Area is a string/text datatype
    if filtered_df[area_col].dtype == 'object' or isinstance(filtered_df[area_col].iloc[0], str):
        print("📝 'area' detected as TEXT. Parsing text units...")
        
        # Create helper columns to extract number and unit
        # Example format: "5 Marla" or "1 Kanal"
        filtered_df['area_lower'] = filtered_df[area_col].astype(str).str.strip().str.lower()
        
        # Extract numeric part using regex
        filtered_df['area_num'] = filtered_df['area_lower'].str.extract(r'([0-9\.]+)').astype(float)
        
        # Function to standardize to Marla
        def convert_to_marla(row):
            text = str(row['area_lower'])
            val = row['area_num']
            if pd.isna(val):
                return np.nan
            if 'kanal' in text:
                return val * 20.0  # 1 Kanal = 20 Marla
            return val  # Default assuming Marla or already handled
            
        filtered_df['area_marla'] = filtered_df.apply(convert_to_marla, axis=1)
        filtered_df['area'] = filtered_df['area_marla']
        
    else:
        # Case B: If Area is already numeric
        print("🔢 'area' detected as NUMERIC. Checking scale...")
        sample_mean = filtered_df[area_col].mean()
        if sample_mean > 500:
            print("💡 Area values are high (e.g. thousands). Assuming unit is SQUARE FEET.")
            print("🔄 Converting Square Feet to Marla (Dividing by 225)...")
            filtered_df['area'] = filtered_df[area_col] / 225.0  # Standard Pakistani Marla = 225 sqft
        else:
            print("💡 Area values are low (e.g. 5, 10, 20). Assuming unit is already MARLA.")

    # Drop intermediate columns if any were created
    final_df = filtered_df[[price_col, 'area']].dropna()
    
    # Rename columns explicitly for modeling
    final_df.columns = ['price_pkr', 'area_marla']
    
    print(f"✅ Cleaning complete! Final dataset shape: {final_df.shape[0]} rows, 2 columns.")
    print(final_df.head())
    
    # Save the cleaned file
    final_df.to_csv(output_path, index=False)
    print(f"💾 Cleaned file saved successfully to: '{output_path}'")

if __name__ == "__main__":
    # Change 'dataset.csv' to the actual name of your downloaded Zameen.com file
    # Example: clean_zameen_data("zameen_properties.csv")
    print("🚀 Script ready. To run this, call: clean_zameen_data('your_filename.csv')")