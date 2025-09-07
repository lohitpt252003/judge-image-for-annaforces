# Code Execution Engine

## Project Overview

This project is a simple and robust code execution engine built with Flask and Docker. It provides a secure environment to execute code in different languages with resource constraints (time and memory limits).

## Features

- **Secure Execution:** Code is executed in an isolated Docker container to prevent any harm to the host system.
- **Language Support:** Supports C, C++, and Python.
- **Resource Limits:** Enforces time and memory limits on code execution.
- **Simple API:** A single API endpoint to submit code for execution.
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

To start the Flask application, run the following command:

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000`.

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
