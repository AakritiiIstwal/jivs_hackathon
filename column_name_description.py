import pandas as pd
import pyodbc

filtered_df60 = pd.read_csv("filtered_df60.csv")
filtered_df60 = filtered_df60.sort_values("cos_sim", ascending = False)    

column_matches = filtered_df60[["ORACLE_TABLE_ID", "ORACLE_TABLE_NAME", "ORACLE_TABLE_DESCRIPTION", "SAP_TABLE_NAME", "SAP_TABLE_DESCRIPTION", "cos_sim"]]
column_matches = column_matches.rename(columns={"cos_sim": "table_desc_sim"})

# matched_row = filtered_df60.iloc[7,:]
oracle_table_id = tuple(column_matches.ORACLE_TABLE_ID)
sap_table_name = tuple(column_matches.SAP_TABLE_NAME)

conn_str = (
    r'driver={SQL Server};'
    r'server=(local);'
    r'database=ORACLE_EBS_HACK;'
    r'trusted_connection=yes;'
    )

cnxn = pyodbc.connect(conn_str)

query1 = f"SELECT TABNAME AS SAP_TABLE_NAME, FIELDNAME AS SAP_COL_NAME, ROLLNAME, DATATYPE as SAP_DATATYPE FROM [ECC60jkl_HACK].[dbo].[DD03L] where TABNAME IN {sap_table_name}"
sap_col_rollname = pd.read_sql(query1, cnxn)

query22 = f"SELECT ROLLNAME, DDTEXT AS SAP_COL_DESCRIPTION FROM [ECC60jkl_HACK].[dbo].[DD04T] where DDLANGUAGE = 'E' and ROLLNAME in {tuple(sap_col_rollname.ROLLNAME)}"
sap_tables_data1 = pd.read_sql(query22, cnxn)

sap_col_data = sap_col_rollname.merge(sap_tables_data1, on = "ROLLNAME", how = "left")
#print(sap_col_data)

query2 = f"SELECT TABLE_ID AS ORACLE_TABLE_ID, COLUMN_NAME AS ORACLE_COL_NAME, DESCRIPTION AS ORACLE_COL_DESCRIPTION, COLUMN_TYPE AS ORACLE_DATATYPE  FROM [ORACLE_EBS_HACK].[dbo].[APPLSYS_FND_COLUMNS] where TABLE_ID IN {oracle_table_id} and DESCRIPTION is not NULL"
oracle_tables_data = pd.read_sql(query2, cnxn)
#query = "SELECT count(*) FROM [ECC60jkl_HACK].[dbo].[DD02L]"

column_matches = column_matches.merge(oracle_tables_data, on = "ORACLE_TABLE_ID", how = "left")
column_matches = column_matches.merge(sap_col_data, on = "SAP_TABLE_NAME", how = "left")

column_matches.to_csv("column_matched.csv", index = False)

sap_col_data.to_csv("sap_col_desc_matched.csv", index = False)
oracle_tables_data.to_csv("oracle_col_desc_matched.csv", index = False)