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
    def generate_ascii():
  # Создаем скользящие позиции для симуляции падающего кода "Матрицы"
  offset = 0

  while True:
    # 1. Создаем искусственный холст (кадр) полностью средствами NumPy
    frame = np.zeros((rows, cols), dtype=np.uint8)

    # 2. Генерируем вертикальные полосы, сдвигая их по фазе каждую итерацию
    for c in range(cols):
      speed_factor = (c % 5) + 1
      for r in range(rows):
        # Математическая формула для динамического волнового эффекта
        val = int(
            (np.sin((r + offset * speed_factor) * 0.3) + 1)
            * 0.5
            * (num_chars - 1)
        )
        frame[r, c] = val

    # 3. Собираем символы на основе сгенерированной NumPy матрицы
    ascii_lines = []
    for row in frame:
      line = "".join([ASCII_CHARS[pixel] for pixel in row])
      ascii_lines.append(line)

    ascii_frame = "\n".join(ascii_lines)
    safe_frame = ascii_frame.replace("\n", "\\n")

    # Сдвигаем анимацию вперед
    offset += 1

    # Отправляем в веб-интерфейс
    yield f"data: {safe_frame}\n\n"

    # Пауза между фреймами (примерно 25 кадров в секунду)
    time.sleep(0.04)



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

