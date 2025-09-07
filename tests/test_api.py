import unittest
import requests
import subprocess
import time
import os
import sys
import json

class TestApiExecution(unittest.TestCase):
    server_process = None

    @classmethod
    def setUpClass(cls):
        # Start the Flask server as a background process
        python_executable = os.path.join(os.path.dirname(__file__), '..', 'venv', 'Scripts', 'python.exe')
        app_file = os.path.join(os.path.dirname(__file__), '..', 'app.py')
        cls.server_process = subprocess.Popen(
            [python_executable, app_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Wait for the server to start
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        # Terminate the server process
        cls.server_process.terminate()
        cls.server_process.wait()

    def run_api_test(self, test_name, language, code, stdin, time_limit=2, memory_limit=1024):
        print(f"\n--- Running API test: {test_name} ---")
        payload = {
            "language": language,
            "code": code,
            "stdin": stdin,
            "timelimit": time_limit,
            "memorylimit": memory_limit
        }
        print(f"Request payload:\n{json.dumps(payload, indent=2)}")
        response = requests.post("http://127.0.0.1:5000/api/execute", json=payload)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        print(f"Response body:\n{json.dumps(result, indent=2)}")
        print("======================================================================")
        return result

    # --- Hello World Tests ---
    def test_api_python_hello_world(self):
        result = self.run_api_test("test_api_python_hello_world", "python", "print('Hello, World!')", "")
        self.assertTrue(result['success'])
        self.assertEqual(result['stdout'].strip(), "Hello, World!")

    def test_api_c_hello_world(self):
        result = self.run_api_test("test_api_c_hello_world", "c", """
#include <stdio.h>
int main() {
    printf(\"Hello, World!\");
    return 0;
}
""", "")
        self.assertTrue(result['success'])
        self.assertEqual(result['stdout'].strip(), "Hello, World!")

    def test_api_cpp_hello_world(self):
        result = self.run_api_test("test_api_cpp_hello_world", "c++", """
#include <iostream>
int main() {
    std::cout << \"Hello, World!\";
    return 0;
}
""", "")
        self.assertTrue(result['success'])
        self.assertEqual(result['stdout'].strip(), "Hello, World!")

    # --- Compilation Error Tests ---
    def test_api_c_compilation_error(self):
        result = self.run_api_test("test_api_c_compilation_error", "c", "int main() { printf('hello') }", "")
        self.assertFalse(result['success'])
        self.assertEqual(result['err'], "Compilation Error")

    def test_api_cpp_compilation_error(self):
        result = self.run_api_test("test_api_cpp_compilation_error", "c++", """
#include <iostream>
int main() { std::cout << \"hello\" }
""", "")
        self.assertFalse(result['success'])
        self.assertEqual(result['err'], "Compilation Error")

    # --- Performance Tests ---
    def test_api_fibonacci_performance(self):
        code = '''
def fib(n):
    MOD = 10**9 + 7
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % MOD
    return a

print(fib(1000))
'''
        result = self.run_api_test("test_api_fibonacci_performance", 'python', code, '')
        self.assertTrue(result['success'])
        try:
            int(result['stdout'].strip())
            is_number = True
        except ValueError:
            is_number = False
        self.assertTrue(is_number)

if __name__ == '__main__':
    print("======================================================================")
    print("                         Running API Tests")
    print("======================================================================")
    unittest.main(verbosity=2)
