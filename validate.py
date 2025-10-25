import subprocess
import tempfile
import os
import uuid

def validate_output(validator_language='python', validator_code='', user_output='', test_input='', time_limit_s=2, memory_limit_mb=1024):
    language = validator_language.lower()
    file_info = {
        'c': {'ext': 'c', 'compiler': 'gcc', 'executable': 'validator.out'},
        'c++': {'ext': 'cpp', 'compiler': 'g++', 'executable': 'validator.out'},
        'python': {'ext': 'py', 'compiler': None, 'executable': 'validator.py'}
    }
    if language not in file_info:
        return {
            "stdout": "", "stderr": "", "err": f"Language '{language}' is not supported.",
            "timetaken": 0, "memorytaken": 0, "success": False
        }

    image_name = "code-runner-image:latest"
    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        image_check = subprocess.run(["docker", "image", "inspect", image_name], check=False, capture_output=True)
        if image_check.returncode != 0:
            return {
                "stdout": "", "stderr": "", "err": f"Docker image '{image_name}' not found.",
                "timetaken": 0, "memorytaken": 0, "success": False
            }
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        error_message = e.stderr.decode('utf-8') if hasattr(e, 'stderr') and e.stderr else str(e)
        return {
            "stdout": "", "stderr": "", "err": f"Docker error: {error_message}",
            "timetaken": 0, "memorytaken": 0, "success": False
        }

    info = file_info[language]
    validator_filename = f"validator.{info['ext']}"
    container_name = f"validator-container-{uuid.uuid4()}"

    with tempfile.TemporaryDirectory() as temp_dir:
        validator_filepath = os.path.join(temp_dir, validator_filename)
        with open(validator_filepath, "w") as f:
            f.write(validator_code)

        user_output_filepath = os.path.join(temp_dir, "user_output.txt")
        with open(user_output_filepath, "w") as f:
            f.write(user_output)

        test_input_filepath = os.path.join(temp_dir, "test_input.txt")
        with open(test_input_filepath, "w") as f:
            f.write(test_input)

        container_id = None
        try:
            run_cmd = [
                "docker", "run",
                "--name", container_name,
                "--memory", f"{memory_limit_mb}m",
                "--memory-swap", f"{memory_limit_mb}m",
                "-d",
                image_name,
                "sleep", "3600"
            ]
            container_id = subprocess.check_output(run_cmd).decode('utf-8').strip()

            subprocess.run(["docker", "cp", validator_filepath, f"{container_id}:/sandbox/temp/{validator_filename}"], check=True)
            subprocess.run(["docker", "cp", user_output_filepath, f"{container_id}:/sandbox/temp/user_output.txt"], check=True)
            subprocess.run(["docker", "cp", test_input_filepath, f"{container_id}:/sandbox/temp/test_input.txt"], check=True)

            if info['compiler']:
                compile_cmd = f"{info['compiler']} -o {info['executable']} {validator_filename}"
                compile_proc = subprocess.run(
                    ["docker", "exec", container_id, "/bin/sh", "-c", compile_cmd],
                    capture_output=True
                )
                if compile_proc.returncode != 0:
                    return {
                        "stdout": "", "stderr": compile_proc.stderr.decode('utf-8'), "err": "Validator Compilation Error",
                        "timetaken": 0, "memorytaken": 0, "success": False
                    }

            exec_path = info['executable']
            if language == 'python':
                run_cmd_main = f"python3 {exec_path} user_output.txt test_input.txt"
            else:
                run_cmd_main = f"./{exec_path} user_output.txt test_input.txt"
            
            run_cmd_container = f"timeout {time_limit_s}s {run_cmd_main}"
            
            exec_proc = subprocess.run(
                ["docker", "exec", container_id, "/bin/sh", "-c", run_cmd_container],
                capture_output=True
            )
            
            exit_code = exec_proc.returncode
            stdout_output = exec_proc.stdout.decode('utf-8')
            stderr_output = exec_proc.stderr.decode('utf-8')

            if exit_code != 0:
                return {
                    "stdout": stdout_output, "stderr": stderr_output, "err": f"Validator Runtime Error (Exit Code: {exit_code})",
                    "timetaken": 0, "memorytaken": 0, "success": False
                }
            else:
                return {
                    "stdout": stdout_output, "stderr": stderr_output, "err": "",
                    "timetaken": 0, "memorytaken": 0, "success": True
                }

        finally:
            if container_id:
                subprocess.run(["docker", "rm", "-f", container_id], capture_output=True)