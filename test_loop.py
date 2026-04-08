import requests
import json
import time

url = "https://prabhav1437-corpseql.hf.space"
headers = {"Content-Type": "application/json"}

# Give the space a second in case it was restarting
time.sleep(2)

print("--- RESET ---")
r = requests.post(f"{url}/reset")
print(json.dumps(r.json(), indent=2))

print("\n--- SCAN ---")
r = requests.post(f"{url}/step", json={"action": "scan"})
print(json.dumps(r.json(), indent=2))

print("\n--- INJECT ---")
r = requests.post(f"{url}/step", json={"action": "inject_sql"})
print(json.dumps(r.json(), indent=2))

print("\n--- REPORT ---")
r = requests.post(f"{url}/step", json={"action": "report"})
print(json.dumps(r.json(), indent=2))

print("\n--- PATCH ---")
r = requests.post(f"{url}/step", json={"action": "patch"})
print(json.dumps(r.json(), indent=2))
