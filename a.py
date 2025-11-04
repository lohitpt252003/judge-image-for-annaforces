from validate import validate_output

def test():
    validator_code = r'''#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <vector>

void to_lower(std::string& s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c){ return std::tolower(c); });
}

std::string trim(const std::string& str) {
    size_t first = str.find_first_not_of(" \t\n\r");
    if (std::string::npos == first) {
        return str;
    }
    size_t last = str.find_last_not_of(" \t\n\r");
    return str.substr(first, (last - first + 1));
}

std::string f(int n) {
    return (n % 2 != 0) ? "YES" : "NO";
}

void validate(const std::string& user_output, const std::string& test_input) {
    try {
        int n = std::stoi(trim(test_input));
        std::string expected = f(n);
        std::string user_output_copy = trim(user_output);

        to_lower(expected);
        to_lower(user_output_copy);

        if (user_output_copy == expected) {
            std::cout << "ACCEPTED" << std::endl;
        } else {
            std::cout << "WRONG ANSWER" << std::endl;
        }
    } catch (const std::exception& e) {
        // Do nothing
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        return 1;
    }

    std::ifstream user_output_file(argv[1]);
    std::ifstream test_input_file(argv[2]);

    if (!user_output_file.is_open() || !test_input_file.is_open()) {
        return 1;
    }

    std::string user_output((std::istreambuf_iterator<char>(user_output_file)),
                             std::istreambuf_iterator<char>());
    std::string test_input((std::istreambuf_iterator<char>(test_input_file)),
                            std::istreambuf_iterator<char>());

    validate(user_output, test_input);

    return 0;
}
'''
    user_output = "no"
    test_input = "10"
    
    result = validate_output(
        validator_language='c++',
        validator_code=validator_code,
        user_output=user_output,
        test_input=test_input
    )

    print(result)


test()