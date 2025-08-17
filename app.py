import os
import shutil
import subprocess
import tempfile
import logging


# Setup logging
logging.basicConfig(
    filename='judge_runner.log',
    filemode='a',
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG
)

IMAGE_NAME = "judge-image"
IMAGE_TAG = "latest"
IMAGE = f"{IMAGE_NAME}:{IMAGE_TAG}"

TEST_FOLDER = "test"
TEST_FILE = 'main.py'

DEFAULT_COMILE_TIME_LIMIT = 5

def create_folder_and_file(folder_name=TEST_FOLDER, file_name=TEST_FILE, content='print("\\t=== This is the default one\\n\\t=== Please change the code")'):
    try:
        os.makedirs(folder_name, exist_ok=True)
        with open(f'{folder_name}/{file_name}', 'w') as f:
            f.write(content)
        logging.info(f"Created folder '{folder_name}' and file '{file_name}'.")
    except Exception as e:
        logging.error(f"Error creating folder/file: {e}")

def delete_folder(folder_name=TEST_FOLDER):
    try:
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)
            logging.info(f"Deleted folder '{folder_name}'.")
        else:
            logging.info(f"Folder '{folder_name}' does not exist; nothing to delete.")
    except Exception as e:
        logging.error(f"Error deleting folder '{folder_name}': {e}")

def create_image(image=IMAGE):
    try:
        result = subprocess.run(
            ["docker", "images", "-q", image],
            capture_output=True, text=True
        )
        if not result.stdout.strip():
            logging.info(f"Image '{image}' not found. Building...")
            build_proc = subprocess.run(
                ["docker", "build", "-t", image, "."],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logging.info(f"Docker build stdout: {build_proc.stdout.decode(errors='replace')}")
            logging.info(f"Docker build stderr: {build_proc.stderr.decode(errors='replace')}")
        else:
            logging.info(f"Image '{image}' already exists.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Docker build failed: {e.stderr.decode(errors='replace') if e.stderr else str(e)}")
    except Exception as e:
        logging.error(f"Error in create_image: {e}")

def run_code_in_container(
    image=IMAGE,
    file_path=f'{TEST_FOLDER}/{TEST_FILE}',
    language='python',
    stdin='',
    time_limit=1,
    memory_limit=1024
):
    result = {
        'success': False,
        'stdout': '',
        'stderr': '',
        'error': None,
        'safe': True
    }

    language = language.lower()
    compile_cmd = []
    run_cmd = []

    from safe import check_code_safety
    code = open(file_path, 'r').read()

    safety = check_code_safety(file_path, language)
    logging.info(f"Code safety check result: {safety}")

    if not safety['success']:
        result['error'] = 'Code safety check failed: ' + safety['reason']
        result['safe'] = False
        return result


    # Set up the correct command for each language
    if language == 'python':
        run_cmd = ['python3', os.path.basename(file_path)]
    elif language == 'c':
        compile_cmd = ['gcc', os.path.basename(file_path), '-o', 'main']
        run_cmd = ['./main']
    elif language == 'c++':
        compile_cmd = ['g++', os.path.basename(file_path), '-o', 'main']
        run_cmd = ['./main']
    else:
        result['error'] = 'Unsupported language'
        return result

    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copy(file_path, os.path.join(temp_dir, os.path.basename(file_path)))
        container_folder = "/sandbox/temp"
        docker_base = [
            "docker", "run",
            "--rm", "-i",
            f"--memory={memory_limit}m",
            "-v", f"{temp_dir}:{container_folder}",
            "-w", container_folder,
            image
        ]

        # Compile if necessary
        if compile_cmd:
            compile_command = docker_base + compile_cmd
            try:
                subprocess.run(
                    compile_command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    input=stdin.encode() if stdin else None,
                    timeout=DEFAULT_COMILE_TIME_LIMIT,
                    check=True
                )
            except subprocess.CalledProcessError as e:
                result['error'] = 'Compile error: ' + str(e)
                result['stdout'] = e.stdout.decode(errors="replace") if e.stdout else ''
                result['stderr'] = e.stderr.decode(errors="replace") if e.stderr else ''
                return result
            except subprocess.TimeoutExpired:
                result['error'] = 'Compile Time Limit Exceeded'
                return result
            except Exception as e:
                result['error'] = 'Compile exception: ' + str(e)
                return result

        # Run the code
        run_command = docker_base + run_cmd
        try:
            run_proc = subprocess.run(
                run_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                input=stdin.encode() if stdin else None,
                timeout=time_limit,
                check=True
            )
            result['success'] = True
            result['stdout'] = run_proc.stdout.decode(errors="replace")
            result['stderr'] = run_proc.stderr.decode(errors="replace")
        except subprocess.CalledProcessError as e:
            result['error'] = 'Run error: ' + str(e)
            result['stdout'] = e.stdout.decode(errors="replace") if e.stdout else ''
            result['stderr'] = e.stderr.decode(errors="replace") if e.stderr else ''
        except subprocess.TimeoutExpired:
            result['error'] = 'Time Limit Exceeded'
        except Exception as e:
            result['error'] = 'Run exception: ' + str(e)

    return result

if __name__ == "__main__":
    create_folder_and_file()
    create_image()
    print(run_code_in_container())
    delete_folder()