from app import create_folder_and_file, create_image, run_code_in_container, delete_folder

cpp_code = (
    '#include <bits/stdc++.h>\n'
    'using namespace std;\n'
    'int main() {\n'
    '    cout << "Hello, World!\\n";\n'
    '    string str; cin >> str; cout << str << endl; return 0;\n'
    '}\n'
)

create_folder_and_file(file_name='main.cpp', content=cpp_code)
create_image()
print(run_code_in_container(language='c++', file_path='test/main.cpp', stdin='10'))
delete_folder()