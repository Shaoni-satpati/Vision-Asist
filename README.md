# VisionAssist

VisionAssist is a Flask-based desktop vision assistant that streams camera frames to a browser UI, performs object detection with YOLO, and supports depth estimation and text-to-speech narration.

## Requirements

- Python 3.10 or 3.11
- Windows
- A working webcam

## Setup

1. Open a terminal in the project root:
   ```bash
   cd "c:/my code/steg-desktop-windows/visionassist"
   ```

2. Create and activate a virtual environment:
   ```bash
   py -3.10 -m venv .venv
   ./.venv/Scripts/Activate.ps1
   ```

3. Upgrade pip and install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

## Run

1. Start the server:
   ```bash
   ./.venv/Scripts/python.exe main.py
   ```

2. Open the UI in your browser:
   ```text
   http://127.0.0.1:5000
   ```

## Project structure

- `main.py` — app entry point
- `config.py` — application configuration and environment variables
- `server/` — Flask app setup, routes, and WebSocket stream
- `frontend/` — browser UI files (`index.html`, `css/`, `js/`)
- `core/` — computer vision and pipeline logic
- `tests/` — unit tests

## Notes

- The project uses `Flask` with `flask-sock` for WebSocket streaming.
- The `frontend/` directory is served as the Flask static and template folder.
- A `.gitignore` file is included to exclude environment files, logs, and local build artifacts.
- If you need to change the camera, model, or server settings, use environment variables or edit `config.py`.

## GitHub push example

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```
