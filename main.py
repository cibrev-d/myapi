from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import psycopg2

app = FastAPI()

DB_URI = "postgresql://postgres.qxpkcayggyiihhwcnhbn:YOUR_PASSWORD@aws-1-eu-west-1.pooler.supabase.com:6543/postgres"

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

@app.get("/dashboard")
def dashboard():
    return HTMLResponse(open("dashboard.html").read())

@app.get("/stats")
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total_rows, AVG(column01) as avg_column01, AVG(column03) as avg_column03, AVG(column07) as avg_column07, MIN(column01) as min_column01, MAX(column01) as max_column01, MIN(column03) as min_column03, MAX(column03) as max_column03, MIN(column07) as min_column07, MAX(column07) as max_column07 FROM survey")
    stats = cursor.fetchone()
    cursor.execute("SELECT column04, COUNT(*) FROM survey GROUP BY column04")
    coffee_tea = cursor.fetchall()
    cursor.execute("SELECT column05, COUNT(*) FROM survey GROUP BY column05")
    football = cursor.fetchall()
    cursor.execute("SELECT column06, COUNT(*) FROM survey GROUP BY column06")
    alcohol = cursor.fetchall()
    cursor.close()
    conn.close()
    return {
        "total_rows": stats[0],
        "avg_column01": round(stats[1], 2) if stats[1] else None,
        "avg_column03": round(stats[2], 2) if stats[2] else None,
        "avg_column07": round(stats[3], 2) if stats[3] else None,
        "min_column01": stats[4], "max_column01": stats[5],
        "min_column03": round(stats[6], 2) if stats[6] else None,
        "max_column03": round(stats[7], 2) if stats[7] else None,
        "min_column07": round(stats[8], 2) if stats[8] else None,
        "max_column07": round(stats[9], 2) if stats[9] else None,
        "coffee_tea": [{"label": r[0], "count": r[1]} for r in coffee_tea],
        "football": [{"label": r[0], "count": r[1]} for r in football],
        "alcohol": [{"label": r[0], "count": r[1]} for r in alcohol],
    }