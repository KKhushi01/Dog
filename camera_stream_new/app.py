import cv2
from flask import Flask, Response, render_template
import threading
import time
from ultralytics import YOLO

app = Flask(__name__)

lock = threading.Lock()
output_frame = None

# ── YOLO setup ───────────────────────────────────────────────────────────────
model = YOLO("yolov8n.pt")  # nano = fastest

CONF_THRESHOLD = 0.45
ALLOWED_CLASSES = None  # None = all 80 classes. e.g. [0] = person only

# ── Performance tuning ───────────────────────────────────────────────────────
YOLO_EVERY_N_FRAMES = 3   # run YOLO once every N frames (raise to 4/5 if still slow)
DETECT_WIDTH  = 320        # resize frame to this before detection
DETECT_HEIGHT = 240


def run_yolo(frame):
    """Resize down for detection, scale boxes back up to original frame size."""
    orig_h, orig_w = frame.shape[:2]

    small = cv2.resize(frame, (DETECT_WIDTH, DETECT_HEIGHT))
    results = model(small, conf=CONF_THRESHOLD, classes=ALLOWED_CLASSES, verbose=False)[0]

    scale_x = orig_w / DETECT_WIDTH
    scale_y = orig_h / DETECT_HEIGHT

    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1 = int(x1 * scale_x)
        y1 = int(y1 * scale_y)
        x2 = int(x2 * scale_x)
        y2 = int(y2 * scale_y)

        conf    = float(box.conf[0])
        cls_id  = int(box.cls[0])
        label   = model.names[cls_id]
        color   = (0, 255, 100) if label == "person" else (0, 220, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        text = f"{label} {conf:.0%}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
        cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 6, y1), color, -1)
        cv2.putText(frame, text, (x1 + 3, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1, cv2.LINE_AA)

    count = len(results.boxes)
    cv2.putText(frame, f"Objects: {count}", (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 136), 2, cv2.LINE_AA)

    return frame


def capture_frames():
    global output_frame

    camera = None
    for index in range(5):
        cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
        if cap.isOpened():
            camera = cap
            print(f"✅ Camera found at index {index}")
            break

    if camera is None:
        print("❌ ERROR: No camera found.")
        return

    # Lower resolution = faster everything
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 30)

    frame_count = 0
    last_frame  = None  # reuse last YOLO result on skipped frames

    while True:
        success, frame = camera.read()
        if not success:
            time.sleep(0.05)
            continue

        frame_count += 1

        if frame_count % YOLO_EVERY_N_FRAMES == 0:
            frame = run_yolo(frame)
            last_frame = frame
        elif last_frame is not None:
            # paste previous boxes onto new frame to avoid flickering
            frame = last_frame

        with lock:
            output_frame = frame.copy()


def generate_stream():
    global output_frame

    while True:
        with lock:
            if output_frame is None:
                time.sleep(0.01)
                continue
            ret, buffer = cv2.imencode('.jpg', output_frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
            if not ret:
                continue
            frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    print("⏳ Loading YOLO model...")
    import numpy as np
    model(np.zeros((DETECT_HEIGHT, DETECT_WIDTH, 3), dtype=np.uint8), verbose=False)
    print("✅ YOLO ready")

    t = threading.Thread(target=capture_frames, daemon=True)
    t.start()

    print("🚀 Server running — open http://<PI_IP>:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)