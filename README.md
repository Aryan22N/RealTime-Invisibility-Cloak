## \_

````md
# 🧥 Invisibility Cloak Controller

### Real-Time Vision System using **Next.js + Flask + OpenCV**

This project implements a **real-time invisibility cloak** inspired by the Harry Potter concept — powered by **Computer Vision (OpenCV)** and a **Next.js frontend** for smooth control and monitoring.  
Users can **start or stop** the cloak process, view **live output**, and manage **color selection** for the cloak.

---

## 🚀 Project Overview

The system works by identifying a specific cloak color (e.g., black or blue) from a live webcam feed using **color masking** and **background subtraction**.  
It then replaces those pixels with the background, creating an illusion of invisibility.

**Core features include:**

- 🎥 Dual camera window — one for **original** and one for **processed cloak output**
- ⚡ Real-time video streaming with Flask and OpenCV
- 🌈 Adjustable cloak color
- 🧠 Smooth frontend controls using React Hooks
- 🔗 API communication between Next.js & Flask

---

## 🧩 Tech Stack

| Layer               | Technologies Used                   |
| :------------------ | :---------------------------------- |
| **Frontend**        | Next.js (React), TailwindCSS, Axios |
| **Backend**         | Flask (Python), Flask-CORS          |
| **Computer Vision** | OpenCV                              |
| **Language**        | JavaScript + Python                 |

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Aryan22N/Invisibility-Cloak-AI.git
cd Invisibility-Cloak-AI
```
````

---

### 2️⃣ Backend Setup (Flask)

```bash
cd backend
pip install flask flask-cors opencv-python
python app.py
```

Your Flask server will run at:

```
http://127.0.0.1:5001
```

---

### 3️⃣ Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Your frontend will be available at:

```
http://localhost:3000
```

---

## ⚙️ API Endpoints

| Endpoint | Method | Description                          |
| :------- | :----- | :----------------------------------- |
| `/start` | POST   | Start the invisibility cloak process |
| `/stop`  | POST   | Stop the invisibility cloak process  |

---

## 🧠 Working Principle

1. Capture the background frame before starting.
2. Detect cloak color (e.g., black or blue) using HSV color masking.
3. Replace the detected cloak area with the stored background.
4. Stream both the **original feed** and **processed output** live.

---

## 🖥️ UI Preview

| Feature                | Screenshot                                             |
| :--------------------- | :----------------------------------------------------- |
| **Main Control Panel** | 🧥 Start/Stop buttons, color selector, and live status |
| **Dual Feed Output**   | Original + Cloaked video windows                       |

---

## 👨‍💻 Team Members

| Name                |
| :------------------ |
| **Aryan Nandanwar** |
| **Pranav Shende**   |
| **Krishna Jajoo**   |

---

## 🌟 Future Enhancements

- Add support for **multiple cloak colors**
- Implement **AI-based segmentation** for better accuracy
- Deploy full stack on **Render / Vercel**
- Add **dark/light theme** toggle in UI

---

## ❤️ Acknowledgments

- OpenCV community for Computer Vision libraries
- Next.js & Flask documentation for framework support
- Inspired by **Harry Potter’s Invisibility Cloak** concept

---
