from sqlalchemy import create_engine, inspect
import pandas as pd


def extract_schema(engine):
    inspector = inspect(engine)
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


connection_string_chinook = f'sqlite:///Chinook.db'
connection_string_northwind = f'sqlite:///northwind.db'

engine_chinook = create_engine(connection_string_chinook)
engine_northwind = create_engine(connection_string_northwind)

schema_chinook = extract_schema(engine_chinook)
schema_northwind = extract_schema(engine_northwind)

schema_chinook.to_csv('schema_chinook.csv', index=False)
schema_northwind.to_csv('schema_northwind.csv', index=False)

print("Schema information extracted and saved to CSV files.")
