from datetime import datetime, timedelta
from .database import add_attendance, last_attendance_for

def mark_attendance(person_id, name, cooldown_minutes=10):
    now = datetime.now()
    previous = last_attendance_for(person_id)
    if previous:
        try:
            if now - datetime.fromisoformat(previous[0]) < timedelta(minutes=cooldown_minutes):
                return False
        except ValueError:
            pass
    add_attendance(person_id, name, now.isoformat(timespec="seconds"))
    return True
