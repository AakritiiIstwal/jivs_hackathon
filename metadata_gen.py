import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker for generating random data
faker = Faker()

# Define the schema with column names and types
schema_applsys_fnd_tables = {
    'APPLICATION_ID': 'numeric',
    'TABLE_ID': 'numeric',
    'TABLE_NAME': 'nvarchar',
    'USER_TABLE_NAME': 'nvarchar',
    'LAST_UPDATE_DATE': 'datetime2',
    'LAST_UPDATED_BY': 'numeric',
    'CREATION_DATE': 'datetime2',
    'CREATED_BY': 'numeric',
    'LAST_UPDATE_LOGIN': 'numeric',
    'AUTO_SIZE': 'nvarchar',
    'TABLE_TYPE': 'nvarchar',
    'INITIAL_EXTENT': 'numeric',
    'NEXT_EXTENT': 'numeric',
    'MIN_EXTENTS': 'numeric',
    'MAX_EXTENTS': 'numeric',
    'PCT_INCREASE': 'numeric',
    'INI_TRANS': 'numeric',
    'MAX_TRANS': 'numeric',
    'PCT_FREE': 'numeric',
    'PCT_USED': 'numeric',
    'DESCRIPTION': 'nvarchar',
    'HOSTED_SUPPORT_STYLE': 'nvarchar',
    'IREP_COMMENTS': 'nvarchar',
    'IREP_ANNOTATIONS': 'nvarchar'
}

schema_dd02t = {
    'TABNAME': 'nvarchar',
    'DDLANGUAGE': 'nvarchar',
    'AS4LOCAL': 'nvarchar',
    'AS4VERS': 'nvarchar',
    'DDTEXT': 'nvarchar'
}

oracle_table_descriptions = [
    {'TABLE_NAME': 'APPLSYS_FND_APPLICATION', 'DESCRIPTION': 'Applications'},
    {'TABLE_NAME': 'APPLSYS_FND_APPLICATION_TL', 'DESCRIPTION': 'Application Translations'},
    {'TABLE_NAME': 'APPLSYS_FND_ATTACHED_DOCUMENTS', 'DESCRIPTION': 'Attached Documents'},
    {'TABLE_NAME': 'APPLSYS_FND_COLUMNS', 'DESCRIPTION': 'Table Columns'},
    {'TABLE_NAME': 'APPLSYS_FND_CURRENCIES', 'DESCRIPTION': 'Currencies'},
    {'TABLE_NAME': 'APPLSYS_FND_CURRENCIES_TL', 'DESCRIPTION': 'Currency Translations'},
    {'TABLE_NAME': 'APPLSYS_FND_DESCRIPTIVE_FLEXS', 'DESCRIPTION': 'Descriptive Flexfields'},
    {'TABLE_NAME': 'APPLSYS_FND_DESCRIPTIVE_FLEXS_TL', 'DESCRIPTION': 'Descriptive Flexfield Translations'},
    {'TABLE_NAME': 'APPLSYS_FND_DOCUMENTS', 'DESCRIPTION': 'Documents'},
    {'TABLE_NAME': 'APPLSYS_FND_DOCUMENTS_LONG_TEXT', 'DESCRIPTION': 'Documents Long Text'},
    {'TABLE_NAME': 'APPLSYS_FND_DOCUMENTS_SHORT_TEXT', 'DESCRIPTION': 'Documents Short Text'},
    {'TABLE_NAME': 'APPLSYS_FND_DOCUMENTS_TL', 'DESCRIPTION': 'Document Translations'},
    {'TABLE_NAME': 'APPLSYS_FND_DOCUMENT_CATEGORIES', 'DESCRIPTION': 'Document Categories'},
    {'TABLE_NAME': 'APPLSYS_FND_DOCUMENT_CATEGORIES_TL', 'DESCRIPTION': 'Document Category Translations'},
    {'TABLE_NAME': 'APPLSYS_FND_DOCUMENT_DATATYPES', 'DESCRIPTION': 'Document Datatypes'},
    {'TABLE_NAME': 'APPLSYS_FND_FLEX_VALUES', 'DESCRIPTION': 'Flex Values'},
    {'TABLE_NAME': 'APPLSYS_FND_FLEX_VALUE_SETS', 'DESCRIPTION': 'Flex Value Sets'},
    {'TABLE_NAME': 'APPLSYS_FND_ID_FLEX_STRUCTURES', 'DESCRIPTION': 'ID Flex Structures'},
    {'TABLE_NAME': 'APPLSYS_FND_ID_FLEX_STRUCTURES_TL', 'DESCRIPTION': 'ID Flex Structure Translations'},
    {'TABLE_NAME': 'APPLSYS_FND_LANGUAGES', 'DESCRIPTION': 'Languages'}
]

# Existing table descriptions
table_descriptions = [
    {'TABNAME': 'MARA', 'DDTEXT': 'Material Master'},
    {'TABNAME': 'BKPF', 'DDTEXT': 'Accounting Document Header'},
    {'TABNAME': 'LFA1', 'DDTEXT': 'Vendor Master (General)'},
    {'TABNAME': 'KNA1', 'DDTEXT': 'Customer Master'},
    {'TABNAME': 'VBAP', 'DDTEXT': 'Sales Document Item'},
    {'TABNAME': 'VBAK', 'DDTEXT': 'Sales Document Header'},
    {'TABNAME': 'EBAN', 'DDTEXT': 'Purchase Requisition'},
    {'TABNAME': 'EKPO', 'DDTEXT': 'Purchasing Document Item'},
    {'TABNAME': 'EKKN', 'DDTEXT': 'Account Assignment in Purchasing Document'},
    {'TABNAME': 'AFKO', 'DDTEXT': 'Order Header'}
]

