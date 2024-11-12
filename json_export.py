import os
import json

def save_to_json(data, output_folder, file_name):
    """
    Saves each sheet's data as JSON files in the specified output folder.
    Each file is named based on the original file name and sheet name.
    """
    for sheet_name, df in data.items():
        # Convert all datetime columns to strings (ISO format) to ensure JSON compatibility
        for col in df.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns:
            df[col] = df[col].astype(str)

        json_file_name = f"{file_name}_{sheet_name}.json".replace(" ", "_")
        json_path = os.path.join(output_folder, json_file_name)
        
        # Convert DataFrame to JSON format
        json_data = df.to_dict(orient='records')
        print(json_data)
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, default=str)
            #json.dumps(json_data, indent=4, sort_keys=True, default=str)
        
        print(f"Saved JSON file: {json_path}")
