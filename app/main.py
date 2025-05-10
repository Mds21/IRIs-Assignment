from fastapi import FastAPI
from app.routers import excel

app = FastAPI()

app.include_router(excel.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Excel Processing App!"}