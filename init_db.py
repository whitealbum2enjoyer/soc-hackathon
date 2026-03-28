import sqlite3
import os

def init_db():
    # File path for the database
    db_file = 'library.db'
    schema_file = 'schema.sql'

    # Remove the existing database to start fresh
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing {db_file}")

    # Connect to (or create) the database file
    connection = sqlite3.connect(db_file)
    
    # Read the schema file
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            connection.executescript(f.read())
        print(f"Executed {schema_file} successfully.")
    except Exception as e:
        print(f"Error executing schema: {e}")
        connection.close()
        return

    # Commit changes and close
    connection.commit()
    connection.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
