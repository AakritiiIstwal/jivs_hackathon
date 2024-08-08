import pandas as pd

def process_csv(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Group the DataFrame by the 'Table' column
    grouped = df.groupby('Table')
    # Create a list to store the combined results
    combined_rows = []
    # Create a new DataFrame to store the combined results
    combined_df = pd.DataFrame(columns=['Table', 'Columns'])

    for table_name, group in grouped:
        # Combine the column details into a single string for each table
        columns_info = []
        for _, row in group.iterrows():
            column_info = f"{row['Column']} {row['Type']}"
            # if pd.notna(row['Default']):
            #     column_info += f" DEFAULT {row['Default']}"
            columns_info.append(column_info)

        combined_row = {
            'Table': table_name,
            'Columns': ', '.join(columns_info)
        }
         # Append the combined row to the list
        combined_rows.append(combined_row)

    # Convert the list of combined rows to a DataFrame
    combined_df = pd.DataFrame(combined_rows, columns=['Table', 'Columns'])

    return combined_df

def main():
    # Path to your CSV file
    file_path = 'schema_chinook.csv'

    # Process the CSV file
    result_df = process_csv(file_path)

    # Display the result
    print(result_df.head())
    result_df.to_csv(f'flattened_{file_path}', index=False)
    print("Flattened out file ", file_path)

if __name__ == "__main__":
    main()
