import os
import sys
import requests
import time

def get_sonar_quality_gate_status(project_key, sonar_host_url, sonar_token):
    url = f"{sonar_host_url}/api/qualitygates/project_status?projectKey={project_key}"
    headers = {
        'Authorization': f'Basic {sonar_token.encode("utf-8").hex()}'
    }

    print(f"🔍 Checking Quality Gate for project: {project_key}")
    
    response = requests.get(url, auth=(sonar_token, ''))
    
    if response.status_code != 200:
        print(f"❌ Failed to get quality gate status. HTTP {response.status_code}: {response.text}")
        sys.exit(1)

    data = response.json()
    status = data.get("projectStatus", {}).get("status")

    print(f"📊 Quality Gate Status: {status}")
    return status

def wait_for_analysis(project_key, sonar_host_url, sonar_token, timeout=60):
    """Optional: wait
