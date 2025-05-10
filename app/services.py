import pandas as pd
from io import BytesIO
from fastapi import UploadFile

async def read_excel(file: UploadFile):
    """Reads the uploaded Excel file and returns its content."""
    content = await file.read()
    excel_data = pd.read_excel(BytesIO(content))
    return excel_data

def read_excel_from_path(file_path: str):
    """
    Reads the Excel file from the given file path and returns its content.
    Each sheet is loaded as a DataFrame and stored in a dictionary.
    """
    try:
        excel_data = pd.read_excel(file_path, sheet_name=None, header=None)  # Read all sheets without headers
        return excel_data
    except FileNotFoundError:
        raise FileNotFoundError(f"Excel file not found at path: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading Excel file: {str(e)}")

def parse_excel(data):
    """Parses the Excel data and returns it in a structured format."""
    
    return data.to_dict(orient="records")

def list_tables(data):
    """
    Dynamically lists all meaningful table names in the Excel file.
    Only considers sections with actual content as tables.
    """
    table_names = []
    for sheet_name, sheet_data in data.items():
        # Iterate through the sheet to find potential table names
        for row_index, row in sheet_data.iterrows():
            for cell_index, cell in enumerate(row):
                if isinstance(cell, str) and cell.isupper():  # Check for uppercase text as potential table name
                    cleaned_cell = cell.strip()
                    # Exclude irrelevant labels based on patterns
                    if len(cleaned_cell) > 3 and not cleaned_cell.endswith("=") and " " in cleaned_cell:
                        # Check if the next row or adjacent cells have meaningful content
                        if not sheet_data.iloc[row_index + 1:, :].isnull().all(axis=None):  # Check below the row
                            table_names.append(cleaned_cell)
    return list(table_names)

def get_table_details(data, table_name: str):
    """
    Returns the names of the rows or columns (depending on the structure) for the specified table.
    Handles multiple occurrences of the same table name.
    """
    # Extract the single sheet from the data dictionary
    sheet_name = list(data.keys())[0]  # Get the first (and only) sheet name
    sheet_data = data[sheet_name]  # Get the sheet content as a DataFrame

    # Normalize the table name for comparison
    normalized_table_name = table_name.strip().upper()

    # Debugging: Print the sheet name and table name
    print(f"Processing sheet: {sheet_name}, looking for table: {normalized_table_name}")

    # Identify the start of the table by matching the table name in the sheet
    table_start_row = None
    for row_index, row in sheet_data.iterrows():
        if any(isinstance(cell, str) and cell.strip().upper() == normalized_table_name for cell in row):
            table_start_row = row_index
            break

    if table_start_row is None:
        raise KeyError(f"Table '{table_name}' not found in the sheet.")

    # Debugging: Print the position of the table name
    print(f"Table '{table_name}' found at row {table_start_row}")

    # Extract rows below the table name
    table_content = sheet_data.iloc[table_start_row + 1 :, :]  # Rows below the table name
    first_column = table_content.iloc[:, 0].dropna()  # First column values, dropping NaN

    # Stop extracting when encountering another table name or unrelated content
    row_names = []
    for row_value in first_column:
        if isinstance(row_value, str):
            # Stop if we encounter another table name (uppercase text)
            if row_value.strip().isupper() and row_value.strip().upper() != normalized_table_name:
                break
            row_names.append(row_value.strip())

    # Return the extracted rows for the specified table
    return row_names

def calculate_row_sum(data, table_name: str, row_name: str):
    """
    Calculates the sum of the specified row in all occurrences of the specified table.
    """
    # Normalize the table name and row name for comparison
    normalized_table_name = table_name.strip().upper()
    normalized_row_name = row_name.strip().upper()

    # Extract the single sheet from the data dictionary
    sheet_name = list(data.keys())[0]  # Get the first (and only) sheet name
    sheet_data = data[sheet_name]  # Get the sheet content as a DataFrame

    # Identify all occurrences of the table name in the sheet
    table_start_rows = []
    for row_index, row in sheet_data.iterrows():
        if any(isinstance(cell, str) and cell.strip().upper() == normalized_table_name for cell in row):
            table_start_rows.append(row_index)

    if not table_start_rows:
        raise KeyError(f"Table '{table_name}' not found in the sheet.")

    # Initialize the total sum
    total_sum = 0

    # Process each occurrence of the table
    for table_start_row in table_start_rows:
        # Extract rows below the table name
        table_content = sheet_data.iloc[table_start_row + 1 :, :]  # Rows below the table name
        first_column = table_content.iloc[:, 0].dropna()  # First column values, dropping NaN

        # Find the row matching the row_name
        row_index = None
        for idx, row_value in enumerate(first_column):
            if isinstance(row_value, str) and row_value.strip().upper() == normalized_row_name:
                row_index = table_start_row + 1 + idx
                break

        if row_index is not None:
            # Extract the row data (excluding the first column, which contains the row name)
            row_data = sheet_data.iloc[row_index, 1:]

            # Filter out non-numeric values
            numeric_row_data = pd.to_numeric(row_data, errors='coerce').dropna()

            # Calculate the sum of the numeric values and add to the total sum
            total_sum += numeric_row_data.sum()

    if total_sum == 0:
        raise KeyError(f"Row '{row_name}' not found in any occurrence of table '{table_name}'.")

    return int(total_sum)