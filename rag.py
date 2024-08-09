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
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from huggingface_hub import InferenceClient
from langchain.llms import HuggingFaceEndpoint
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = getpass.getpass()
llm = ChatOpenAI(model="gpt-4o-mini")

# llm = HuggingFaceEndpoint(
#             endpoint_url="https://q2sxm30ut74mj3w3.us-east-1.aws.endpoints.huggingface.cloud/",
#             huggingfacehub_api_token="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",
#             task="text-generation",
#             max_new_tokens=150, 
#             do_sample=True, 
#             top_p=0.9, 
#             temperature=0.2
#             )
loader = TextLoader("target.txt")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)


# #remove
# # Hugging-Face Embeddings
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2",
#     model_kwargs={"device": "cpu"},
# )
# vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)



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
"This table stores information about projects, including their planned start and finish dates, planning method, budget authorization key, and project definition. The table provides a comprehensive overview of project planning and execution, enabling effective monitoring and control of project progress."
If yes, then give the source and target column mappings.'''

for chunk in rag_chain.stream(query):
    print(chunk, end="", flush=True)