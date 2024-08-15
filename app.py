import streamlit as st
import time 
import random
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import pandas as pd
from sentence_transformers import util
import warnings
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

sentence_embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def response_generator(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.05)

def open_file_to_list(file_name):
    my_file = open(file_name, "r") 
    table_names = my_file.read() 
    table_names_list = table_names.split("\n") 
    my_file.close() 
    return table_names_list

st.markdown("""
    <div style='text-align: center;'>
        <h1> Welcome to MapX </h1>
    </div>
""", unsafe_allow_html=True)

def Home():
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("""Unlock the power of seamless data integration with MapX. Designed for today's data-centric world, MapX
             automates the complex task of cross-database schema mapping and value harmonization. Effortlessly identify, 
             map, and align tables and columns across different database systems, ensuring data consistency and operational 
             efficiency across your organization.
             """
    )
    st.write("\n")
    st.write("\n")
    st.write("""Whether you're merging data from diverse sources or standardizing terminology and formats, 
             MapX empowers you to streamline processes, reduce errors, and make informed decisions faster. Experience a smarter way to manage your 
             data today.""")

def Matcher():
    style = "<style>.row-widget.stButton {text-align: center;}</style>"
    st.markdown(style, unsafe_allow_html=True)
    if st.button("Start Matching"):
        progress_text = "Matching in progress.. Please wait!!"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)

    database = st.selectbox(
                "Select the required Database",
                (" ", "Oracle", "SAP"),
                )
    if database == "Oracle":
        # oracle_table_names_list = open_file_to_list("oracle_table_names.txt")
        oracle_table_names_list = []
        oracle_table_names_list.append( " ")
        oracle_table_names_list = open_file_to_list("processed_oracle_table_names.txt")
        table_name = st.selectbox(
                        "Select the table name",
                        (oracle_table_names_list)
                    )
    if database == "SAP":
        sap_table_names_list = open_file_to_list("sap_table_names.txt")
        table_name = st.selectbox(
                        "Select the table name",
                        (sap_table_names_list)
                    )

    if st.button("Detailed Report"):
        column_matched = pd.read_csv("column_matched_final.csv")
        if database == "Oracle":
            selected_df = column_matched[column_matched['ORACLE_TABLE_NAME'] == table_name]
        elif database == "SAP":
            selected_df = column_matched[column_matched['SAP_TABLE_NAME'] == table_name]

        selected_df["COLUMN_COSINE_SIMILARITY"] = selected_df.apply(lambda x: util.cos_sim(list(sentence_embedding_model.encode(str(x["ORACLE_COL_DESCRIPTION"]))),
                                                                                  list(sentence_embedding_model.encode(str(x["SAP_COL_DESCRIPTION"]))))[0][0].item(), axis = 1)
        filtered_df = selected_df[selected_df["COLUMN_COSINE_SIMILARITY"] > 0.6]
        filtered_df = filtered_df[["ORACLE_TABLE_NAME", "ORACLE_TABLE_DESCRIPTION", "ORACLE_COL_NAME", "ORACLE_COL_DESCRIPTION", "ORACLE_DATATYPE", "SAP_TABLE_NAME",
         "SAP_TABLE_DESCRIPTION", "SAP_COL_NAME", "SAP_COL_DESCRIPTION", "SAP_DATATYPE", "TABLE_DESCRIPTION_SIMILARITY",
         "COLUMN_COSINE_SIMILARITY"]]
        
        filtered_df['TABLE_DESCRIPTION_SIMILARITY'] = filtered_df['TABLE_DESCRIPTION_SIMILARITY'].round(2)
        filtered_df['COLUMN_COSINE_SIMILARITY'] = filtered_df['COLUMN_COSINE_SIMILARITY'].round(2)
        filtered_df.reset_index(inplace=True, drop= True)
        
        result_json = filtered_df.to_json(orient="index")

        tab_list = []  
        for i in range(filtered_df.shape[0]):
            tab_list.append("Tab "+ str(i+1))

        index = 0
        for tab in tab_list:
            with st.expander(tab):
                st.write("This is the content of:")
                st.write(filtered_df.iloc[index,:])
            index = index + 1

        st.session_state.messages = []

        client = OpenAI(api_key="API_KEY")
        prompt = f"""Here is a dictionary of dictionary having table details that I want you to explain if the tables are a match or not. 
                    Each index of the json corresponds to the two table details \n {result_json}"""

        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are an assistant who is an expert in schema mapping. Based on the incoming json you need to 
            explain if the source and target table is a match or not. The structure should be having each of the index of json.
            explaned with bullet points.
            """},
            {"role": "user", "content": prompt}
        ]
        )
        
        # Get the summary and named entities
        result = completion.choices[0].message.content
        print(result)

        client.close()
        
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(result))
            # response = st.write_stream(response_generator())
        st.session_state.messages.append({"role": "assistant", "content": response})

def Settings():
    st.write()

pg = st.navigation([st.Page(Home), st.Page(Matcher), st.Page(Settings)])
pg.run()
