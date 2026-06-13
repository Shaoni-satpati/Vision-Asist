@echo off
set PYTHON_EXE="C:\Users\bsatp\AppData\Local\Programs\Python\Python310\python.exe"

%PYTHON_EXE% --version
%PYTHON_EXE% -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip==24.0
pip install torch==2.3.0 torchvision==0.18.0 timm==0.9.16
pip install ultralytics==8.2.18 numpy==1.26.4 opencv-python==4.10.0.84 pyttsx3==2.90 pywin32 flask==3.0.3 Werkzeug==3.0.3 flask-sock==0.7.0 Pillow==10.3.0 python-dotenv==1.0.1 pytest
python .venv\Scripts\pywin32_postinstall.py -install
echo SETUP COMPLETE
