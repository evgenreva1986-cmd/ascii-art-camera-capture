import time
import cv2
from flask import Flask, Response, render_template
import numpy as np
import os

app = Flask(__name__)

# Символы от темного к светлому 
ASCII_CHARS = " .,:;i-+*h%@#W漢字"
num_chars = len(ASCII_CHARS)

cap = cv2.VideoCapture(0)

# Размеры сетки (как у вас в коде)
cols, rows = 110, 70


def generate_ascii():
  while True:
    ret, frame = cap.read()
    if not ret:
      # Создаем случайную матрицу (шум), имитирующую кадр
      frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)

    # 1. Ваша логика: серое изображение и уменьшение размера
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (cols, rows))

    # 2. Переводим пиксели в ASCII-символы
    # Нормализуем значения от 0 до (num_chars - 1)
    animated_indices = (small / 255.0 * (num_chars - 1)).astype(int)

    ascii_lines = []
    for row in animated_indices:
      # Собираем строку из символов по индексам яркости
      line = "".join([ASCII_CHARS[pixel] for pixel in row])
      ascii_lines.append(line)

    # Объединяем строки через символ переноса строки
    ascii_frame = "\n".join(ascii_lines)

    # Заменяем реальные переносы на экранированные '\\n', чтобы SSE не ломал строку
    safe_frame = ascii_frame.replace("\n", "\\n")

    # Отправляем текстовый кадр в веб по протоколу Server-Sent Events (SSE)
    yield f"data: {safe_frame}\n\n"

    # Небольшая задержка, чтобы не перегружать процессор (~30 FPS)
    time.sleep(0.03)


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

  app.run(host="0.0.0.0", port=port)

