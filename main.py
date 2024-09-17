from flask import Flask, render_template, Response
import cv2
import mss
import numpy as np
import time

app = Flask(__name__)

def generate_frames():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            img = sct.grab(monitor)
            frame = np.array(img)
            # frame = cv2.resize(frame, (640, 360))
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            time.sleep(0.05)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
