from dotenv import load_dotenv
from flask import Flask, request
import psycopg2
import os

GETSTATES = """SELECT cf."state", pd."PD_id"
FROM public."CensusForm" cf
JOIN public."CensusRespondent" cr ON cf."ECN" = cr."CensusForm_ECN"
JOIN public."PrivateDwelling" pd ON cr."PrivateDwelling_PD_id" = pd."PD_id"
JOIN public."CensusCollector" cc ON pd."CensusCollector_CWL" = cc."CWL"
WHERE cc."CWL" = %s;"""

UPDATE_CFN_QUERY = """UPDATE public."PrivateDwelling"
                     SET "CFN" = %s
                     WHERE "PD_id" = %s;"""

UPDATE_STATE_QUERY = """UPDATE public."CensusForm"
SET "state" = %s
FROM public."CensusRespondent" cr
JOIN public."PrivateDwelling" pd ON cr."PrivateDwelling_PD_id" = %s
WHERE cr."CensusForm_ECN" = public."CensusForm"."ECN"
  AND pd."PD_id" = '1';"""

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
            cursor.execute(GETSTATES, (cwlcc,))
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
                    cursor.execute(UPDATE_CFN_QUERY, (cfn, pd_id))
                
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
                    

                    # Execute the update query with parameters for each entry
                    cursor.execute(UPDATE_STATE_QUERY, (state, pd_id))
                
        return {"message": "State updated successfully"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True)

