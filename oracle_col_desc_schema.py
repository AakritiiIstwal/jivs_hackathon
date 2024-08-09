import pandas as pd

# Define the schema with column names and descriptions
schema = {
    'Column': [
        'OWNER', 'TABLE_NAME', 'COLUMN_NAME', 'DATA_TYPE', 'DATA_TYPE_MOD', 'DATA_TYPE_OWNER',
        'DATA_LENGTH', 'DATA_PRECISION', 'DATA_SCALE', 'NULLABLE', 'COLUMN_ID', 'DEFAULT_LENGTH',
        'DATA_DEFAULT', 'NUM_DISTINCT', 'LOW_VALUE', 'HIGH_VALUE', 'DENSITY', 'NUM_NULLS',
        'NUM_BUCKETS', 'LAST_ANALYZED', 'SAMPLE_SIZE', 'CHARACTER_SET_NAME', 'CHAR_COL_DECL_LENGTH',
        'GLOBAL_STATS', 'USER_STATS', 'AVG_COL_LEN', 'CHAR_LENGTH', 'CHAR_USED', 'V80_FMT_IMAGE',
        'DATA_UPGRADED', 'HISTOGRAM', 'DEFAULT_ON_NULL', 'IDENTITY_COLUMN', 'SENSITIVE_COLUMN',
        'EVALUATION_EDITION', 'UNUSABLE_BEFORE', 'UNUSABLE_BEGINNING', 'COLLATION'
    ],
    'Datatype': [
        'VARCHAR2(128)', 'VARCHAR2(128)', 'VARCHAR2(128)', 'VARCHAR2(128)', 'VARCHAR2(3)', 'VARCHAR2(128)',
        'NUMBER', 'NUMBER', 'NUMBER', 'VARCHAR2(1)', 'NUMBER', 'NUMBER',
        'LONG', 'NUMBER', 'RAW(1000)', 'RAW(1000)', 'NUMBER', 'NUMBER',
        'NUMBER', 'DATE', 'NUMBER', 'VARCHAR2(44)', 'NUMBER',
        'VARCHAR2(3)', 'VARCHAR2(3)', 'NUMBER', 'NUMBER', 'VARCHAR2(1)', 'VARCHAR2(3)',
        'VARCHAR2(3)', 'VARCHAR2(15)', 'VARCHAR2(3)', 'VARCHAR2(3)', 'VARCHAR2(3)',
        'VARCHAR2(128)', 'VARCHAR2(128)', 'VARCHAR2(128)', 'VARCHAR2(100)'
    ],
    'Description': [
        'Owner of the table, view, or cluster', 'Name of the table, view, or cluster', 'Column name',
        'Data type of the column', 'Data type modifier of the column', 'Owner of the data type of the column',
        'Length of the column (in bytes)', 'Decimal precision for NUMBER data type; binary precision for FLOAT data type; NULL for all other data types',
        'Digits to the right of the decimal point in a number', 'Indicates whether a column allows NULLs. The value is N if there is a NOT NULL constraint on the column or if the column is part of a PRIMARY KEY. The constraint should be in an ENABLE VALIDATE state.',
        'Sequence number of the column as created', 'Length of the default value for the column',
        'Default value for the column', 'Number of distinct values in the column', 'Low value in the column', 'High value in the column',
        'If a histogram is available on COLUMN_NAME, then this column displays the selectivity of a value that spans fewer than 2 endpoints in the histogram. It does not represent the selectivity of values that span 2 or more endpoints. If a histogram is not available on COLUMN_NAME, then the value of this column is 1/NUM_DISTINCT.',
        'Number of NULLs in the column', 'Number of buckets in the histogram for the column. Note: The number of buckets in a histogram is specified in the SIZE parameter of the ANALYZE SQL statement. However, Oracle Database does not create a histogram with more buckets than the number of rows in the sample. Also, if the sample contains any values that are very repetitious, Oracle Database creates the specified number of buckets, but the value indicated by this column may be smaller because of an internal compression algorithm.',
        'Date on which this column was most recently analyzed', 'Sample size used in analyzing this column',
        'Name of the character set: CHAR_CS, NCHAR_CS', 'Declaration length of the character type column',
        'GLOBAL_STATS will be YES if statistics are gathered or incrementally maintained, otherwise it will be NO',
        'Indicates whether statistics were entered directly by the user (YES) or not (NO)', 'Average length of the column (in bytes)',
        'Displays the length of the column in characters. This value only applies to the following data types: CHAR, VARCHAR2, NCHAR, NVARCHAR2',
        'Indicates that the column uses BYTE length semantics (B) or CHAR length semantics (C), or whether the data type is not any of the following (NULL): CHAR, VARCHAR2, NCHAR, NVARCHAR2',
        'Indicates whether the column data is in release 8.0 image format (YES) or not (NO)', 'Indicates whether the column data has been upgraded to the latest type version format (YES) or not (NO)',
        'Indicates existence/type of histogram: NONE, FREQUENCY, TOP-FREQUENCY, HEIGHT BALANCED, HYBRID', 'Indicates whether the column has DEFAULT ON NULL semantics (YES) or not (NO)',
        'Indicates whether this is an identity column (YES) or not (NO)', 'Indicates whether this is a sensitive column (YES) or not (NO)',
        'Name of the edition in which editioned objects referenced in an expression column are resolved', 'Name of the oldest edition in which the index may be used as part of a query plan',
        'Name of the edition for which the index may not be used as part of a query plan in this edition or any of its descendants', 'Collation for the column. Only applies to columns with character data types.'
    ]
}

# Check lengths of all lists to ensure they are equal
lengths = [len(v) for v in schema.values()]
print(f"Lengths of each list: {lengths}")

# Create a DataFrame from the schema
df = pd.DataFrame(schema)

# Save the DataFrame to a CSV file
csv_file_path = 'oracle_dba_tab_columns.csv'
df.to_csv(csv_file_path, index=False)

print(f"CSV file with table descriptions saved to {csv_file_path}")