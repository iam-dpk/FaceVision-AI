import csv
from datetime import datetime
from .config import ATTENDANCE_DIR, ensure_dirs
from .database import list_attendance

def export_csv(query=""):
    ensure_dirs()
    path = ATTENDANCE_DIR / f"attendance_{datetime.now():%Y%m%d_%H%M%S}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Record ID","Person ID","Name","Timestamp","Status"])
        writer.writerows(list_attendance(query))
    return path
