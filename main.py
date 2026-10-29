import base64
import time
import cv2
from flask import Flask, Response, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_matrix_key'
# Инициализируем сокеты и разрешаем CORS для работы на хостингах
socketio = SocketIO(app, cors_allowed_origins="*")

# Символы от темного к светлому 
ASCII_CHARS = " .,:;i-+*h%@#W漢字"
num_chars = len(ASCII_CHARS)

# Размеры сетки вывода
cols, rows = 110, 70

@app.route("/")
def index():
    return render_template("index.html")

# Ловим кадр от браузера по сокету
@socketio.on('video_frame')
def handle_video_frame(data):
    try:
        # Извлекаем чистую строку Base64, отрезая техническую шапку
        encoded_data = data.split(',')[1]
        
        # Декодируем байты в картинку OpenCV
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return

        # Зеркалим кадр по горизонтали для удобства пользователя
        frame = cv2.flip(frame, 1)

        # Конвертируем в серое изображение и уменьшаем размер до нашей сетки
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (cols, rows))

        # Масштабируем яркость пикселей в индексы нашей строки символов
        animated_indices = (small / 255.0 * (num_chars - 1)).astype(int)

        ascii_lines = []
        for row in animated_indices:
            line = "".join([ASCII_CHARS[pixel] for pixel in row])
            ascii_lines.append(line)

        # Собираем финальную текстовую картинку
        ascii_frame = "\n".join(ascii_lines)

        # Мгновенно отправляем ASCII-арт обратно клиенту по тому же сокет-каналу
        emit('ascii_response', {'ascii': ascii_frame})

    except Exception as e:
        print(f"Ошибка сокета: {e}")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    # Разрешаем запуск unsafe werkzeug, чтобы обойти защиту Flask на хостингах
    socketio.run(app, host="0.0.0.0", port=port, debug=True, allow_unsafe_werkzeug=True)
