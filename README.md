# 🎬 ASCII Matrix Camera Capture

A real-time interactive Python application that captures video from your webcam, converts the pixel data into text characters, and generates a dynamic digital rain effect inspired by the iconic **Matrix** movie.

The project renders falling code streams onto a graphical canvas using OpenCV, linking the brightness of the characters to your movements and silhouette in front of the camera.

---

## 📸 Preview

### Real-time Matrix Effect
![ASCII Matrix Camera Preview](./preview.gif)
*Place your animated GIF or project screenshot here (save your image as `preview.gif` in the repository root).*

---

## ✨ Features
- 🎥 **Real-time Processing**: Zero-lag webcam video capture and conversion.
- 🟢 **Matrix Rain Logic**: Independent vertical streams with fading tail effects and randomized speeds.
- 👁️ **Interactive Silhouette**: Characters glow brighter where they detect light and movement, revealing your shape out of the code.
- 🪟 **Clean Exit Management**: Handles window closing smoothly via keyboard hotkeys (`Q` or `Esc`) as well as the standard OS close window button (even when compiled in borderless/no-console mode).

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.x Installed
- A working webcam

### 2. Install Dependencies
Clone the repository and install the required libraries:
```bash
pip install opencv-python numpy
```

### 3. Running the App
```bash
python main.py
```

### ⌨️ Controls:
* Press **`Q`** or **`Esc`** on your keyboard while focusing on the video window to quit.
* Click the standard **X (Close)** button in the top-right corner of the window to exit instantly.

---

## 📦 Building a Standalone Windows `.exe`

The codebase is fully optimized to be compiled into a single executable file using `PyInstaller` (or `Auto PY to EXE`) without opening a messy black system console in the background:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole main.py
```
Once the build is complete, you can find your standalone executable inside the `dist/` folder.

---

## 🛠️ Built With
- **Python 3**
- **OpenCV (`cv2`)** — Image matrix resizing, grayscale conversion, video stream capture, and vector font text rendering.
- **NumPy** — High-performance pixel array manipulation (generating the black background canvas).
