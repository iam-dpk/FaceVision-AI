# FaceVision AI

Portfolio-ready desktop face recognition and attendance application....

## Supported environment

**Recommended: Python 3.11 or 3.12 on Windows.**

Python 3.14 is not recommended for this project because computer-vision dependencies may lag behind the newest Python release.....

## Windows quick start

Open PowerShell in this folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Or double-click `run.bat`.

## Features

- Dashboard
- Integrated live webcam recognition window
- Face registration from image
- Known/unknown recognition
- Automatic attendance with cooldown
- SQLite database
- Attendance search
- CSV export
- Face management
- Settings
- Demo data
- Markdown report generation
- Automated tests

## Demo

```powershell
python -m src.demo
python app.py
```

## Tests

```powershell
pytest -q
```

## Recognition note

The default encoder is a lightweight local descriptor designed for a runnable portfolio demo. It is not a state-of-the-art biometric model. For real deployments, use a validated modern face-embedding model, consent/retention controls, encryption, access control and liveness/anti-spoofing....

## Troubleshooting camera

1. Close Teams/Zoom/Camera and other applications using the webcam.
2. Open **Settings** and try camera index `1`.
3. Check Windows Settings → Privacy & security → Camera.
4. Make sure desktop apps are allowed to access the camera....
