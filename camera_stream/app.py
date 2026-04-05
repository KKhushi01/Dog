import cv2
from flask import Flask, Response, render_template
import threading
import time

app = Flask(__name__)

lock = threading.Lock()
output_frame = None


def capture_frames():
    global output_frame

    camera = None

    # Try camera indices
    for index in range(5):
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if cap.isOpened():
            camera = cap
            print(f"✅ Camera found at index {index}")
            break

    if camera is None:
        print("❌ ERROR: No camera found.")
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 30)

    while True:
        success, frame = camera.read()
        if not success:
            print("❌ Failed to read frame")
            time.sleep(0.1)
            continue

        with lock:
            output_frame = frame.copy()


def generate_stream():
    global output_frame

    while True:
        with lock:
            if output_frame is None:
                time.sleep(0.01)
                continue

            ret, buffer = cv2.imencode('.jpg', output_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
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
    t = threading.Thread(target=capture_frames, daemon=True)
    t.start()

    print("🚀 Server running...")
    print("👉 Open browser: http://<PI_IP>:5000")

    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)