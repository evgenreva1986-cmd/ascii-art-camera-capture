import base64
import time
import cv2
from flask import Flask, Response, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

ASCII_CHARS = " .,:;i-+*h%@#W漢字"
num_chars = len(ASCII_CHARS)

LATEST_FRAME = None
cols, rows = 110, 70


def generate_ascii():
    global LATEST_FRAME
    while True:
        if LATEST_FRAME is None:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(
                frame, 
                "WAITING FOR CAMERA...", 
                (140, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (255, 255, 255), 
                2
            )
        else:
            frame = LATEST_FRAME

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (cols, rows))

        animated_indices = (small / 255.0 * (num_chars - 1)).astype(int)

        ascii_lines = []
        for row in animated_indices:
            line = "".join([ASCII_CHARS[pixel] for pixel in row])
            ascii_lines.append(line)

        ascii_frame = "\n".join(ascii_lines)
        safe_frame = ascii_frame.replace("\n", "\\n")

        yield f"data: {safe_frame}\n\n"
        time.sleep(0.05)


# ВОТ ЭТОТ РОУТ СЕЙЧАС ОТСУТСТВУЕТ НА СЕРВЕРЕ И ВЫЗЫВАЕТ ОШИБКУ 404:
@app.route("/upload_frame", methods=["POST"])
def upload_frame():
    global LATEST_FRAME
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"status": "error", "message": "No image data"}), 400
        
        encoded_data = data['image'].split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        LATEST_FRAME = cv2.flip(img, 1)
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"Ошибка при приеме кадра: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ascii_feed")
def ascii_feed():
    return Response(generate_ascii(), mimetype="text/event-stream")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)