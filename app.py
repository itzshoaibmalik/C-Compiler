from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def interpret_c_code(code):
    # Simple C code interpreter for basic operations
    output = []
    
    # Extract printf statements
    printf_pattern = r'printf\s*\(\s*"([^"]*)"\s*\)'
    printf_matches = re.finditer(printf_pattern, code)
    
    for match in printf_matches:
        # Replace \n with actual newlines
        text = match.group(1).replace('\\n', '\n')
        output.append(text)
    
    return '\n'.join(output)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json.get('code', '')
    
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
        output = interpret_c_code(code)
        
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