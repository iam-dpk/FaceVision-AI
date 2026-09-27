from datetime import datetime
from .config import REPORT_DIR, ensure_dirs
from .database import list_persons, list_attendance

def generate_report():
    ensure_dirs()
    path = REPORT_DIR / f"FaceVision_Report_{datetime.now():%Y%m%d_%H%M%S}.md"
    people = list_persons()
    attendance = list_attendance()
    lines = [
        "# FaceVision AI Project Report",
        "",
        f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
        f"Registered people: **{len(people)}**",
        f"Attendance records: **{len(attendance)}**",
        "",
        "## Registered People",
        "",
        "| ID | Name | Created |",
        "|---|---|---|",
    ]
    for pid,name,_,_,created in people:
        lines.append(f"| {pid} | {name} | {created} |")
    lines += ["", "## Recent Attendance", "", "| ID | Name | Timestamp | Status |", "|---|---|---|---|"]
    for _,pid,name,ts,status in attendance[:100]:
        lines.append(f"| {pid} | {name} | {ts} | {status} |")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
