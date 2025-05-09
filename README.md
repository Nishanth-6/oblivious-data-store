# Oblivious Data Store

A minimalist, educational implementation of **Path ORAM (Oblivious RAM)** in Python, exposing secure memory access through a RESTful Flask API.

This project simulates privacy-preserving access patterns for key-value storage, showcasing ORAM principles, recursive position map hiding, and stress-tested stash behavior — all wrapped in a clean Flask server for demonstration and testing.

---

## 🔧 Features

- 📦 **Path ORAM** core logic (in-memory, randomized access path)
- 🔁 **Recursive ORAM** to hide position map accesses
- 💾 **Persistence layer** (`/save`, `/load`) to serialize/restore ORAM state
- 📶 **RESTful API**: `PUT`, `GET`, `DEBUG`, and future endpoints
- ⚠️ **Stash overflow detection** with dynamic thresholds
- 🧪 **Stress testing** to simulate load and detect ORAM bottlenecks
- 📊 *(Coming soon)*: Stash growth visualization and retry-aware eviction

---

## 📁 Folder Structure

```
oblivious-data-store/
├── backend/
│   ├── store.py               # Flask API server
│   ├── oram.py                # Optional entry point
│   └── oram_core/
│       ├── path_oram.py       # Core ORAM logic
│       └── recursive_oram.py  # Recursive ORAM wrapper
├── client/
│   └── client.py              # Placeholder test client (optional)
├── scripts/
│   ├── setup.sh               # Reserved for setup automation
│   └── stress_test.py         # Stash overflow simulator
├── tests/
│   ├── test_oram.py
│   ├── test_store.py
│   └── test_recursive_oram.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Setup Instructions

### 1. Set up virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Flask Server

```bash
python3 -m backend.store
```

---

## 🧪 Example API Usage

### Store a key-value pair
```bash
curl -X POST http://127.0.0.1:5000/put \
     -H "Content-Type: application/json" \
     -d '{"key": "5", "value": "hello world"}'
```

### Retrieve a value
```bash
curl http://127.0.0.1:5000/get/5
```

### Save & Load ORAM state
```bash
curl -X POST http://127.0.0.1:5000/save
curl -X POST http://127.0.0.1:5000/load
```

### Debug endpoints
```bash
curl http://127.0.0.1:5000/debug/logs
curl http://127.0.0.1:5000/debug/stats
```

---

## 🧪 Stress Testing

```bash
python3 scripts/stress_test.py
```

Monitors stash growth under randomized write pressure. You’ll see outputs like:

```
⚠️ WARNING: Stash overflow — current size: 54 (threshold was 36)
```

---

## ✅ Tests

```bash
pytest -q
```

Or run individual tests:
```bash
pytest -q tests/test_recursive_oram.py
```

---

## 📚 Future Enhancements

- 🧵 **Thread-safe ORAM** to support concurrent clients
- 🌲 **Merkle Tree** for data integrity checks
- 🔄 **Batch reads/writes** with improved eviction heuristics
- 📊 **Stash growth plots** and `/debug/stash_growth` endpoint
- 📁 **Export logs/results** as CSV or JSON for reproducibility

---
