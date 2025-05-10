from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services import read_excel_from_path, parse_excel, list_tables, get_table_details, calculate_row_sum

router = APIRouter()

FILE_PATH = "Data/capbudg.xls"  # Path to the Excel file


@router.get("/list_tables")
async def list_tables_endpoint():
    try:
        data = read_excel_from_path(FILE_PATH)
        tables = list_tables(data)
        return {"tables": tables}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Excel file not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get_table_details")
async def get_table_details_endpoint(table_name: str):
    """
    Retrieves the details (row names) for the specified table.
    """
    try:
        data = read_excel_from_path(FILE_PATH)
        
        # Debugging: Print the keys in the data dictionary
        print("Available tables:", list(data.keys()))
        
        row_names = get_table_details(data, table_name)
        return {"table_name": table_name, "row_names": row_names}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/row_sum")
async def row_sum_endpoint(table_name: str, row_name: str):
    """
    Calculates the sum of the specified row in the specified table.
    """
    try:
        data = read_excel_from_path(FILE_PATH)
        row_sum = calculate_row_sum(data, table_name, row_name)
        return {"table_name": table_name, "row_name": row_name, "sum": row_sum}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' or row '{row_name}' not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))