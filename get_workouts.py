import json
from whoop import WhoopClient

username = "ale.iphone@gmail.com"
password = ""

start_date="2024-02-26 23:59:59.999999"

print("Get workouts...")
with WhoopClient(username, password) as client:
    workouts = client.get_workout_collection(start_date=start_date)
    recovery = client.get_recovery_collection(start_date=start_date)
    sleep = client.get_sleep_collection(start_date=start_date)

with open("workouts.json", "w") as f:
    json.dump(workouts, f, indent=4)

with open("recovery.json", "w") as f:
    json.dump(recovery, f, indent=4)

with open("sleep.json", "w") as f:
    json.dump(sleep, f, indent=4)

print(f"Found {len(workouts)} workouts and saved it to `workouts.json`")
print(f"Found {len(recovery)} recovery data and saved it to `recovery.json`")
print(f"Found {len(sleep)} sleep data and saved it to `sleep.json`")