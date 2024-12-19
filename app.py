from flask import Flask, request, jsonify
import re

app = Flask(__name__)

SQL_INJECTION_PATTERNS = [
    r"(--|#|;)",                      
    r"(\b(ALTER|DROP|SELECT|INSERT|DELETE|UPDATE|CREATE|WHERE|OR|AND)\b)",  
    r"(\bUNION\b.*\bSELECT\b)",     
    r"(\\x00|\\n|\\r|\\t|\\Z|\\b|\\x20)",   
    r"(\b(1=1|1=0)\b)",              
    r"(\W)"                          
  # r"('|\"|`|\\|\/|\*|\+|\-|=|%|@|!|\^|\(|\)|\[|\]|\{|\}|\<|\>|\?|:|,|\.|\||~|\$)"           
]

def is_sql_injection(input_text):
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, input_text, re.IGNORECASE):
            return True
    return False

@app.route('/v1/sanitized/input/', methods=['POST'])
def sanitize_input():
    try:
        data = request.get_json()
        payload = data.get('payload', '')

        if not data: 
           return jsonify({"error": "Missing payload"}), 400 # Invaid input
        
        if not payload: 
            return jsonify({"result": "unsanitized"}), 200 # Success
        
        if not isinstance(payload, str):
            return jsonify({"error": "Invalid input, payload must be a string"}), 400 # Invaid input

        if is_sql_injection(payload):
            return jsonify({"result": "unsanitized"}), 200 # Success
        else:
            return jsonify({"result": "sanitized"}), 200 # Success
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 # Server side error

if __name__ == '__main__':
    app.run(debug=True)
