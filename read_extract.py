import pandas as pd
import os

def clean_column_names(df):
    """
    Rename columns to ensure each column has a meaningful, unique name.
    'Unnamed' columns are renamed sequentially as 'Column_X' where X is the column index.
    """
    new_column_names = []
    for i, col in enumerate(df.columns):
        col_name = str(col).strip() if isinstance(col, str) else f"Column_{i}"
        if 'Unnamed' in col_name or col_name == '':
            new_column_names.append(f"Column_{i}")
        else:
            new_column_names.append(col_name)
    df.columns = new_column_names
    return df

def read_and_clean_excel(file_path):
    """
    Reads and cleans the data from an Excel file, returning a dictionary with sheet names as keys.
    """
    print(f"Reading Excel file: {file_path}")
    file_extension = os.path.splitext(file_path)[1].lower()
    engine = 'openpyxl' if file_extension == '.xlsx' else 'xlrd'
    
    try:
        excel_file = pd.ExcelFile(file_path, engine=engine)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}
    
    all_data = {}
    
    for sheet_name in excel_file.sheet_names:
        print(f"Processing sheet: {sheet_name}")
        df = excel_file.parse(sheet_name)
        df = clean_column_names(df)
        df = df.fillna('')
        all_data[sheet_name] = df
    print(all_data)
    
    return all_data

