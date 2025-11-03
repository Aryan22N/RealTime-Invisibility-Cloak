# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import threading
# import cv2
# import numpy as np
# import time
# from datetime import datetime

# app = Flask(__name__)
# CORS(app)

# # -------- USER SETTINGS ----------
# DETECTION_COLOR = "blue"     # default cloak color
# CAPTURE_DURATION = 3.0
# NUM_BACKGROUND_FRAMES = 60
# WAIT_KEY_MS = 30
# # ---------------------------------

# is_running = False
# thread = None


# def get_hsv_ranges(color_name: str):
#     """Return HSV color ranges for cloak detection."""
#     color_name = color_name.lower()

#     if color_name == "red":
#         lower1 = np.array([0, 120, 70])
#         upper1 = np.array([10, 255, 255])
#         lower2 = np.array([170, 120, 70])
#         upper2 = np.array([180, 255, 255])
#         return [(lower1, upper1), (lower2, upper2)]

#     elif color_name == "black":
#         # Detect very dark regions (low brightness)
#         lower = np.array([0, 0, 0])
#         upper = np.array([180, 255, 60])
#         return [(lower, upper)]

#     elif color_name == "blue":
#         return [(np.array([94, 80, 2]), np.array([126, 255, 255]))]

#     elif color_name == "green":
#         return [(np.array([35, 80, 40]), np.array([90, 255, 255]))]

#     else:
#         raise ValueError("Unsupported color. Use red, green, blue, or black.")


# def refine_mask(mask: np.ndarray) -> np.ndarray:
#     """Smooth and clean mask."""
#     kernel = np.ones((5, 5), np.uint8)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
#     mask = cv2.dilate(mask, kernel, iterations=1)
#     mask = cv2.GaussianBlur(mask, (15, 15), 0)
#     return mask


# def run_cloak(color):
#     global is_running
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open webcam.")
#         return

#     print(f"--- 🧥 Invisibility Cloak Activated (Color: {color}) ---")
#     print("Capturing background in 3 seconds. Please move away from frame.")
#     time.sleep(CAPTURE_DURATION)

#     background_frames = []
#     for _ in range(NUM_BACKGROUND_FRAMES):
#         ret, frame = cap.read()
#         if not ret:
#             continue
#         frame = cv2.flip(frame, 1)
#         background_frames.append(frame.astype(np.float32))
#         cv2.waitKey(1)

#     if not background_frames:
#         print("Error: Could not capture background.")
#         cap.release()
#         return

#     background = np.mean(background_frames, axis=0).astype(np.uint8)
#     hsv_ranges = get_hsv_ranges(color)

#     while is_running and cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame = cv2.flip(frame, 1)
#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#         mask = None
#         for (lower, upper) in hsv_ranges:
#             temp_mask = cv2.inRange(hsv, lower, upper)
#             mask = temp_mask if mask is None else cv2.bitwise_or(mask, temp_mask)

#         mask = refine_mask(mask)
#         mask_inv = cv2.bitwise_not(mask)

#         background_part = cv2.bitwise_and(background, background, mask=mask)
#         current_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
#         final = cv2.addWeighted(background_part, 1, current_part, 1, 0)

#         # --- Show both screens ---
#         cv2.imshow("Original", frame)
#         cv2.imshow("Invisibility Cloak Output", final)

#         key = cv2.waitKey(WAIT_KEY_MS) & 0xFF
#         if key == ord('q') or not is_running:
#             print("Stopping cloak...")
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     is_running = False


# @app.route("/start", methods=["POST"])
# def start_cloak():
#     global is_running, thread
#     if is_running:
#         return jsonify({"status": "already_running"}), 200

#     # Fix: Ensure JSON is read safely
#     data = request.get_json(silent=True) or {}
#     color = data.get("color") or DETECTION_COLOR

#     print(f"🔹 Selected cloak color: {color}")

#     is_running = True
#     thread = threading.Thread(target=run_cloak, args=(color,), daemon=True)
#     thread.start()
#     return jsonify({"status": "started", "color": color})


# @app.route("/stop", methods=["POST"])
# def stop_cloak():
#     global is_running
#     is_running = False
#     cv2.destroyAllWindows()
#     return jsonify({"status": "stopped"})


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5001, debug=True)



from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import threading
import cv2
import numpy as np
import time

app = Flask(__name__)
CORS(app)

# -------- SETTINGS ----------
DETECTION_COLOR = "blue"
CAPTURE_DURATION = 3.0
NUM_BACKGROUND_FRAMES = 60
# ----------------------------

is_running = False
output_frame = None
original_frame = None
lock = threading.Lock()


def get_hsv_ranges(color_name: str):
    color_name = color_name.lower()
    if color_name == "red":
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])
        return [(lower1, upper1), (lower2, upper2)]
    elif color_name == "black":
        return [(np.array([0, 0, 0]), np.array([180, 255, 60]))]
    elif color_name == "blue":
        return [(np.array([94, 80, 2]), np.array([126, 255, 255]))]
    elif color_name == "green":
        return [(np.array([35, 80, 40]), np.array([90, 255, 255]))]
    else:
        raise ValueError("Unsupported color")


def refine_mask(mask):
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.GaussianBlur(mask, (15, 15), 0)
    return mask


def run_cloak(color):
    global is_running, output_frame, original_frame
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open webcam.")
        is_running = False
        return

    print(f"🎥 Capturing background for {CAPTURE_DURATION} sec...")
    time.sleep(CAPTURE_DURATION)

    bg_frames = []
    for _ in range(NUM_BACKGROUND_FRAMES):
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        bg_frames.append(frame.astype(np.float32))
        cv2.waitKey(1)

    if not bg_frames:
        print("Error: Could not capture background.")
        cap.release()
        is_running = False
        return

    background = np.mean(bg_frames, axis=0).astype(np.uint8)
    hsv_ranges = get_hsv_ranges(color)

    while is_running:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = None
        for (lower, upper) in hsv_ranges:
            temp_mask = cv2.inRange(hsv, lower, upper)
            mask = temp_mask if mask is None else cv2.bitwise_or(mask, temp_mask)

        mask = refine_mask(mask)
        mask_inv = cv2.bitwise_not(mask)

        background_part = cv2.bitwise_and(background, background, mask=mask)
        current_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
        final = cv2.addWeighted(background_part, 1, current_part, 1, 0)

        with lock:
            original_frame = frame.copy()
            output_frame = final.copy()

    cap.release()
    is_running = False


# ---- STREAM HELPERS ----
def generate_frames(frame_type="output"):
    global output_frame, original_frame
    while True:
        with lock:
            if frame_type == "output":
                frame = output_frame
            else:
                frame = original_frame

            if frame is None:
                continue
            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route("/video_feed_output")
def video_feed_output():
    return Response(generate_frames("output"),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/video_feed_original")
def video_feed_original():
    return Response(generate_frames("original"),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/start", methods=["POST"])
def start_cloak():
    global is_running
    if is_running:
        return jsonify({"status": "already_running"})

    data = request.get_json(silent=True) or {}
    color = data.get("color", DETECTION_COLOR)

    print(f"🧥 Starting cloak with color: {color}")
    is_running = True
    threading.Thread(target=run_cloak, args=(color,), daemon=True).start()
    return jsonify({"status": "started", "color": color})


@app.route("/stop", methods=["POST"])
def stop_cloak():
    global is_running
    is_running = False
    return jsonify({"status": "stopped"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)




