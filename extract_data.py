import os
import glob
import pandas as pd
import json

# Function to clean up the data
def clean_data(df):
    # Drop any entirely empty rows or columns
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)

    # Remove leading/trailing whitespace from column headers
    df.columns = df.columns.str.strip()

    # Remove leading/trailing whitespace from data in each column
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Handle missing values (optional)
    # Example: Replace NaN with 'N/A' as a placeholder
    df = df.fillna('N/A')

    # Remove any columns like 'Unnamed' that may appear due to misaligned headers
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    return df

# Function to read and process CSV or Excel files
def read_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.csv':
        # Read CSV file using pandas
        print(f"Reading CSV file: {file_path}")
        df = pd.read_csv(file_path)
        df = clean_data(df)
        print(df)
    
    elif file_extension == '.xlsx' or file_extension == '.xls':
        # Read Excel file using pandas (with sheet name as None to read all sheets)
        print(f"Reading Excel file: {file_path}")
        df = pd.read_excel(file_path, sheet_name=None)
        
        # Iterate over all sheets and clean each one
        for sheet_name, sheet_df in df.items():
            print(f"Processing sheet: {sheet_name}")
            df[sheet_name] = clean_data(sheet_df)
        
    else:
        print(f"Unsupported file type: {file_extension}")
        return None

    return df

# Function to save DataFrame as a JSON file
def save_json(data, file_name, output_dir):
    # Create the directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the output directory if it doesn't exist

    # Save as JSON
    json_file_path = os.path.join(output_dir, f"{file_name}.json")
    print(f"Saving data to {json_file_path}")
    data.to_json(json_file_path, orient='records', lines=True)  # 'records' stores rows as JSON objects

# Function to process all files in a directory and save as JSON
def process_files(directory_path, output_dir):
    # Find all CSV and Excel files in the given directory
    csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
    xls_files = glob.glob(os.path.join(directory_path, "*.xlsx"))
    print(f"Found CSV files: {csv_files}")
    print(f"Found Excel files: {xls_files}")

    all_files = csv_files + xls_files

    # Process each file
    for file in all_files:
        # Extract file name without extension
        file_name = os.path.splitext(os.path.basename(file))[0]
        
        data = read_file(file)
        if isinstance(data, pd.DataFrame):
            # Single sheet CSV or Excel file
            save_json(data, file_name, output_dir)
        
        elif isinstance(data, dict):
            # Multiple sheets (Excel file)
            for sheet_name, sheet_df in data.items():
                sheet_file_name = f"{file_name}_{sheet_name}"
                save_json(sheet_df, sheet_file_name, output_dir)
        
        else:
            print(f"Error processing {file}. Skipping...")

# Main execution
if __name__ == "__main__":
    # Specify the directory containing sheets
    input_directory = './data' 
    output_directory = './output' 
    
    # Process all files in the directory and save the data as JSON
    process_files(input_directory, output_directory)

