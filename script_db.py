from sqlalchemy import create_engine, inspect
import pandas as pd
from transformers import DistilBertTokenizer, DistilBertModel
import torch

def execute_sql_file(engine, sql_file_path):
    with engine.connect() as connection:
        with open(sql_file_path, 'r') as file:
            sql_content = file.read()
        connection.execute(sql_content)

def extract_schema(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    schema_info = []

    for table in tables:
        columns = inspector.get_columns(table)
        for column in columns:
            schema_info.append({
                'Table': table,
                # 'Column': column['name'],
                # 'Type': str(column['type']),
                # 'Nullable': column['nullable'],
                # 'Default': column.get('default')
            })

    return pd.DataFrame(schema_info)

def convert_to_sentence(table_name, columns):
    return f"The table {table_name} has columns: {columns}"

def get_embedding(sentence, model, tokenizer):
    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

def process_sql_files_and_generate_embeddings(sql_files):
    engine = create_engine('sqlite:///:memory:')  # In-memory SQLite database

    for sql_file in sql_files:
        execute_sql_file(engine, sql_file)

    # schema_df = extract_schema(engine)

    # tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    # model = DistilBertModel.from_pretrained('distilbert-base-uncased')

    # embeddings = []
    # grouped = schema_df.groupby('Table')

    # for table_name, group in grouped:
    #     columns_info = []
    #     for _, row in group.iterrows():
    #         column_info = f"{row['Column']} {row['Type']} {'NULL' if row['Nullable'] else 'NOT NULL'}"
    #         if pd.notna(row['Default']):
    #             column_info += f" DEFAULT {row['Default']}"
    #         columns_info.append(column_info)

    #     sentence = convert_to_sentence(table_name, ', '.join(columns_info))
    #     embedding = get_embedding(sentence, model, tokenizer)
    #     embeddings.append((table_name, embedding))

    # return embeddings
    # return schema_df

def main():
    # List of SQL files to process
    sql_files = ['createtablesecc60kjl.sql', 'ORACLE_EBS.sql']  # Replace with your actual file paths

    ## Process the SQL files and generate embeddings
    # embeddings = process_sql_files_and_generate_embeddings(sql_files)
    # Process the SQL files and generate embeddings
    process_sql_files_and_generate_embeddings(sql_files)
    # print(type(schema_df))
    # # Print the embeddings
    # for table_name, embedding in embeddings:
    #     print(f"Table: {table_name}, Embedding: {embedding}")

if __name__ == "__main__":
    main()
