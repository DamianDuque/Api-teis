from dotenv import load_dotenv
from flask import Flask
import psycopg2
import os

TESTQUERY = """SELECT "ECN", "CensusData", state
	FROM public."CensusForm";"""

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.get("/")
def home():
    return "Hello, world!"

@app.get("/api/room/")
def get_room_all():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(TESTQUERY)
            resultquery = cursor.fetchall()
    return {"result": resultquery}

if __name__ == "__main__":
    app.run(debug=True)
