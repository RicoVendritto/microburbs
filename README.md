# Microburbs — Local dev

This small demo app exposes a web UI to query the microburbs properties API by suburb.

How to set up (zsh / macOS):

1. Create and activate a virtualenv in the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
# activate the venv, or run the bundled python directly
source .venv/bin/activate
python app.py

# Or without activating (zsh):
.venv/bin/python app.py
```

Open http://127.0.0.1:5000 in your browser. Type a suburb and press Search.

Notes

- `main.fetch_properties(suburb)` is used by the Flask app to fetch data.
- The template will try to render arrays of objects as cards; fallback is prettified JSON.
