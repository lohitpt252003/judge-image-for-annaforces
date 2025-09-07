import unittest
import sys
import os
import json

# Add the parent directory to the path to import execute
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execute import execute_code

class TestCodeExecution(unittest.TestCase):

    def run_test(self, test_name, language, code, stdin, time_limit_s=2, memory_limit_mb=1024):
        print(f"\n--- Running test: {test_name} ---")
        print(f"Input:\n  Language: {language}\n  Time Limit: {time_limit_s}s\n  Memory Limit: {memory_limit_mb}MB")
        print(f"  Code:\n{code}")
        print(f"  Stdin: {stdin}")
        
        result = execute_code(
            language=language, 
            code=code, 
            stdin=stdin, 
            time_limit_s=time_limit_s, 
            memory_limit_mb=memory_limit_mb
        )
        
        print(f"Output:\n{json.dumps(result, indent=2)}")
        print("======================================================================")
        return result

    # --- Hello World Tests ---
    def test_python_hello_world(self):
        result = self.run_test("test_python_hello_world", 'python', '''print("Hello, World!")''', '')
        self.assertTrue(result['success'])
        self.assertEqual(result['stdout'].strip(), "Hello, World!")

    def test_c_hello_world(self):
        result = self.run_test("test_c_hello_world", 'c', '''
#include <stdio.h>
int main() {
    printf("Hello, World!");
    return 0;
}
''', '')
        self.assertTrue(result['success'])
        self.assertEqual(result['stdout'].strip(), "Hello, World!")

    def test_cpp_hello_world(self):
        result = self.run_test("test_cpp_hello_world", 'c++', '''
#include <iostream>
int main() {
    std::cout << "Hello, World!";
    return 0;
}
''', '')
        self.assertTrue(result['success'])
        self.assertEqual(result['stdout'].strip(), "Hello, World!")

    # --- Two Lines Input Tests ---
    def test_python_two_lines_input(self):
        result = self.run_test("test_python_two_lines_input", 'python', '''
line1 = input()
line2 = input()
print(line1)
print(line2)
''', "Hello\nWorld")
        self.assertTrue(result['success'])
        self.assertEqual(result['stdout'].strip().replace('\r\n', '\n'), "Hello\nWorld")

    def test_c_two_lines_input(self):
        result = self.run_test("test_c_two_lines_input", 'c', r'''
#include <stdio.h>
int main() {
    char line1[100], line2[100];
    scanf("%s", line1);
    scanf("%s", line2);
    printf("%s\n%s", line1, line2);
    return 0;
}
''', "Hello\nWorld")
        self.assertTrue(result['success'], msg=f"err: {result['err']}, stderr: {result['stderr']}")
        self.assertEqual(result['stdout'].strip().replace('\r\n', '\n'), "Hello\nWorld")

    def test_cpp_two_lines_input(self):
        result = self.run_test("test_cpp_two_lines_input", 'c++', '''
#include <iostream>
#include <string>
int main() {
    std::string line1, line2;
    std::cin >> line1 >> line2;
    std::cout << line1 << std::endl << line2;
    return 0;
}
''', "Hello\nWorld")
        self.assertTrue(result['success'])
        self.assertEqual(result['stdout'].strip().replace('\r\n', '\n'), "Hello\nWorld")

    # --- Time Limit Exceeded Tests ---
    def test_python_tle(self):
        result = self.run_test("test_python_tle", 'python', '''while True: pass''', '', time_limit_s=1)
        self.assertFalse(result['success'])
        self.assertIn("Time Limit Exceeded", result['err'])

    def test_c_tle(self):
        result = self.run_test("test_c_tle", 'c', '''int main() { while(1); return 0; }''', '', time_limit_s=1)
        self.assertFalse(result['success'])
        self.assertIn("Time Limit Exceeded", result['err'])

    def test_cpp_tle(self):
        result = self.run_test("test_cpp_tle", 'c++', '''int main() { while(true); return 0; }''', '', time_limit_s=1)
        self.assertFalse(result['success'])
        self.assertIn("Time Limit Exceeded", result['err'])

    # --- Memory Limit Exceeded Tests ---
    def test_python_mle(self):
        result = self.run_test("test_python_mle", 'python', '''a = " " * (10**8)''', '', memory_limit_mb=50)
        self.assertFalse(result['success'])
        self.assertIn("Memory Limit Exceeded", result['err'])

    def test_c_mle(self):
        result = self.run_test("test_c_mle", 'c', '''
#include <stdlib.h>
#include <string.h>
int main() {
    size_t size = 200 * 1024 * 1024;
    void *p = malloc(size);
    if (p) {
        memset(p, 0, size);
    }
    return 0;
}
''', '', memory_limit_mb=100)
        self.assertFalse(result['success'])
        self.assertIn("Memory Limit Exceeded", result['err'])

    def test_cpp_mle(self):
        result = self.run_test("test_cpp_mle", 'c++', '''
#include <vector>
#include <iostream>
int main() {
    try {
        std::vector<int> v(50 * 1024 * 1024);
        std::cout << "Allocated" << std::endl;
    } catch (const std::bad_alloc& e) {
        std::cerr << "Allocation failed: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
''', '', memory_limit_mb=100)
        self.assertFalse(result['success'])
        self.assertIn("Memory Limit Exceeded", result['err'])

    # --- Runtime Error Tests ---
    def test_python_runtime_error(self):
        result = self.run_test("test_python_runtime_error", 'python', '''1 / 0''', '')
        self.assertFalse(result['success'])
        self.assertIn("Runtime Error", result['err'])
        self.assertIn("ZeroDivisionError", result['stderr'])

    def test_c_runtime_error(self):
        result = self.run_test("test_c_runtime_error", 'c', '''int main() { int x = 1 / 0; return 0; }''', '')
        self.assertFalse(result['success'])
        self.assertIn("Runtime Error", result['err'])

    def test_cpp_runtime_error(self):
        result = self.run_test("test_cpp_runtime_error", 'c++', '''int main() { int x = 1 / 0; return 0; }''', '')
        self.assertFalse(result['success'])
        self.assertIn("Runtime Error", result['err'])

    # --- Segmentation Fault Tests ---
    def test_c_segfault(self):
        result = self.run_test("test_c_segfault", 'c', '''
#include <stdio.h>
#include <stdlib.h>
int main() { int *p = NULL; *p = 10; return 0; }
''', '')
        self.assertFalse(result['success'])
        self.assertIn("Runtime Error", result['err'])

    def test_cpp_segfault(self):
        result = self.run_test("test_cpp_segfault", 'c++', '''int main() { int *p = nullptr; *p = 10; return 0; }''', '')
        self.assertFalse(result['success'])
        self.assertIn("Runtime Error", result['err'])

    # --- Compilation Error Tests ---
    def test_python_syntax_error(self):
        result = self.run_test("test_python_syntax_error", 'python', r'''print "hello"''', '')
        self.assertFalse(result['success'])
        self.assertIn("Runtime Error", result['err'])
        self.assertIn("SyntaxError", result['stderr'])

    def test_c_compilation_error(self):
        result = self.run_test("test_c_compilation_error", 'c', '''int main() { printf("hello") }''', '')
        self.assertFalse(result['success'])
        self.assertEqual(result['err'], "Compilation Error")

    def test_cpp_compilation_error(self):
        result = self.run_test("test_cpp_compilation_error", 'c++', '''#include <iostream>\nint main() { std::cout << "hello" }''', '')
        self.assertFalse(result['success'])
        self.assertEqual(result['err'], "Compilation Error")

    # --- Performance Tests ---
    def test_fibonacci_performance(self):
        code = '''
def fib(n):
    MOD = 10**9 + 7
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % MOD
    return a

print(fib(1000))
'''
        self.run_test("test_fibonacci_performance", 'python', code, '')

if __name__ == '__main__':
    print("======================================================================")
    print("                     Running Code Execution Tests")
    print("======================================================================")
    unittest.main(verbosity=2)