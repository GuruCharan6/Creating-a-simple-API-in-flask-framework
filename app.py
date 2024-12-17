from flask import Flask, request, jsonify
import re

app = Flask(__name__)
def is_sanitized(input_str):
    sql_patterns = [
        r"(--|;|\b(OR|AND|SELECT|INSERT|DELETE|UPDATE|DROP|UNION)\b)",
        r"(=|#|\bWHERE\b|\bLIKE\b|\bFROM\b|\bTABLE\b)"
    ]
    for pattern in sql_patterns:
        if re.search(pattern, input_str, re.IGNORECASE):
            return False
    return True

@app.route('/v1/sanitized/input/',methods=['POST'])
def sanitize_input():
    data = request.get_json()
    payload = data.get("payload","")

    if is_sanitized(payload):
        return jsonify({"result":"sanitized"})
    else:
        return jsonify({"result":"unsanitized"})

if __name__ == '__main__':
    app.run(debug=True)
