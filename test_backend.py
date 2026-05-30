import requests
import time
import subprocess
import os
import signal
import sys

# Start the server
server = subprocess.Popen([sys.executable, "main.py"])
print("Waiting for server to start...")
time.sleep(3)

try:
    print("Testing /outreach endpoint...")
    payload = {
        "opportunity_id": 101,
        "candidate_name": "Test Candidate",
        "opportunity": {
            "title": "Senior Python Developer",
            "company": "Tech Corp",
            "match_reasoning": "Strong match based on Python experience."
        },
        "candidate_profile": {
            "core_skills": ["Python", "Django", "FastAPI"],
            "project_descriptions": "Built a highly scalable backend using Python and FastAPI for a fintech startup, improving latency by 40% and handling 10k requests per second."
        }
    }
    
    response = requests.post("http://localhost:8000/outreach", json=payload)
    print("Status Code:", response.status_code)
    
    if response.status_code == 200:
        data = response.json()
        print("Proof Card:")
        print(data.get("proof_card", {}))
    else:
        print("Error:", response.text)

finally:
    # Terminate server
    server.terminate()
    server.wait()
    print("Server terminated.")
