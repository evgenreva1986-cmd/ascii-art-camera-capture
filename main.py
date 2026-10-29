import base64
import time
import cv2
from flask import Flask, Response, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

# Символы от темного к светлому 
ASCII_CHARS = " .,:;i-+*h%@#W漢字"
num_chars = len(ASCII_CHARS)

# Глобальный буфер кадра
LATEST_FRAME = None

# Размеры сетки
cols, rows = 110, 70


# ИСПРАВЛЕНО: Убрали отсюда роут /upload_frame. Теперь это просто функция-генератор.
def generate_ascii():
    global LATEST_FRAME

    while True:
        if LATEST_FRAME is None:
            # Если кадра нет, создаем временную заглушку и отправляем её через yield
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
            # Если кадр пришел из браузера — берем его
            frame = LATEST_FRAME

        # Обработка изображения в ASCII
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (cols, rows))

        # Переводим пиксели в ASCII-символы
        animated_indices = (small / 255.0 * (num_chars - 1)).astype(int)

        ascii_lines = []
        for row in animated_indices:
            line = "".join([ASCII_CHARS[pixel] for pixel in row])
            ascii_lines.append(line)

        # Объединяем строки и экранируем переносы для SSE
        ascii_frame = "\n".join(ascii_lines)
        safe_frame = ascii_frame.replace("\n", "\\n")

        # ИСПРАВЛЕНО: Теперь yield срабатывает всегда, генерируя поток данных
        yield f"data: {safe_frame}\n\n"
        
        # Контроль частоты кадров (около 20 FPS)
        time.sleep(0.05)


# ИСПРАВЛЕНО: Этот роут теперь отвечает только за прием кадров от JS
@app.route("/upload_frame", methods=["POST"])
def upload_frame():
    global LATEST_FRAME
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"status": "error", "message": "No image data"}), 400
        
        # Извлекаем чистую строку Base64
        encoded_data = data['image'].split(',')[1]
        
        # Декодируем и собираем картинку для OpenCV
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Зеркалим для удобства пользователя
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
    # Отдаем текст с миметпом event-stream
    return Response(generate_ascii(), mimetype="text/event-stream")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    # Включаем отладку (debug=True), чтобы видеть ошибки в реальном времени
    app.run(host="0.0.0.0", port=port, debug=True)