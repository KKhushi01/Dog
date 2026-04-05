from flask import Flask, render_template, Response
from camera.camera import Camera

app = Flask(__name__)
camera = Camera()  # Initialize Raspberry Pi camera


@app.route("/")
def index():
    return render_template("control.html")


def gen_frames():
    for jpeg in camera.frames():
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               jpeg + b"\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/stand")
def stand():
    print("STAND command triggered")
    # TODO: Add servo control code here
    return "Standing..."


@app.route("/sit")
def sit():
    print("SIT command triggered")
    # TODO: Add servo control code here
    return "Sitting..."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
