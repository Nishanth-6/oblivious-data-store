from backend.persistence import save_recursive_oram, load_recursive_oram
from backend.oram_core.recursive_oram import RecursivePathORAM

oram = RecursivePathORAM(n_blocks=64)

from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate and store encryption key (do this once and save it securely)
key = Fernet.generate_key()
cipher = Fernet(key)

# store = {}


@app.route("/put", methods=["POST"])
def put():
    data = request.get_json()
    key = int(data["key"])  # Expect numeric keys for ORAM
    value = data["value"]
    oram.write(key, value)
    return jsonify({"status": "success", "message": f"Data stored at key {key}"})


@app.route("/get/<key>", methods=["GET"])
def get(key):
    try:
        index = int(key)  # ORAM uses numeric indices
        value = oram.read(index)  # Get from ORAM, not store[]
        if value is None:
            return jsonify({"error": "Key not found"}), 404
        return jsonify({"value": value})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/debug/logs", methods=["GET"])
def debug_logs():
    return jsonify({"access_log": oram.get_access_log()})


@app.route("/save", methods=["POST"])
def save_state():
    success = save_recursive_oram(oram)
    return jsonify({"status": "saved" if success else "failed"})


@app.route("/load", methods=["POST"])
def load_state():
    success = load_recursive_oram(oram)
    return jsonify({"status": "loaded" if success else "file_not_found"})


@app.route("/debug/stats", methods=["GET"])
def debug_stats():
    return jsonify(oram.dump_stats())


if __name__ == "__main__":
    app.run(port=5000, debug=True)
