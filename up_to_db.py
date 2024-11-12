import os
import mysql.connector
from mysql.connector import errorcode

def connect_to_database(db_config):
    """
    Establishes a connection to the database.
    """
    try:
        conn = mysql.connector.connect(**db_config)
        print("Database connection established.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def execute_sql_file(cursor, file_path):
    """
    Reads and executes SQL commands from a file.
    """
    with open(file_path, 'r') as file:
        sql_commands = file.read()
    
    # Execute each SQL command in the file
    for sql_command in sql_commands.split(';'):
        sql_command = sql_command.strip()
        if sql_command:
            try:
                cursor.execute(sql_command)
                print(f"Executed SQL command from {file_path}")
            except mysql.connector.Error as err:
                print(f"Error executing command in {file_path}: {err}")

def upload_sql_schemas_to_db(sql_folder, db_config):
    """
    Uploads all SQL schema files in a directory to the database.
    """
    conn = connect_to_database(db_config)
    if not conn:
        print("Failed to connect to the database. Exiting.")
        return

    cursor = conn.cursor()

    # List all SQL files in the specified folder
    sql_files = [f for f in os.listdir(sql_folder) if f.endswith('.sql')]
    
    if not sql_files:
        print(f"No SQL files found in directory: {sql_folder}")
    else:
        for sql_file in sql_files:
            file_path = os.path.join(sql_folder, sql_file)
            print(f"Processing SQL file: {file_path}")
            execute_sql_file(cursor, file_path)
        
        # Commit the transaction if all SQL commands execute successfully
        conn.commit()
        print("All SQL schema files uploaded to the database.")
    
    cursor.close()
    conn.close()
