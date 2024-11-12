import json
import os
import re

def generate_table_name(json_data):
    # If the JSON is a list, use the first dictionary's first key
    if isinstance(json_data, list) and len(json_data) > 0 and isinstance(json_data[0], dict):
        # Use the first dictionary's first key as the table name (simplified)
        first_key = list(json_data[0].keys())[0]
    else:
        # If it's a dictionary, use the first key as the table name
        first_key = list(json_data.keys())[0] if isinstance(json_data, dict) else "default_table"
    
    # Clean up the table name (e.g., remove spaces, special characters)
    table_name = re.sub(r'\W+', '_', first_key).lower()  # Replace non-alphanumeric characters with _
    
    return table_name

def create_sql_schema(json_data):
    # Determine the table name dynamically
    table_name = generate_table_name(json_data)
    
    if not json_data:
        return "", []

    # Assuming the JSON is a list of dictionaries (records)
    columns = json_data[0].keys()

    # Create table schema based on column names and types
    sql_columns = []
    for col in columns:
        # For simplicity, all columns are TEXT, you can extend logic to infer types
        sql_columns.append(f"{col} TEXT")
    
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    create_table_query += ",\n".join(sql_columns)
    create_table_query += "\n);"

    # Create insert statements based on data
    insert_statements = []
    for record in json_data:
        values = [f"'{str(record[col])}'" for col in columns]
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
        insert_statements.append(insert_query)
    
    return create_table_query, insert_statements

def process_json_files_from_directory(dir_path, output_dir):
    # List all JSON files in the specified directory
    json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]
    
    if not json_files:
        print(f"No JSON files found in directory: {dir_path}")
        return
    
    for json_file in json_files:
        file_path = os.path.join(dir_path, json_file)
        print(f"Processing file: {file_path}")
        
        try:
            # Read the JSON data from the file
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            # Generate SQL schema
            create_query, insert_queries = create_sql_schema(json_data)
            
            # Save the SQL schema to a file in the specified output directory
            output_sql_file = os.path.splitext(json_file)[0] + "_output.sql"
            save_sql_to_file(create_query, insert_queries, os.path.join(output_dir, output_sql_file))
        
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {json_file}")
        except Exception as e:
            print(f"An error occurred while processing {json_file}: {str(e)}")

def save_sql_to_file(create_query, insert_queries, filename="output.sql"):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(create_query + "\n\n")
        file.write("\n".join(insert_queries))
    print(f"SQL schema saved to {filename}")


# Example usage: Process JSON files from a folder called 'json_data'
#directory_path = './json'  # Change this to your folder path
#output_sql_path = './sql'
#process_json_files_from_directory(directory_path, output_sql_path)
