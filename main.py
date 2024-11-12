import os
import argparse
import subprocess

from read_extract import read_and_clean_excel
from json_export import save_to_json
from design_schema import process_json_files_from_directory
from up_to_db import upload_sql_schemas_to_db 


# MySQL database connection configuration
db_config = {
    'user': 'root',       # Your MySQL username
    'password': 'password',  # Your MySQL password
    'host': 'localhost',  # Database host (usually localhost)
    'database': 'my_database',  # The name of the database you want to use
}

def check_mysql_installed():
    """
    Check if MySQL is installed on the system.
    """
    try:
        result = subprocess.run(['mysql', '--version'], capture_output=True, text=True, check=True)
        print(f"MySQL is installed: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("MySQL is not installed or not available in PATH.")
        return False
    except FileNotFoundError:
        print("MySQL executable not found. Please ensure MySQL is installed and added to your PATH.")
        return False
def parse_args():
    """
    Parse command-line arguments for database configuration.
    """
    parser = argparse.ArgumentParser(description="Process Excel files, generate SQL schemas, and upload to MySQL database.")
    
    # Define the expected command-line arguments
    parser.add_argument('--user', required=True, help="MySQL username")
    parser.add_argument('--password', required=True, help="MySQL password")
    parser.add_argument('--host', default='localhost', help="MySQL host (default: localhost)")
    parser.add_argument('--database', default='Soneras', help="Name of the MySQL database")

    # Parse the arguments and return them as a dictionary
    return vars(parser.parse_args())

def process_folder(folder_path, output_folder):
    """
    Process all Excel files in the given folder, converting each sheet to a JSON file.
    """

    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.xls', '.xlsx')):
            file_path = os.path.join(folder_path, file_name)
            data = read_and_clean_excel(file_path)
            base_name = os.path.splitext(file_name)[0]
            save_to_json(data, output_folder, base_name)


if __name__ == "__main__":

    # Step 0: Check if MySQL is installed
    if not check_mysql_installed():
        print("Exiting the script. Please install MySQL and try again.")
        exit(1)
    
    # Parse command-line arguments to get database configuration
    db_config = parse_args()

    #folders paths (i/o data)
    folder_path = './data'
    output_folder_json = './json'
    output_folder_sql = './sql'
    
    # Create the outputs folders if they doesn't exist
    os.makedirs(output_folder_json, exist_ok=True)  
    os.makedirs(output_folder_sql, exist_ok=True)  

    #step1: convert excels to json
    process_folder(folder_path, output_folder_json)

    #step2: Call the function to process the files and upload data to MySQL
    process_json_files_from_directory(output_folder_json, output_folder_sql)

    #step3: Upload SQL schemas to the database
    upload_sql_schemas_to_db(output_folder_sql, db_config)
    print("Database upload complete.")




