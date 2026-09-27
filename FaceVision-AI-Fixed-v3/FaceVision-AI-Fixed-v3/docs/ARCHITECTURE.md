# Architecture

```text
Webcam/Image
    |
    v
FaceDetector -> FaceEncoder -> FaceRecognizer
                                  |
                                  v
                           Attendance Service
                                  |
                    +-------------+-------------+
                    |                           |
                 SQLite                      CSV/Report
                    |
                    v
                  GUI
```

The core modules are independent from Tkinter. This makes the recognition and attendance logic reusable in a future web/API interface.