# Add additional dummy entries
additional_entries = [
    {'TABNAME': 'PKHD', 'DDTEXT': 'Control Cycle Header'},
    {'TABNAME': 'PLAB', 'DDTEXT': 'Planning Table: Orders by Location'},
    {'TABNAME': 'PLAS', 'DDTEXT': 'Allocation Table for Planned Orders'},
    {'TABNAME': 'PLFH', 'DDTEXT': 'Production Resources/Tools Assignment Header'},
    {'TABNAME': 'PLFL', 'DDTEXT': 'Production Resources/Tools Assignment Lines'},
    {'TABNAME': 'PLFT', 'DDTEXT': 'Production Resources/Tools Assignment Texts'},
    {'TABNAME': 'PLFV', 'DDTEXT': 'Production Resources/Tools Assignment Versions'},
    {'TABNAME': 'PLKO', 'DDTEXT': 'Routing Header'},
    {'TABNAME': 'PLKZ', 'DDTEXT': 'Capacity Planning Header'},
    {'TABNAME': 'PLMK', 'DDTEXT': 'Inspection Plan Header'},
    {'TABNAME': 'PLMW', 'DDTEXT': 'Quality Management Inspection Point'},
    {'TABNAME': 'PLMZ', 'DDTEXT': 'Quality Management Inspection Lot'},
    {'TABNAME': 'PLPO', 'DDTEXT': 'Routing Operations'},
    {'TABNAME': 'PLWP', 'DDTEXT': 'Work Center Capacity Requirements'},
    {'TABNAME': 'PLZU', 'DDTEXT': 'Planning Allocation Overview'}
]

# Combine the lists
table_descriptions.extend(additional_entries)

# Number of dummy rows to generate
num_rows_applsys = len(oracle_table_descriptions)
num_rows_dd02t = len(table_descriptions)

# Generate random data for APPLSYS_FND_TABLES based on its schema
data_applsys_fnd_tables = {}
for column, col_type in schema_applsys_fnd_tables.items():
    if col_type == 'numeric':
        data_applsys_fnd_tables[column] = np.random.randint(1, 1000000, size=num_rows_applsys)
    elif col_type == 'nvarchar':
        if column == 'TABLE_NAME':
            data_applsys_fnd_tables[column] = [entry['TABLE_NAME'] for entry in oracle_table_descriptions]
        elif column == 'DESCRIPTION':
            data_applsys_fnd_tables[column] = [entry['DESCRIPTION'] for entry in oracle_table_descriptions]
        elif column == 'USER_TABLE_NAME':
            data_applsys_fnd_tables[column] = [faker.company() for _ in range(num_rows_applsys)]
        elif column == 'AUTO_SIZE':
            data_applsys_fnd_tables[column] = [faker.random_element(elements=('Y', 'N')) for _ in range(num_rows_applsys)]
        elif column == 'TABLE_TYPE':
            data_applsys_fnd_tables[column] = [faker.random_element(elements=('T', 'V', 'L')) for _ in range(num_rows_applsys)]
        elif column == 'HOSTED_SUPPORT_STYLE':
            data_applsys_fnd_tables[column] = [faker.random_element(elements=('Style1', 'Style2', 'Style3')) for _ in range(num_rows_applsys)]
        elif column in ['IREP_COMMENTS', 'IREP_ANNOTATIONS']:
            data_applsys_fnd_tables[column] = [faker.paragraph(nb_sentences=3) for _ in range(num_rows_applsys)]
        else:
            data_applsys_fnd_tables[column] = [faker.text(max_nb_chars=30) for _ in range(num_rows_applsys)]
    elif col_type == 'datetime2':
        data_applsys_fnd_tables[column] = [faker.date_time_this_decade() for _ in range(num_rows_applsys)]

# Generate random data for DD02T based on its schema
data_dd02t = {
    'TABNAME': [entry['TABNAME'] for entry in table_descriptions],
    'DDLANGUAGE': ['E' for _ in range(num_rows_dd02t)],
    'AS4LOCAL': [faker.random_element(elements=('A', 'B', 'C')) for _ in range(num_rows_dd02t)],
    'AS4VERS': [faker.random_element(elements=('0001', '0002', '0003')) for _ in range(num_rows_dd02t)],
    'DDTEXT': [entry['DDTEXT'] for entry in table_descriptions]
}

# Create DataFrames from the generated data
df_applsys_fnd_tables = pd.DataFrame(data_applsys_fnd_tables)
df_dd02t = pd.DataFrame(data_dd02t)

# Save the DataFrames to CSV files
csv_file_path_applsys = 'oracle_dummy_data.csv'
csv_file_path_dd02t = 'sap_dummy_data_dd02t.csv'
df_applsys_fnd_tables.to_csv(csv_file_path_applsys, index=False)
df_dd02t.to_csv(csv_file_path_dd02t, index=False)

print(f"Dummy data for APPLSYS_FND_TABLES saved to {csv_file_path_applsys}")
print(f"Dummy data for DD02T saved to {csv_file_path_dd02t}")