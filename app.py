from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json.get('code', '')
    
    # Create a temporary file for the C code
    with tempfile.NamedTemporaryFile(suffix='.c', delete=False) as temp_file:
        temp_file.write(code.encode())
        temp_file_path = temp_file.name
    
    try:
        # Compile the C code
        compile_result = subprocess.run(['gcc', temp_file_path, '-o', temp_file_path + '.exe'], 
                                     capture_output=True, text=True)
        
        if compile_result.returncode != 0:
            return jsonify({
                'success': False,
                'error': compile_result.stderr
            })
        
        # Run the compiled program
        run_result = subprocess.run([temp_file_path + '.exe'], 
                                  capture_output=True, text=True)
        
        return jsonify({
            'success': True,
            'output': run_result.stdout,
            'error': run_result.stderr
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
    finally:
        # Clean up temporary files
        try:
            os.unlink(temp_file_path)
            os.unlink(temp_file_path + '.exe')
        except:
            pass

if __name__ == '__main__':
    app.run(debug=True) 