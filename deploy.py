"""Simple local deployment: copies the app into a versioned release folder
and points a 'current' marker at it, then smoke-tests the deployed copy."""
import os
import shutil
import subprocess
import sys
from datetime import datetime

DEPLOY_ROOT = os.environ.get(
    "DEPLOY_DIR", os.path.join(os.path.expanduser("~"), "jenkins_deploy")
)
FILES = ["app.py", "requirements.txt"]


def deploy():
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    build = os.environ.get("BUILD_NUMBER", stamp)
    release = os.path.join(DEPLOY_ROOT, "releases", f"build-{build}")
    os.makedirs(release, exist_ok=True)
    for f in FILES:
        shutil.copy2(f, release)
    with open(os.path.join(DEPLOY_ROOT, "CURRENT"), "w") as fh:
        fh.write(release + "\n")

    out = subprocess.run(
        [sys.executable, os.path.join(release, "app.py")],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    print(f"Deployed build {build} to {release}")
    print(f"Smoke test output: {out}")
    return release


if __name__ == "__main__":
    deploy()
