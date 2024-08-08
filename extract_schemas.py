from sqlalchemy import create_engine, inspect, text
import pandas as pd


def extract_schema(engine):
    # Create an inspector object
    inspector = inspect(engine)

    # Get schema information
    tables = inspector.get_table_names()

    schema_info = []

    for table in tables:
        columns = inspector.get_columns(table)
        for column in columns:
            schema_info.append({
                'Table': table,
                'Column': column['name'],
                'Type': str(column['type']),
                'Nullable': column['nullable'],
                'Default': column.get('default')
            })

    return pd.DataFrame(schema_info)


# Define connection strings for the two SQLite databases
connection_string_db1 = 'sqlite:///database1.db'
connection_string_db2 = 'sqlite:///database2.db'

# Create engines for each database
engine_db1 = create_engine(connection_string_db1)
engine_db2 = create_engine(connection_string_db2)

# Example to create tables and insert data into database1 (for testing purposes)
with engine_db1.connect() as conn:
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT
        )
    '''))
    conn.execute(text('''
        INSERT INTO employees (name, position) VALUES
        ('Alice', 'Engineer'),
        ('Bob', 'Manager')
    '''))

# Example to create tables and insert data into database2 (for testing purposes)
with engine_db2.connect() as conn:
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_name TEXT NOT NULL,
            location TEXT
        )
    '''))
    conn.execute(text('''
        INSERT INTO departments (department_name, location) VALUES
        ('Engineering', 'Building A'),
        ('HR', 'Building B')
    '''))

# Extract schema information from both databases
schema_db1 = extract_schema(engine_db1)
schema_db2 = extract_schema(engine_db2)

# Save schema information to CSV files
schema_db1.to_csv('schema_db1.csv', index=False)
schema_db2.to_csv('schema_db2.csv', index=False)

print("Schema information extracted and saved to CSV files.")
