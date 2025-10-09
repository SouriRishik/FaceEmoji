# 🤖 FaceEmoji  

**FaceEmoji** is a real-time emotion recognition system that reacts to your facial expressions and gestures — just like an emoji mirror!  
It detects **straight face**, **smiling**, and **hands up** gestures from your webcam feed and displays matching emojis in real time.

---

## 🧠 Features
- 🎥 Live emotion detection using **MediaPipe**
- 😐 Detects **Straight Face**
- 😁 Detects **Smile**
- ✋ Detects **Hands Up**
- 🧩 Real-time emoji reactions using **Pygame**

---

## 🖥️ Demo
| Emotion | Example |
|----------|----------|
| Straight Face | 😐 |
| Smiling | 😁 |
| Hands Up | 🙌 |

---

## ⚙️ Installation

```bash
# Clone this repository
git clone https://github.com/SouriRishik/FaceEmoji.git
cd FaceEmoji
```
## ▶️ Usage
```bash
python emoji_reactor.py
```
Make sure you have an emojis/ folder containing:

emojis/
├── straight.png
├── smile.png
└── handsup.png

## 🧩 Tech Stack

- Python 3
- MediaPipe – Face and Hand landmark detection
- OpenCV – Real-time video processing
- Pygame – Emoji display window

## 📸 Preview

Real-time emotion-based emoji reaction system built for fun and creative interaction.
Press _'q'_ to exit the app.
# Install dependencies
pip install opencv-python mediapipe pygame numpy
