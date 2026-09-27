from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FACES_DIR = DATA_DIR / "faces"
ATTENDANCE_DIR = DATA_DIR / "attendance"
DB_DIR = DATA_DIR / "database"
REPORT_DIR = ROOT / "reports" / "generated"
CONFIG_FILE = DB_DIR / "config.json"
LOG_FILE = DB_DIR / "activity.log"

DEFAULT_CONFIG = {
    "camera_index": 0,
    "recognition_threshold": 0.72,
    "attendance_cooldown_minutes": 10,
    "camera_width": 960,
    "camera_height": 540,
}

def ensure_dirs():
    for p in (FACES_DIR, ATTENDANCE_DIR, DB_DIR, REPORT_DIR):
        p.mkdir(parents=True, exist_ok=True)

def load_config():
    ensure_dirs()
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG.copy())
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return {**DEFAULT_CONFIG, **data}
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config):
    ensure_dirs()
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")
