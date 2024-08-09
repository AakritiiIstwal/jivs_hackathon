import getpass
import os

import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.text import TextLoader
from langchain_experimental.agents.agent_toolkits import create_csv_agent



os.environ["OPENAI_API_KEY"] = getpass.getpass()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

#CSV AGENT-------------

# # Create the CSV agent
# agent = create_csv_agent(llm, "sap_dummy_data_dd02t.csv", verbose=True, allow_dangerous_code=True)
# def query_data(query):
#     response = agent.invoke(query)
#     return response

# query = "Can you tell me something about tabname MARA?"
# response = query_data(query)
# print(response)

#CSV AGENT-------------


#TEXT LOADER------------

# # Load, chunk and index the contents of the blog.
# loader = WebBaseLoader(
#     web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
#     bs_kwargs=dict(
#         parse_only=bs4.SoupStrainer(
#             class_=("post-content", "post-title", "post-header")
#         )
#     ),
# )
# docs = loader.load()
#TEXT LOADER------------

loader = TextLoader("target.txt")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

query = '''Find if the table is relevant to the target database for the following description: 
"This table contains customer information such as names, contact details, and demographic data. The key columns include a unique identifier for each customer, the customer's first name, last name, email, phone number, date of birth, address, city, state, zip code, and registration date."
If yes, then give the source and target column mappings'''

for chunk in rag_chain.stream(query):
    print(chunk, end="", flush=True)