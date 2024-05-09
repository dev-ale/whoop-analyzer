import json
from fetch_save import fetch_and_save_data
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = FastAPI()
load_dotenv()
scheduler = BackgroundScheduler()

# State variables
app_start_time = datetime.now()
last_fetch_time = None
data_counts = {
    "sleep": 0,
    "workouts": 0,
    "recovery": 0
}


@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(fetch_data, 'interval', hours=1)
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

@app.get("/health")
def get_stats():
    return {
        "application_started": app_start_time,
        "last_fetch_time": last_fetch_time,
        "data_counts": data_counts
    }

@app.get("/fetchdata")
async def fetch_data():
    global last_fetch_time, data_counts
    try:
        # Ideally fetch these from environment variables or a secure config
        username = os.getenv("WHOOP_USERNAME", "default_user")
        password = os.getenv("WHOOP_PASSWORD", "default_pass")
        start_date = "2024-02-26 23:59:59.999999"

        result = fetch_and_save_data(username, password, start_date)

        # Update the last fetch time
        last_fetch_time = datetime.now()

        # Update counts
        data_counts["sleep"] = len(result['sleep'])
        data_counts["workouts"] = len(result['workouts'])
        data_counts["recovery"] = len(result['recovery'])

        return data_counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workouts")
async def read_workouts():
    # Specify the path to your JSON file
    json_file_path = "data/workouts.json"

    # Check if the file exists to prevent errors
    if not os.path.exists(json_file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Read the JSON file
    with open(json_file_path, "r") as file:
        workouts_data = json.load(file)

    # Return the JSON data
    return workouts_data


@app.get("/recovery")
async def read_recovery():
    # Specify the path to your JSON file
    json_file_path = "data/recovery.json"

    # Check if the file exists to prevent errors
    if not os.path.exists(json_file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Read the JSON file
    with open(json_file_path, "r") as file:
        recovery_data = json.load(file)

    # Return the JSON data
    return recovery_data


@app.get("/sleep")
async def read_sleep():
    # Specify the path to your JSON file
    json_file_path = "data/sleep.json"

    # Check if the file exists to prevent errors
    if not os.path.exists(json_file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Read the JSON file
    with open(json_file_path, "r") as file:
        sleep_data = json.load(file)

    # Return the JSON data
    return sleep_data
