import subprocess
import os
import shutil

# DOCKER THINGS
IMAGE_NAME = "my-ubuntu-app"
IMAGE_TAG = "latest"
IMAGE = f"{IMAGE_NAME}:{IMAGE_TAG}"

# TEST FOLDER
TEST_FOLDER = "test"

def create_folder_and_file(folder_name=TEST_FOLDER, file_name='main.py', content='print("\t=== This is the default one\\n\t=== Please change the code")'):
    os.makedirs(folder_name, exist_ok=True)
    with open(f'{folder_name}/{file_name}', 'w') as f:
        f.write(content)
    
    

def delete_folder(folder_name=TEST_FOLDER):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)


# def create_image(IMAGE):
#     # Host directory
#     host_path = os.getcwd()

#     # --- Step 1: Check if image exists ---
#     result = subprocess.run(
#         ["docker", "images", "-q", IMAGE],
#         capture_output=True, text=True
#     )

#     if not result.stdout.strip():
#         print(f"[INFO] Image {IMAGE} not found. Building...")
#         subprocess.run(
#             ["docker", "build", "-t", IMAGE, "."],
#             check=True
#         )
#     else:
#         print(f"[INFO] Image {IMAGE} already exists.")




create_folder_and_file()
delete_folder()
'''

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
'''