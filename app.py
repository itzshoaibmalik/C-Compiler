from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def interpret_c_code(code, user_inputs=None):
    if user_inputs is None:
        user_inputs = []
    
    # Simple C code interpreter for basic operations
    output = []
    input_index = 0
    
    # Extract printf statements
    printf_pattern = r'printf\s*\(\s*"([^"]*)"\s*\)'
    printf_matches = re.finditer(printf_pattern, code)
    
    # Extract scanf statements
    scanf_pattern = r'scanf\s*\(\s*"([^"]*)"\s*,\s*&?(\w+)\s*\)'
    scanf_matches = re.finditer(scanf_pattern, code)
    
    # Process printf statements
    for match in printf_matches:
        # Replace \n with actual newlines
        text = match.group(1).replace('\\n', '\n')
        output.append(text)
    
    # Process scanf statements
    for match in scanf_matches:
        format_str = match.group(1)
        var_name = match.group(2)
        
        if input_index < len(user_inputs):
            # Add the input value to output
            output.append(f"Input for {var_name}: {user_inputs[input_index]}")
            input_index += 1
        else:
            output.append(f"Waiting for input for {var_name}")
    
    return '\n'.join(output)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json.get('code', '')
    user_inputs = request.json.get('inputs', [])
    
    try:
        # Basic validation
        if not code.strip():
            return jsonify({
                'success': False,
                'error': 'Empty code provided'
            })
        
        # Check for basic C syntax
        if not '#include <stdio.h>' in code:
            return jsonify({
                'success': False,
                'error': 'Missing #include <stdio.h>'
            })
        
        if 'main()' not in code and 'main(void)' not in code:
            return jsonify({
                'success': False,
                'error': 'Missing main() function'
            })
        
        # Interpret the code
        output = interpret_c_code(code, user_inputs)
        
        return jsonify({
            'success': True,
            'output': output,
            'error': None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interpreting code: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True) 