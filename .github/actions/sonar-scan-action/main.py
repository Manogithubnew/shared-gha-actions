import subprocess
import os
import sys

def run_sonar_scan():
    sonar_token = os.getenv('SONAR_TOKEN')
    sonar_host_url = os.getenv('SONAR_HOST_URL', 'https://your-sonarqube-server.com')
    project_key = os.getenv('SONAR_PROJECT_KEY', 'my-python-app')
    project_name = os.getenv('SONAR_PROJECT_NAME', 'My Python App')
    project_version = os.getenv('SONAR_PROJECT_VERSION', '1.0')

    if not sonar_token:
        print("❌ SONAR_TOKEN environment variable is not set.")
        sys.exit(1)

    sonar_cmd = [
        'sonar-scanner',
        f'-Dsonar.login={sonar_token}',
        f'-Dsonar.projectKey={project_key}',
        f'-Dsonar.projectName={project_name}',
        f'-Dsonar.projectVersion={project_version}',
        '-Dsonar.sources=.',
        '-Dsonar.language=py',
        f'-Dsonar.host.url={sonar_host_url}',
        '-Dsonar.sourceEncoding=UTF-8'
    ]

    try:
        print("🚀 Running SonarQube scan...")
        result = subprocess.run(sonar_cmd, check=True, text=True)
        print("✅ SonarQube scan completed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ SonarQube scan failed.")
        sys.exit(e.returncode)

if __name__ == "__main__":
    run_sonar_scan()
