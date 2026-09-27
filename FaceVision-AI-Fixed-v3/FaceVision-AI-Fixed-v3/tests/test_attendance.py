from datetime import datetime
import src.attendance as attendance

def test_mark_attendance_cooldown(monkeypatch):
    calls = []
    monkeypatch.setattr(attendance, "last_attendance_for", lambda pid: None)
    monkeypatch.setattr(attendance, "add_attendance",
                        lambda *args, **kwargs: calls.append(args))
    assert attendance.mark_attendance("P1", "Alice", 10) is True
    assert calls
