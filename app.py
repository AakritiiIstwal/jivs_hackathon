# 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
import streamlit as st
import time 
import random
from openai import OpenAI
import warnings
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)


# def response_generator(response):
def response_generator():
    response = random.choice(
        [
            "This is the reason behind the issue",
            "FInally giving the answer",
            "I know why it is a match",
        ]
    )
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.05)


dummy = [
        {
            "Source table": "EMPLOYEES",
            "Target Table": "EMPLOYEE_MASTER",
            "Source Column Name": "EMP_SALARY",
            "Target Column Name": "SALARY",
            "Source Column Type": "NUMBER(10,2)",
            "Target Column Type": "DECIMAL(10,2)"
        },
        {
            "Source table": "EMPLOYEES",
            "Target Table": "PAYROLL_DATA",
            "Source Column Name": "EMP_ID",
            "Target Column Name": "EMPLOYEE_ID",
            "Source Column Type": "NUMBER(10)",
            "Target Column Type": "INT"
        },
        {
            "Source table": "EMPLOYEES",
            "Target Table": "PERSONAL_INFO",
            "Source Column Name": "EMP_NAME",
            "Target Column Name": "FULL_NAME",
            "Source Column Type": "VARCHAR2(100)",
            "Target Column Type": "VARCHAR(100)"
        },
        {
            "Source table": "EMPLOYEES",
            "Target Table": "DEPARTMENT_INFO",
            "Source Column Name": "EMP_DEPT",
            "Target Column Name": "DEPARTMENT",
            "Source Column Type": "VARCHAR2(50)",
            "Target Column Type": "VARCHAR(50)"
        },
        {
            "Source table": "EMPLOYEES",
            "Target Table": "EMPLOYEE_HISTORY",
            "Source Column Name": "EMP_HIRE_DATE",
            "Target Column Name": "HIRE_DATE",
            "Source Column Type": "DATE",
            "Target Column Type": "DATETIME"
        }
]

def open_file_to_list(file_name):
    my_file = open(file_name, "r") 
    table_names = my_file.read() 
    table_names_list = table_names.split("\n") 
    my_file.close() 
    return table_names_list

# st.title("Next Gen Schema Matcher")
st.markdown("""
    <div style='text-align: center;'>
        <h1>MapX</h1>
        <h2> Welcome to MapX </h2>
    </div>
""", unsafe_allow_html=True)


def Home():
    # st.write(st.session_state.foo)
    # st.write("""This Next Gen AI Matcher can automaticly help in the process of schema mapping between different databases. The 
    #          application identifies tables and columns with similar structures and suggest potential mappings. The tool provides a 
    #          with an interpretable reason why it is a possible match""")

    st.write("""Unlock the power of seamless data integration with MapX. Designed for today's data-centric world, MapX
             automates the complex task of cross-database schema mapping and value harmonization. Effortlessly identify, 
             map, and align tables and columns across different database systems, ensuring data consistency and operational 
             efficiency across your organization.
             """
    )

    st.write("""Whether you're merging data from diverse sources or standardizing terminology and formats, 
             MapX empowers you to streamline processes, reduce errors, and make informed decisions faster. Experience a smarter way to manage your 
             data today.""")

def Matcher():
    # uploaded_file = st.file_uploader("Upload the file")
    # print(uploaded_file)
    proceed_flag = False
    style = "<style>.row-widget.stButton {text-align: center;}</style>"
    st.markdown(style, unsafe_allow_html=True)
    if st.button("Start Matching"):
        progress_text = "Matching in progress.. Please wait!!"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
            if percent_complete == 99:
                proceed_flag = True
        time.sleep(1)

    database = st.selectbox(
                "Select the required Database",
                ("Oracle", "SAP"),
                )
    if database == "Oracle":
        oracle_table_names_list = open_file_to_list("oracle_table_names.txt")
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
        st.session_state.messages = []

        # client = OpenAI(api_key="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")
        # prompt = f"Here are a list of dictionary having table details that I want you to explain if the tables are a match or not. \n {dummy}"

        # completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        # messages=[
        #     {"role": "system", "content": """You are an assistant who is an expert in schema mapping. Based on the incoming json file you need to 
        #     explain if the source and target table is a match or not. Make sure to generate the explanation in the end with bullet points.
        #     """},
        #     {"role": "user", "content": prompt}
        # ]
        # )
        
        # # Get the summary and named entities
        # result = completion.choices[0].message.content
        # print(result)

        # client.close()

        
        with st.chat_message("assistant"):
            # response = st.write_stream(response_generator(result))
            response = st.write_stream(response_generator())
        st.session_state.messages.append({"role": "assistant", "content": response})

        tab_list = []  

        # for i, tab in enumerate(tabs):
        #     with tab:
        #         st.write(f"This is the content of {tab_list[i]}")

        for i in range(len(dummy)):
            tab_list.append("Tab "+ str(i))

        index = 0
        for tab in tab_list:
            with st.expander(tab):
                st.write("This is the content of:")
                st.write(dummy[index])
            index = index + 1

def Settings():
    st.write()

pg = st.navigation([st.Page(Home), st.Page(Matcher), st.Page(Settings)])
pg.run()

