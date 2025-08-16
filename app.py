import subprocess
import os

IMAGE_NAME = "my-ubuntu-app"
IMAGE_TAG = "latest"
IMAGE = f"{IMAGE_NAME}:{IMAGE_TAG}"

# Host directory
host_path = os.getcwd()

# --- Step 1: Check if image exists ---
result = subprocess.run(
    ["docker", "images", "-q", IMAGE],
    capture_output=True, text=True
)

if not result.stdout.strip():
    print(f"[INFO] Image {IMAGE} not found. Building...")
    subprocess.run(
        ["docker", "build", "-t", IMAGE, "."],
        check=True
    )
else:
    print(f"[INFO] Image {IMAGE} already exists.")

# --- Step 2: Run container ---
command = [
    "docker", "run",
    "--rm", "-it",
    "-v", f"{host_path}/test:/sandbox/temp",
    "-w", "/sandbox/temp",
    IMAGE,
    "python3", "main.py"
]

print(f"[INFO] Running container with {IMAGE}...")
subprocess.run(command, check=True)
