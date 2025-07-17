import os
import yaml
import json
import re
import subprocess
import sys

def run_cmd(command):
    """Run a shell command and return output or raise error."""
    try:
        print(f"Running: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, check=True, text=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(e.returncode)

def oc_login(api_url, token):
    """Login to OpenShift cluster."""
    return run_cmd(['oc', 'login', api_url, '--token', token, '--insecure-skip-tls-verify=true'])

def oc_project(project_name):
    """Switch to a specific OpenShift project (namespace)."""
    return run_cmd(['oc', 'project', project_name])

def oc_apply(manifest_file):
    """Apply a YAML manifest to deploy resources."""
    return run_cmd(['oc', 'apply', '-f', manifest_file])

def oc_rollout_restart(deployment_name):
    """Restart a deployment to trigger rollout."""
    return run_cmd(['oc', 'rollout', 'restart', f'deployment/{deployment_name}'])

def oc_get_pods(label_selector=None):
    """List pods in the current project."""
    cmd = ['oc', 'get', 'pods']
    if label_selector:
        cmd += ['-l', label_selector]
    return run_cmd(cmd)

# Example helper using yaml and re
def load_yaml_and_replace(file_path, pattern, replacement):
    """Load YAML file, perform a regex replacement on its stringified form, and return updated dict."""
    with open(file_path, 'r') as f:
        content = f.read()
    updated_content = re.sub(pattern, replacement, content)
    return yaml.safe_load(updated_content)

# Example usage
if __name__ == "__main__":
    api_url = os.getenv('OCP_API_URL', 'https://api.your-ocp-cluster.com:6443')
    token = os.getenv('OCP_TOKEN', 'your_token_here')
    project = os.getenv('OCP_PROJECT', 'your-project-name')
    deployment_file = os.getenv('DEPLOY_FILE', 'deployment.yaml')
    deployment_name = os.getenv('DEPLOYMENT_NAME', 'your-deployment-name')

    oc_login(api_url, token)
    oc_project(project)
    oc_apply(deployment_file)
    oc_rollout_restart(deployment_name)
