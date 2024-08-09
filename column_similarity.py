from sentence_transformers import SentenceTransformer
import pandas as pd
from sentence_transformers import util

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# sap_dum = pd.read_csv("sap_col_desc_matched.csv")
# oracle_dum = pd.read_csv("oracle_col_desc_matched.csv")

column_matched = pd.read_csv("column_matched.csv")
selected_df = column_matched[column_matched['ORACLE_TABLE_NAME'] == "PA_PROJECT_PARTIES"]

#column_matched["oracle_emb_description"] = column_matched.apply(lambda x: list(model.encode(str(x["ORACLE_COL_DESCRIPTION"]))), axis = 1)
#column_matched["sap_emb_description"] = column_matched.apply(lambda x: list(model.encode(str(x["SAP_COL_DESCRIPTION"]))), axis = 1)

selected_df["cos_sim_column"] = selected_df.apply(lambda x: util.cos_sim(list(model.encode(str(x["ORACLE_COL_DESCRIPTION"]))), list(model.encode(str(x["SAP_COL_DESCRIPTION"]))))[0][0].item(), axis = 1)
filtered_df = selected_df[selected_df["cos_sim_column"] > 0.6]
print(filtered_df)
filtered_df[["ORACLE_TABLE_NAME", "ORACLE_TABLE_DESCRIPTION", "ORACLE_COL_NAME", "ORACLE_COL_DESCRIPTION", "ORACLE_DATATYPE", "SAP_TABLE_NAME", "SAP_TABLE_DESCRIPTION", "SAP_COL_NAME", "SAP_COL_DESCRIPTION", "SAP_DATATYPE", "table_desc_sim", "cos_sim_column"]].to_csv("filtered_col_sim.csv", index = False)

# oracle_dum["oracle_emb_description"] = oracle_dum.apply(lambda x: list(model.encode(str(x["ORACLE_COL_DESCRIPTION"]))), axis = 1)
# sap_dum["sap_emb_description"] = sap_dum.apply(lambda x: list(model.encode(str(x["SAP_COL_DESCRIPTION"]))), axis = 1)

# oracle_dum.to_csv("oracle_actual_col_desc_with_emb.csv", index = False)
# sap_dum.to_csv("sap_actual_col_desc_with_emb.csv", index = False)


#print(oracle_dum[["DESCRIPTION","emb_description"]].head())
#print(sap_dum[["DDTEXT","emb_description"]].head())

# outer = pd.DataFrame(oracle_dum.assign(key=1).merge(sap_dum.assign(key=1), how='outer', on='key'))

# outer["cos_sim"] = outer.apply(lambda x: util.cos_sim(x["oracle_emb_description"], x["sap_emb_description"])[0][0].item(), axis = 1)
# filtered_df = outer[outer["cos_sim"] > 0.5]
# print(filtered_df)

# filtered_df.to_csv("filtered_col_df60.csv", index = False)

#oracle_dum.to_csv("oracle_dummy_data_emb1.csv", index = False)
#ap_dum.to_csv("sap_dummy_data_emb1.csv", index = False)