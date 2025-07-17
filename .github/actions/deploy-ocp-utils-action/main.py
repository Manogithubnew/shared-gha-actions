import os
import yaml
import json
import re
import time
import sys
import utils.deploy_utils as utils  # Assuming deploy_utils.py is in the utils/ subdirectory

def main():
    # Read environment variables
    api_url = os.getenv('OCP_API_URL')
    token = os.getenv('OCP_TOKEN')
    project = os.getenv('OCP_PROJECT')
    deploy_file = os.getenv('DEPLOY_FILE')
    deployment_name = os.getenv('DEPLOYMENT_NAME')

    # Validate required inputs
    if not all([api_url, token, project, deploy_file, deployment_name]):
        print("❌ Missing one or more required environment variables.")
        print("Required: OCP_API_URL, OCP_TOKEN, OCP_PROJECT, DEPLOY_FILE, DEPLOYMENT_NAME")
        sys.exit(1)

    print("🔐 Logging into OpenShift...")
    utils.oc_login(api_url, token)

    print(f"🔁 Switching to project: {project}")
    utils.oc_project(project)

    print(f"📦 Applying deployment manifest: {deploy_file}")
    utils.oc_apply(deploy_file)

    print(f"🚀 Restarting deployment: {deployment_name}")
    utils.oc_rollout_restart(deployment_name)

    # Optional wait or status check could go here
    time.sleep(3)
    print("📡 Listing pods:")
    utils.oc_get_pods()

    print("✅ Deployment to OpenShift completed successfully!")

if __name__ == "__main__":
    main()
