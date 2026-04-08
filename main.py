from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import psycopg2

app = FastAPI()

DB_URI = "postgresql://postgres.qxpkcayggyiihhwcnhbn:TeyczMNMdAp6l2om@aws-1-eu-west-1.pooler.supabase.com:6543/postgres"

def get_connection():
    return psycopg2.connect(DB_URI)

class Row(BaseModel):
    column01: Optional[int] = None
    column02: Optional[str] = None
    column03: Optional[float] = None
    column04: Optional[str] = None
    column05: Optional[str] = None
    column06: Optional[str] = None
    column07: Optional[float] = None

@app.get("/")
def root():
    return HTMLResponse(open("index.html").read())

@app.get("/data")
def get_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, column01, column02, column03, column04, column05, column06, column07 FROM survey ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "column01": r[1], "column02": r[2], "column03": r[3], "column04": r[4], "column05": r[5], "column06": r[6], "column07": r[7]} for r in rows]

@app.post("/data")
def add_row(row: Row):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO survey (column01, column02, column03, column04, column05, column06, column07) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (row.column01, row.column02, row.column03, row.column04, row.column05, row.column06, row.column07)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Row added successfully!"}