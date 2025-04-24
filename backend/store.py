from backend.oram_core.path_oram import PathORAM   # NEW
oram = PathORAM(n_blocks=64)                       # Example: 64 logical blocks

from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate and store encryption key (do this once and save it securely)
key = Fernet.generate_key()
cipher = Fernet(key)

# store = {}

@app.route('/put', methods=['POST'])
def put():
    data = request.get_json()
    key = int(data['key'])  # Expect numeric keys for ORAM
    value = data['value']
    oram.write(key, value)
    return jsonify({"status": "success", "message": f"Data stored at key {key}"})

@app.route('/get/<key>', methods=['GET'])
def get(key):
    try:
        index = int(key)  # ORAM uses numeric indices
        value = oram.read(index)  # Get from ORAM, not store[]
        if value is None:
            return jsonify({"error": "Key not found"}), 404
        return jsonify({"value": value})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/debug/logs', methods=['GET'])
def debug_logs():
    return jsonify({"access_log": oram.get_access_log()})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
