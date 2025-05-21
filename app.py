from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def interpret_c_code(code, user_inputs=None):
    if user_inputs is None:
        user_inputs = []
    
    # Simple C code interpreter for basic operations
    output = []
    input_index = 0
    
    # Split code into lines and process sequentially
    lines = code.split('\n')
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('//'):
            continue
            
        # Process printf statements
        printf_match = re.search(r'printf\s*\(\s*"([^"]*)"\s*\)', line)
        if printf_match:
            text = printf_match.group(1).replace('\\n', '\n')
            output.append(text)
            continue
            
        # Process scanf statements
        scanf_match = re.search(r'scanf\s*\(\s*"([^"]*)"\s*,\s*&?(\w+)\s*\)', line)
        if scanf_match:
            if input_index < len(user_inputs):
                # Just add the input value without extra text
                output.append(user_inputs[input_index])
                input_index += 1
            else:
                output.append("Waiting for input")
                break  # Stop processing until we get input
    
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