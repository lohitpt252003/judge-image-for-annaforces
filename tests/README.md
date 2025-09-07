Tests
This directory contains the test suite for the Code Execution Engine. The tests are divided into two main categories:

1. Unit Tests
File: test_execution.py
Description: These tests directly invoke the execute_code function from execute.py. They are designed to verify the core logic of the code execution engine, including language support, resource limits, and error handling, without involving the Flask API.
How to Run:
python -m unittest tests/test_execution.py
2. API Tests
File: test_api.py
Description: These tests interact with the Flask API endpoint (/api/execute). They verify the end-to-end functionality of the system, including the Flask application, request/response handling, and integration with the code execution engine. The API tests automatically start and stop the Flask development server.
How to Run:
python -m unittest tests/test_api.py