import base64
import cv2
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_matrix_key'
# Разрешаем сокеты для любых адресов
socketio = SocketIO(app, cors_allowed_origins="*")

ASCII_CHARS = " .,:;i-+*h%@#W漢字"
num_chars = len(ASCII_CHARS)
cols, rows = 110, 70

@app.route("/")
def index():
    return render_template("index.html")

# Ловим кадр от браузера по сокету
@socketio.on('video_frame')
def handle_video_frame(data):
    try:
        # 1. Декодируем Base64 строку в картинку OpenCV
        encoded_data = data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return

        # 2. Зеркалим кадр
        frame = cv2.flip(frame, 1)

        # 3. Наша ASCII-логика обработки
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (cols, rows))
        animated_indices = (small / 255.0 * (num_chars - 1)).astype(int)

        ascii_lines = []
        for row in animated_indices:
            line = "".join([ASCII_CHARS[pixel] for pixel in row])
            ascii_lines.append(line)

        ascii_frame = "\n".join(ascii_lines)

        # 4. МГНОВЕННО отправляем ASCII-кадр обратно тому же пользователю
        emit('ascii_response', {'ascii': ascii_frame})

    except Exception as e:
        print(f"Ошибка сокета: {e}")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    # Для сокетов важно запускаться через socketio.run
    socketio.run(app, host="0.0.0.0", port=port, debug=True)