from fastapi import FastAPI
import psycopg2

app = FastAPI()

DB_URI = "postgresql://postgres:p4ssw0rd@db.qxpkcayggyiihhwcnhbn.supabase.co:5432/postgres"

def get_connection():
    return psycopg2.connect(DB_URI)

@app.get("/")
def root():
    return {"message": "API is running!"}

@app.get("/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]