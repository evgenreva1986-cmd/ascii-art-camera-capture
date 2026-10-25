import cv2
import numpy as np

# Символы от темного к светлому (инвертировано для черного фона окна)
# Обратите внимание: стандартный шрифт OpenCV (FONT_HERSHEY_SIMPLEX) не умеет рисовать иероглифы (漢字),
# вместо них могут отображаться знаки вопроса, но код от этого не сломается.
ASCII_CHARS = " ./:-=+*#%@'0)`~漢字"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Уменьшаем разрешение под размер текстовой сетки
    cols, rows = 110, 70
    small = cv2.resize(gray, (cols, rows))

    # Создаем черный холст, на котором будем рисовать текст
    canvas = np.zeros((750, 900, 3), dtype=np.uint8)

    # Вычисляем шаг сетки для символов
    x_step = 900 // cols
    y_step = 750 // rows

    # Рисуем символы на холсте
    for y in range(rows):
        for x in range(cols):
            pixel = small[y, x]
            char_index = int(pixel / 256 * len(ASCII_CHARS))
            char = ASCII_CHARS[char_index]
            
            # Координаты для текущего символа
            pos_x = x * x_step
            pos_y = y * y_step + 10 # +10 смещение по вертикали
            
            # Рисуем зеленый символ (как в Матрице)
            cv2.putText(canvas, char, (pos_x, pos_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

    # ПОКАЗЫВАЕМ КАДР (Оставили только одну строчку imshow)
    cv2.imshow('Matrix Camera', canvas)

    # Ждем 30 мс и проверяем нажатие клавиши (q или Esc)
    key = cv2.waitKey(30) & 0xFF
    if key == ord('q') or key == 27:
        break

    # МАГИЯ ДЛЯ КРЕСТИКА: Проверяем закрытие окна мышкой.
    # Имя окна 'Matrix Camera' строго совпадает с именем в cv2.imshow выше!
    if cv2.getWindowProperty('Matrix Camera', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
