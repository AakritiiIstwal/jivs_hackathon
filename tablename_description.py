import pandas as pd
import pyodbc


with open('processed_oracle_table_names.txt', 'r') as file:
    oracle_names = []

    for line in file:
        line = line.strip()
        oracle_names.append(line)
       
with open('sap_table_names.txt', 'r') as file:
    sap_names = []

    for line in file:
        line = line.strip()
        sap_names.append(line)
    
        

conn_str = (
    r'driver={SQL Server};'
    r'server=(local);'
    r'database=ORACLE_EBS_HACK;'
    r'trusted_connection=yes;'
    )

cnxn = pyodbc.connect(conn_str)

query1 = f"SELECT TABNAME AS SAP_TABLE_NAME, DDTEXT AS SAP_TABLE_DESCRIPTION FROM [ECC60jkl_HACK].[dbo].[DD02T] where DDLANGUAGE='E' and TABNAME IN {tuple(sap_names)}"
#print(oracle_names)
query2 = f"SELECT TABLE_ID AS ORACLE_TABLE_ID, TABLE_NAME AS ORACLE_TABLE_NAME, DESCRIPTION AS ORACLE_TABLE_DESCRIPTION FROM [ORACLE_EBS_HACK].[dbo].[APPLSYS_FND_TABLES] where TABLE_NAME IN {tuple(oracle_names)}"
#print(query2)

#query = "SELECT count(*) FROM [ECC60jkl_HACK].[dbo].[DD02L]"

sap_tables_data = pd.read_sql(query1, cnxn)
sap_tables_data.to_csv("sap_table_desc_table_all.csv", index = False)

oracle_tables_data = pd.read_sql(query2, cnxn)
oracle_tables_data.to_csv("oracle_table_desc_table_all.csv", index = False)