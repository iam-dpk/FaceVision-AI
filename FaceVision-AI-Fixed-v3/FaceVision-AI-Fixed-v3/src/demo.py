from datetime import datetime, timedelta
from .config import ensure_dirs
from .database import init_db, add_person, add_attendance

def seed_demo():
    ensure_dirs()
    init_db()
    people = [("DEMO001","Demo Alice"),("DEMO002","Demo Bob"),("DEMO003","Demo Charlie")]
    for pid,name in people:
        add_person(pid,name,"","")
    for i,(pid,name) in enumerate(people):
        add_attendance(pid,name,(datetime.now()-timedelta(minutes=15*i)).isoformat(timespec="seconds"))
    print("Demo data created successfully.")

if __name__ == "__main__":
    seed_demo()
