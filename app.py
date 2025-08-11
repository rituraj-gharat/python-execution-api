from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
import json
import ast
import sys
from io import StringIO
import contextlib
import traceback

app = Flask(__name__)

def validate_script(script):
    """Validate that the script contains a main() function and returns JSON"""
    try:
        # Parse the script to check for main function
        tree = ast.parse(script)
        
        # Check if main function exists
        has_main = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'main':
                has_main = True
                break
        
        if not has_main:
            return False, "Script must contain a function named 'main()'"
        
        return True, None
    except SyntaxError as e:
        return False, f"Invalid Python syntax: {str(e)}"

def execute_script_safely(script):
    """Execute the script in a safe environment with security measures"""
    try:
        # Create a temporary file for the script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script)
            script_path = f.name
        
        # Prepare command for safe execution with timeout
        cmd = ['timeout', '30', 'python3', script_path]
        
        # Execute with security measures
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=35,  # Additional timeout as backup
            cwd='/tmp',
            env={
                'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
                'PYTHONPATH': '/usr/lib/python3/dist-packages:/usr/local/lib/python3.9/dist-packages',
                'HOME': '/tmp'
            }
        )
        
        # Clean up temporary file
        os.unlink(script_path)
        
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return -1, "", "Execution timeout exceeded"
    except Exception as e:
        return -1, "", f"Execution error: {str(e)}"

def extract_main_result(stdout):
    """Extract the result from main() function execution"""
    try:
        # Look for JSON result in stdout
        lines = stdout.strip().split('\n')
        for line in reversed(lines):  # Start from the end
            line = line.strip()
            if line and line.startswith('{') and line.endswith('}'):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        return None
    except Exception:
        return None

@app.route('/execute', methods=['POST'])
def execute():
    """Execute Python script and return main() function result"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        if not data or 'script' not in data:
            return jsonify({'error': 'Request must contain "script" field'}), 400
        
        script = data['script']
        if not isinstance(script, str) or not script.strip():
            return jsonify({'error': 'Script must be a non-empty string'}), 400
        
        # Validate script structure
        is_valid, error_msg = validate_script(script)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Execute script safely
        return_code, stdout, stderr = execute_script_safely(script)
        
        if return_code != 0:
            return jsonify({
                'error': f'Script execution failed: {stderr}',
                'stdout': stdout
            }), 400
        
        # Extract main() function result
        result = extract_main_result(stdout)
        if result is None:
            return jsonify({
                'error': 'main() function must return valid JSON',
                'stdout': stdout
            }), 400
        
        return jsonify({
            'result': result,
            'stdout': stdout
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False) 