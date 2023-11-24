from dotenv import load_dotenv
from flask import Flask
import psycopg2
import os


TESTQUERY = """SELECT * FROM "public"."CensusCollector";"""


load_dotenv()


app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.get("/")
def home():
    return "Hello, world!"

@app.get("/api/room/")
def get_room_all(room_id):
    with connection:
        with connection.cursor() as cursor:
            ECNnum = cursor.execute(TESTQUERY)
    return {"name": ECNnum}

if __name__ == "__main__":
    app.run(debug=True)