import cv2

class Camera:
    def __init__(self, device="/dev/video0", width=640, height=480):
        # Use V4L2 backend to access the Pi Camera Module 3
        self.cap = cv2.VideoCapture(device, cv2.CAP_V4L2)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open Raspberry Pi Camera Module.")

        # Set resolution and framerate
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

    def frames(self):
        """Yields JPEG byte frames for the Flask Response."""
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue

            ok, jpeg = cv2.imencode(".jpg", frame)
            if not ok:
                continue

            yield jpeg.tobytes()

    def release(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
