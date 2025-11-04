# Code Execution Engine

## Project Overview

This project is a simple and robust code execution engine built with Flask and Docker. It provides a secure environment to execute code in different languages with resource constraints (time and memory limits).

## Features

- **Secure Execution:** Code is executed in an isolated Docker container to prevent any harm to the host system.
- **Language Support:** Supports C, C++, and Python.
- **Resource Limits:** Enforces time and memory limits on code execution.
- **Custom Output Validation:** Supports custom validator scripts to check the correctness of the user's output.
- **Comprehensive Test Suite:** Includes unit and API tests to ensure reliability.

## API Endpoint

### `/api/execute`

This is the main endpoint to submit code for execution.

- **Method:** `POST`
- **Content-Type:** `application/json`

#### Request Payload

| Field         | Type    | Required | Description                                      |
|---------------|---------|----------|--------------------------------------------------|
| `language`    | string  | Yes      | The programming language (`c`, `c++`, `python`).   |
| `code`        | string  | Yes      | The source code to execute.                      |
| `stdin`       | string  | No       | Standard input for the code. Defaults to empty.  |
| `timelimit`   | integer | No       | Time limit in seconds. Defaults to 2.            |
| `memorylimit` | integer | No       | Memory limit in megabytes. Defaults to 1024.     |

**Example Request:**

```json
{
    "language": "python",
    "code": "print('Hello, World!')",
    "stdin": "",
    "timelimit": 5,
    "memorylimit": 128
}
```

#### Response Payload

The API returns a JSON object with the execution results.

| Field         | Type    | Description                                                                 |
|---------------|---------|-----------------------------------------------------------------------------|
| `success`     | boolean | `true` if the code executed successfully, `false` otherwise.                |
| `stdout`      | string  | The standard output of the code.                                            |
| `stderr`      | string  | The standard error of the code.                                             |
| `err`         | string  | A high-level error message (e.g., "Compilation Error", "Time Limit Exceeded"). |
| `timetaken`   | float   | The time taken for the code to execute in seconds.                          |
| `memorytaken` | float   | The memory consumed by the code in megabytes.                               |

**Example Response (Success):**

```json
{
    "success": true,
    "stdout": "Hello, World!\n",
    "stderr": "",
    "err": "",
    "timetaken": 0.01,
    "memorytaken": 7.6
}
```

**Example Response (Error):**

```json
{
    "success": false,
    "stdout": "",
    "stderr": "Traceback (most recent call last):\n  File \"/sandbox/temp/solution.py\", line 1, in <module>\n    1 / 0\nZeroDivisionError: division by zero\nCommand exited with non-zero status 1",
    "err": "Runtime Error (Exit Code: 1)",
    "timetaken": 0.02,
    "memorytaken": 7.5
}
```

### `/api/validate`

This endpoint validates a user's output using a custom validator script. A blueprint for creating new validators is available in the `DATA/blueprint/validator` directory.

- **Method:** `POST`
- **Content-Type:** `application/json`

#### Request Payload

| Field                | Type   | Required | Description                                          |
| -------------------- | ------ | -------- | ---------------------------------------------------- |
| `validator_language` | string | Yes | The language of the validator script (c, c++, python). |
| `validator_code`     | string | Yes      | The source code of the validator script.             |
| `user_output`        | string | Yes      | The `stdout` from the user's code execution.         |
| `test_input`         | string | Yes      | The original `stdin` for the test case.              |

**Example Request:**

```json
{
    "validator_language": "python",
    "validator_code": "import sys\n\ndef validate(user_output_content, test_input_content):\n    # Your validation logic here\n    # Compare user_output_content with expected output derived from test_input_content\n    # Print \"Accepted\" or \"Wrong Answer\"\n    if user_output_content.strip() == test_input_content.strip():\n        print(\"Accepted\")\n    else:\n        print(\"Wrong Answer\")\n\nif __name__ == \"__main__\":\n    user_output_file = sys.argv[1]\n    test_input_file = sys.argv[2]\n    with open(user_output_file, 'r') as f:\n        user_output = f.read()\n    with open(test_input_file, 'r') as f:\n        test_input = f.read()\n    validate(user_output, test_input)\n",
    "user_output": "expected output",
    "test_input": "input data"
}
```

#### Response Payload

The API returns a JSON object with the validation results.

| Field    | Type    | Description                                         |
| -------- | ------- | --------------------------------------------------- |
| `success`  | boolean | `true` if the validator executed successfully.      |
| `stdout`   | string  | The `stdout` of the validator (e.g., "Accepted").   |
| `stderr`   | string  | The `stderr` of the validator.                      |
| `err`      | string  | A high-level error message (e.g., "Validator Runtime Error"). |

**Example Response (Success):**

```json
{
    "success": true,
    "stdout": "Accepted\n",
    "stderr": "",
    "err": ""
}
```

## Supported Languages

- C (`c`)
- C++ (`c++`)
- Python (`python`)

## How to Run

### 1. Installation

First, make sure you have Docker installed and running.

Then, install the required Python packages using pip:

```bash
# Make sure you are in the project root directory
# and you have activated your virtual environment

pip install -r requirements.txt
```

### 2. Running the Application

To start the Flask application directly, run:

```bash
python app.py
```

The server listens on `http://127.0.0.1:5002` (container exposes port 5002).

### With Docker Compose (recommended)

This repository is integrated in the root `docker-compose.yml` as service `judge`:

```yaml
  judge:
    build:
      context: ./judge-image-for-annaforces
      dockerfile: Dockerfile
    container_name: annaforces-judge
    ports:
      - "5002:5002"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

The socket mount allows the judge to start ephemeral sandbox containers for user code execution. Bring everything up from the repo root:

```bash
docker compose up -d --build
```

Inside the Compose network the backend reaches the judge at `http://judge:5002`.

### Independent Deployment (production)

- Host this service on a VM/host with Docker available so it can launch sandbox containers for user code.
- Expose port `5002` (or place behind a reverse proxy) and secure with TLS (e.g., `https://judge.example.com`).
- No database required; the API is stateless.

Note: Many managed container platforms do not allow mounting `/var/run/docker.sock`. Prefer a VM, or run an alternative sandbox mechanism compatible with the platform.
## How to Run Tests

The project comes with a comprehensive test suite to ensure everything is working correctly. For detailed information on running and understanding the tests, please refer to the [Tests README](tests/README.md).

## Credits and Contributions

This project was developed by Lohit P Talavar.

### Authors

We welcome contributions! If you'd like to contribute, please refer to our `CONTRIBUTING.md` (if available) or open an issue/pull request on the GitHub repository.

Here are some of the key Authors to this project:

*   [Lohit P Talavar](https://github.com/lohitpt252003)
*   [Adarsh Mishra](https://github.com/adarshmishra121)
*   [Priyanshi Meena](https://github.com/MeenaPriyanshi)
