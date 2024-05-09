import json
from whoop import WhoopClient

def fetch_and_save_data(username, password, start_date):
    with WhoopClient(username, password) as client:
        workouts = client.get_workout_collection(start_date=start_date)
        recovery = client.get_recovery_collection(start_date=start_date)
        sleep = client.get_sleep_collection(start_date=start_date)

    # Save to files
    with open("data/workouts.json", "w") as f:
        json.dump(workouts, f, indent=4)
    with open("data/recovery.json", "w") as f:
        json.dump(recovery, f, indent=4)
    with open("data/sleep.json", "w") as f:
        json.dump(sleep, f, indent=4)

    # Return data for state update
    return {
        "workouts": workouts,
        "recovery": recovery,
        "sleep": sleep
    }