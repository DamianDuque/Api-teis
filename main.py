from dotenv import load_dotenv
from flask import Flask, request
import psycopg2
import os
import querys

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.get("/")
def home():
    return "Hello, world!"

@app.get("/api/status/<string:cwlcc>")
def get_status(cwlcc):
    with connection:
        with connection.cursor() as cursor:
            query = querys.getstates()
            cursor.execute(query, (cwlcc,))
            resultquery = cursor.fetchall()
    return {"result": resultquery}


@app.put("/api/update_cfn")
def update_cfn():
    try:
        # Get data from the request
        data = request.json

        with connection:
            with connection.cursor() as cursor:
                for key, values in data.items():
                    # Extract PD_id and CFN values for each entry
                    pd_id = values.get("PD_id")
                    cfn = values.get("CFN")

                    # Execute the update query with parameters for each entry
                    query = querys.update_CFN()
                    cursor.execute(query, (cfn, pd_id))
                
        return {"message": "CFN values updated successfully"}
    
    except Exception as e:
        return {"error": str(e)}
    

@app.put("/api/update_state")
def update_state():
    try:
        # Get PD_id and State values from the request
        data = request.json

        with connection:
            with connection.cursor() as cursor:
                for key, values in data.items():
                    state = values.get("State")
                    pd_id = values.get("PD_id")


                    query = querys.update_state()
                    # Execute the update query with parameters for each entry
                    cursor.execute(query, (state, pd_id))
                
        return {"message": "State updated successfully"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True)

