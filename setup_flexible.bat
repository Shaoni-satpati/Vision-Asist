@echo off
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip

echo Installing Nightly PyTorch for newer Python...
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

echo Installing remaining dependencies...
pip install timm ultralytics numpy opencv-python pyttsx3 pywin32 flask Werkzeug flask-sock Pillow python-dotenv pytest

echo Running pywin32 post-install...
python .venv\Scripts\pywin32_postinstall.py -install

echo SETUP COMPLETE
