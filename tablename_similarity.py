from sentence_transformers import SentenceTransformer
import pandas as pd
from sentence_transformers import util

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

sap_dum = pd.read_csv("sap_table_desc_table_all.csv")
oracle_dum = pd.read_csv("oracle_table_desc_table_all.csv")

oracle_dum["oracle_emb_description"] = oracle_dum.apply(lambda x: list(model.encode(str(x["ORACLE_TABLE_DESCRIPTION"]))), axis = 1)
sap_dum["sap_emb_description"] = sap_dum.apply(lambda x: list(model.encode(str(x["SAP_TABLE_DESCRIPTION"]))), axis = 1)

oracle_dum.to_csv("oracle_actual_table_desc_with_emb.csv", index = False)
sap_dum.to_csv("sap_actual_table_desc_with_emb.csv", index = False)


#print(oracle_dum[["DESCRIPTION","emb_description"]].head())
#print(sap_dum[["DDTEXT","emb_description"]].head())

outer = pd.DataFrame(oracle_dum.assign(key=1).merge(sap_dum.assign(key=1), how='outer', on='key'))

outer["cos_sim"] = outer.apply(lambda x: util.cos_sim(x["oracle_emb_description"], x["sap_emb_description"])[0][0].item(), axis = 1)
filtered_df = outer[outer["cos_sim"] > 0.6]
print(filtered_df.head())

filtered_df.to_csv("filtered_df60.csv", index = False)

#oracle_dum.to_csv("oracle_dummy_data_emb1.csv", index = False)
#ap_dum.to_csv("sap_dummy_data_emb1.csv", index = False)