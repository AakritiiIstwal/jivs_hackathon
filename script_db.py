from sqlalchemy import create_engine, inspect
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import jaccard


def get_sample_data(engine, table_name, sample_size=100):
    query = f"SELECT * FROM {table_name} LIMIT {sample_size}"
    return pd.read_sql(query, engine)

# def extract_schema(engine):
#     inspector = inspect(engine)
#     tables = inspector.get_table_names()

#     schema_info = []

#     for table in tables:
#         columns = inspector.get_columns(table)
#         for column in columns:
#             schema_info.append({
#                 'Table': table,
#                 'Column': column['name'],
#                 'Type': str(column['type']),
#                 'Nullable': column['nullable'],
#                 'Default': column.get('default')
#             })

#     return pd.DataFrame(schema_info)


connection_string_chinook = f'sqlite:///Chinook.db'
connection_string_northwind = f'sqlite:///northwind.db'

engine_chinook = create_engine(connection_string_chinook)
engine_northwind = create_engine(connection_string_northwind)

# schema_chinook = extract_schema(engine_chinook)
# schema_northwind = extract_schema(engine_northwind)

def get_table_schema(engine, table_name):
    query = f"""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = '{table_name}'
    """
    return pd.read_sql(query, engine)


def extract_features(schema, sample_data):
    features = {}
    
    # Schema features
    features['num_columns'] = len(schema)
    features['column_names'] = " ".join(schema['column_name'])
    features['data_types'] = " ".join(schema['data_type'])
    
    # Statistical features
    for col in sample_data.select_dtypes(include=['float64', 'int64']):
        features[f'{col}_mean'] = sample_data[col].mean()
        features[f'{col}_std'] = sample_data[col].std()
        features[f'{col}_min'] = sample_data[col].min()
        features[f'{col}_max'] = sample_data[col].max()
    
    # Text features
    for col in sample_data.select_dtypes(include=['object']):
        text_data = sample_data[col].dropna().astype(str).tolist()
        if text_data:
            vectorizer = TfidfVectorizer(max_features=100)
            tfidf_matrix = vectorizer.fit_transform(text_data)
            features[f'{col}_tfidf'] = tfidf_matrix.mean(axis=0).tolist()
    
    return features

def calculate_similarity(features_a, features_b, sample_data_a, sample_data_b):
    similarities = {}
    
    for table_a, feat_a in features_a.items():
        for table_b, feat_b in features_b.items():
            # Schema similarity (using Jaccard on data types)
            schema_similarity = 1 - jaccard(feat_a['data_types'], feat_b['data_types'])
            
            # Statistical similarity (using cosine similarity on numerical features)
            num_features_a = [feat_a[f'{col}_mean'] for col in sample_data_a.columns if f'{col}_mean' in feat_a]
            num_features_b = [feat_b[f'{col}_mean'] for col in sample_data_b.columns if f'{col}_mean' in feat_b]
            statistical_similarity = cosine_similarity([num_features_a], [num_features_b])[0][0]
            
            # Text similarity (using cosine similarity on TF-IDF vectors)
            text_similarity = 0
            for col in sample_data_a.select_dtypes(include=['object']):
                if f'{col}_tfidf' in feat_a and f'{col}_tfidf' in feat_b:
                    text_similarity += cosine_similarity([feat_a[f'{col}_tfidf']], [feat_b[f'{col}_tfidf']])[0][0]
            text_similarity /= len(sample_data_a.select_dtypes(include=['object']))
            
            # Average similarity score
            overall_similarity = (schema_similarity + statistical_similarity + text_similarity) / 3
            
            similarities[(table_a, table_b)] = overall_similarity
    
    return similarities

tables_chinook = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'", engine_chinook)
schemas_chinook = {table: get_table_schema(engine_chinook, table) for table in tables_chinook['table_name']}
samples_chinook = {table: get_sample_data(engine_chinook, table) for table in tables_chinook['table_name']}
features_chinook = {table: extract_features(schemas_chinook[table], samples_chinook[table]) for table in tables_chinook['table_name']}

tables_northwind = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'", engine_northwind)
schemas_northwind = {table: get_table_schema(engine_northwind, table) for table in tables_northwind['table_name']}
samples_northwind = {table: get_sample_data(engine_northwind, table) for table in tables_northwind['table_name']}
features_northwind = {table: extract_features(schemas_northwind[table], samples_northwind[table]) for table in tables_northwind['table_name']}

similarities = calculate_similarity(features_chinook, features_northwind, samples_chinook, samples_northwind)

print(similarities)

# schema_chinook.to_csv('schema_chinook.csv', index=False)
# schema_northwind.to_csv('schema_northwind.csv', index=False)

# print("Schema information extracted and saved to CSV files.")
