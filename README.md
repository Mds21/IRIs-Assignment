# Excel Table Processing API

## Overview

This API provides functionality to process Excel files, extract table details, and calculate the sum of specific rows within tables. Built with **FastAPI**, it utilizes **Pandas** for Excel data processing.

> **Base URL:** `http://localhost:9090`

---

## Features

- **List Tables:**  
  Automatically detects and lists table names by identifying uppercase headers and validating associated content.

- **Get Table Details:**  
  Retrieves rows or columns associated with a given table name, including multiple occurrences.

- **Calculate Row Sum:**  
  Calculates the sum of numeric values in a specific row across one or more occurrences of the table.

---

## Endpoints

### 1. List Tables

- **Endpoint:** `/list_tables`  
- **Method:** `GET`  
- **Description:** Lists all detected table names from the Excel file.  

**Response Example:**
```json
{
  "tables": ["INITIAL INVESTMENT", "OPERATING CASHFLOWS", "GROWTH RATES"]
}
```

---

### 2. Get Table Details

- **Endpoint:** `/get_table_details`  
- **Method:** `POST`  
- **Parameters:**  
  - `table_name` (string): The name of the table to retrieve details for.  

- **Description:** Retrieves the rows or columns associated with the specified table.  

**Request Example:**
```json
{
  "table_name": "INITIAL INVESTMENT"
}
```

**Response Example:**
```json
{
  "table_name": "INITIAL INVESTMENT",
  "row_names": [
    "Initial Investment=",
    "Opportunity cost (if any)=",
    "Lifetime of the investment",
    "Salvage Value at end of project=",
    "Deprec. method(1:St.line;2:DDB)=",
    "Tax Credit (if any )=",
    "Other invest.(non-depreciable)="
  ]
}
```

---

### 3. Calculate Row Sum

- **Endpoint:** `/row_sum`  
- **Method:** `POST`  
- **Parameters:**  
  - `table_name` (string): The name of the table containing the row.  
  - `row_name` (string): The name of the row to calculate the sum for.  

- **Description:** Calculates the sum of numeric values in the specified row for the given table. If the table name occurs multiple times, it sums the row values across all occurrences.  

**Request Example:**
```json
{
  "table_name": "INITIAL INVESTMENT",
  "row_name": "Investment"
}
```

**Response Example:**
```json
{
  "table_name": "INITIAL INVESTMENT",
  "row_name": "Investment",
  "sum": 50000
}
```

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mds21/IRIs-Assignment.git
   cd IRIs-Assignment
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the application:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 9090 --reload
   ```

2. **Access the API:**
   Open your browser and navigate to `http://localhost:9090/docs` to view the interactive API documentation.

---

## Error Handling

- **File Not Found:** Returns a `404` error if the specified Excel file is not found.
- **Table Not Found:** Returns a `404` error if the specified table name is not found in the Excel file.
- **Row Not Found:** Returns a `404` error if the specified row name is not found in the table.
- **Invalid Data:** Handles non-numeric values gracefully by ignoring them during calculations.

---

## Dependencies

- **FastAPI**: For building the API.
- **Pandas**: For data manipulation.
- **Uvicorn**: For running the FastAPI application.

---

## Future Enhancements

- Add support for Excel files with headers.
- Implement advanced filtering for table and row identification.
- Add support for handling merged cells in Excel.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.