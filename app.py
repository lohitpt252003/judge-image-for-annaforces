from flask import Flask, request, jsonify
from flask_cors import CORS
from execute import execute_code
from validate import validate_output

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Code Execution API is running"

@app.route('/api/execute', methods=['POST'])
def execute():
    data = request.get_json()
    code = data.get('code')
    language = data.get('language')
    stdin = data.get('stdin', '')
    timelimit = data.get('timelimit', 2) # Default to 2 seconds
    memorylimit = data.get('memorylimit', 1024) # Default to 1024 MB

    if not code or not language:
        return jsonify({'error': 'Code and language are required.'}), 400

    result = execute_code(
        language=language,
        code=code,
        stdin=stdin,
        time_limit_s=timelimit,
        memory_limit_mb=memorylimit
    )

    return jsonify(result)

@app.route('/api/validate', methods=['POST'])
def validate():
    data = request.get_json()
    validator_code = data.get('validator_code')
    validator_language = data.get('validator_language')
    user_output = data.get('user_output')
    test_input = data.get('test_input')

    if not validator_code or not validator_language:
        return jsonify({'error': 'Validator code and language are required.'}), 400

    result = validate_output(
        validator_language=validator_language,
        validator_code=validator_code,
        user_output=user_output,
        test_input=test_input
    )

    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
