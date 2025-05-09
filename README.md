# Oblivious Data Store

A clean, in-memory implementation of Path ORAM in Python with a Flask API for secure key-value storage. Designed for clarity, experimentation, and extensibility.

## Features

- 📦 **Path ORAM** built from scratch
- 🔁 **Recursive ORAM** to reduce trusted storage
- 💾 **Persistence layer** using `/save` and `/load` routes
- 📶 **Flask API** with `PUT`, `GET`, `DEBUG` endpoints
- ⚠️ **Stash overflow detection** with dynamic thresholds
- 🧪 **Stress testing** with real-time stash monitoring
- 📊 **(Upcoming)** Stash growth visualization
- 🔐 Prepared for future enhancements like Merkle tree integrity and multi-client access

## Folder Structure

```
backend/
├── __init__.py
├── store.py              # Flask server
├── oram.py               # Legacy ORAM logic (SimpleORAM)
└── oram_core/
    ├── __init__.py
    ├── path_oram.py      # Main ORAM logic
    └── recursive_oram.py # Position map ORAM
client/
└── client.py             # Simple CLI (optional)

scripts/
└── stress_test.py        # Stress test runner

tests/
├── test_oram.py
├── test_recursive_oram.py
└── test_store.py

requirements.txt
README.md
.gitignore
```

## API Endpoints

- `POST /put`  
  Store a key-value pair.  
  Example: `{"key": 5, "value": "hello"}`

- `GET /get/<key>`  
  Retrieve a value using the logical key.

- `GET /debug/logs`  
  Returns the access log (leaf IDs accessed).

- `GET /debug/stats`  
  Returns current stash size and bucket usage for both ORAMs.

- `POST /save`  
  Save the current ORAM state to disk.

- `POST /load`  
  Reload the saved ORAM state from disk.

## How to Run

```bash
# Start Flask server
python3 -m backend.store

# Run tests
pytest -q

# Stress test ORAM
python3 scripts/stress_test.py
```

## Future Scope

- ✅ Recursive ORAM - Done
- ✅ Disk-based persistence - Done
- 🚧 Multi-client thread-safe support
- 🚧 Merkle tree for data integrity
- 🚧 Batched writes and read-ahead caching
- 🚧 Stash growth visualization (/debug/stash_growth)
- 🚧 Smart eviction strategies and retry logic

## Acknowledgments

Inspired by the Path ORAM paper (Stefanov et al., 2013)  
Used for educational and demonstration purposes only.

---
