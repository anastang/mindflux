import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np
from deepface import DeepFace
import requests
import json

# ------------------ GESTURE DETECTION SETUP ------------------ #
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# To track whether a key is currently being held down
current_key = None
last_press_time = time.time()  # Track the last press time
press_delay = 0.2              # Delay between key presses (in seconds)

# Counters for each gesture (click count)
gesture_counts = {
    'up': 0,
    'down': 0,
    'left': 0,
    'right': 0
}

# Define font and text size
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.7
font_thickness = 2


# ------------------ EMOTION DETECTION SETUP ------------------ #
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

emotion_counts = {
    "happy": 0,
    "sad": 0,
    "angry": 0,
    "fear": 0,
    "surprise": 0,
    "disgust": 0,
    "neutral": 0
}

# Example performance variables
current_level = 1
current_score = 0


# ------------------------------------------------------------- #
#  Function to detect specific gestures based on hand landmarks
# ------------------------------------------------------------- #
def detect_gesture(hand_landmarks, frame_width, is_mirror=False):
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]
    wrist = hand_landmarks.landmark[0]

    if is_mirror:
        # Flip horizontally
        thumb_tip.x = 1 - thumb_tip.x
        index_tip.x = 1 - index_tip.x
        middle_tip.x = 1 - middle_tip.x
        ring_tip.x = 1 - ring_tip.x
        pinky_tip.x = 1 - pinky_tip.x
        wrist.x = 1 - wrist.x

    # Gesture: Up (all fingers extended and well spread)
    if (
        all([
            index_tip.y < wrist.y,  # Above wrist
            middle_tip.y < wrist.y,
            ring_tip.y < wrist.y,
            pinky_tip.y < wrist.y
        ])
        and abs(thumb_tip.x - pinky_tip.x) > 0.3
    ):
        return 'up'

    # Gesture: Down (fist gesture, all fingers curled)
    if (
        all([
            index_tip.y > wrist.y,
            middle_tip.y > wrist.y,
            ring_tip.y > wrist.y,
            pinky_tip.y > wrist.y
        ])
        and abs(index_tip.x - thumb_tip.x) < 0.1
    ):
        return 'down'

    # Gesture: Left (index and thumb extended, others curled)
    if (
        index_tip.y < wrist.y
        and middle_tip.y > index_tip.y
        and abs(index_tip.x - thumb_tip.x) > 0.1
        and (
            index_tip.x < thumb_tip.x if not is_mirror else
            index_tip.x > thumb_tip.x
        )
    ):
        return 'left'

    # Gesture: Right (index and thumb extended, others curled)
    if (
        index_tip.y < wrist.y
        and middle_tip.y > index_tip.y
        and abs(index_tip.x - thumb_tip.x) > 0.1
        and (
            index_tip.x > thumb_tip.x if not is_mirror else
            index_tip.x < thumb_tip.x
        )
    ):
        return 'right'

    return None


# ----------------------------------------------------------------- #
#  Functions to simulate or hold key presses
# ----------------------------------------------------------------- #
def click_key(direction):
    global current_key, last_press_time
    current_time = time.time()

    if current_time - last_press_time >= press_delay:
        if direction == 'up':
            if current_key != 'up':
                pyautogui.press('up')
                current_key = 'up'
                gesture_counts['up'] += 1

        elif direction == 'down':
            if current_key != 'down':
                pyautogui.press('down')
                current_key = 'down'
                gesture_counts['down'] += 1

        elif direction == 'left':
            if current_key != 'left':
                pyautogui.press('left')
                current_key = 'left'
                gesture_counts['left'] += 1

        elif direction == 'right':
            if current_key != 'right':
                pyautogui.press('right')
                current_key = 'right'
                gesture_counts['right'] += 1

        last_press_time = current_time


def press_key(direction):
    global current_key, last_press_time
    current_time = time.time()

    if current_time - last_press_time >= press_delay:
        if direction == 'down':
            if current_key != 'down':
                pyautogui.keyDown('down')
                current_key = 'down'
                gesture_counts['down'] += 1

        last_press_time = current_time


def release_key():
    global current_key
    if current_key:
        pyautogui.keyUp(current_key)
        current_key = None


# ----------------------------------------------------------------- #
#  New UI Drawing Function
# ----------------------------------------------------------------- #
def draw_custom_ui(frame):
    """
    Draws a new modern UI with:
      - A top bar showing gesture counts
      - A bottom bar for performance
      - A right sidebar for emotion counts
    """
    overlay = frame.copy()
    h, w, _ = frame.shape

    # ---------------- Top Bar (Gesture Counts) ---------------- #
    top_bar_height = 50
    cv2.rectangle(
        overlay, 
        (0, 0), 
        (w, top_bar_height), 
        (0, 0, 0), 
        -1
    )

    # Gesture text
    gesture_text = (f"Gestures | Up: {gesture_counts['up']} | "
                    f"Down: {gesture_counts['down']} | "
                    f"Left: {gesture_counts['left']} | "
                    f"Right: {gesture_counts['right']}")
    cv2.putText(
        overlay,
        gesture_text,
        (10, 30),  # Slight padding from top-left
        font,
        font_scale,
        (255, 255, 255),
        font_thickness,
        cv2.LINE_AA
    )

    # ---------------- Bottom Bar (Performance) ---------------- #
    bottom_bar_height = 50
    cv2.rectangle(
        overlay,
        (0, h - bottom_bar_height),
        (w, h),
        (0, 0, 0),
        -1
    )

    # Performance calculation
    total_gestures = sum(gesture_counts.values())
    if total_gestures == 0:
        performance_percentage = 0
    else:
        performance_percentage = (
            (total_gestures / (4 * max(gesture_counts.values(), default=1))) * 100
        )
    performance_text = (
        f"Performance: {performance_percentage:.2f}% "
        # f"Level: {current_level}  | Score: {current_score}"
    )
    cv2.putText(
        overlay,
        performance_text,
        (10, h - 15),  # Slight padding above bottom
        font,
        font_scale,
        (255, 255, 255),
        font_thickness,
        cv2.LINE_AA
    )

    # ---------------- Right Sidebar (Emotion Counts) ---------------- #
    sidebar_width = 160
    cv2.rectangle(
        overlay,
        (w - sidebar_width, top_bar_height),
        (w, h - bottom_bar_height),
        (0, 0, 0),
        -1
    )

    # List emotions in the sidebar
    x_text = w - sidebar_width + 10
    y_text = top_bar_height + 30
    line_height = 30

    cv2.putText(
        overlay,
        "Emotions:",
        (x_text, y_text),
        font,
        font_scale,
        (255, 255, 255),
        font_thickness,
        cv2.LINE_AA
    )
    y_text += line_height

    for emotion, count in emotion_counts.items():
        cv2.putText(
            overlay,
            f"{emotion.capitalize()}: {count}",
            (x_text, y_text),
            font,
            font_scale,
            (255, 255, 255),
            font_thickness,
            cv2.LINE_AA
        )
        y_text += line_height

    # Merge overlay with some transparency
    alpha = 0.6
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


# ---------------------- SETUP WEBCAM ---------------------- #
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Optionally load a logo if desired (make sure `overlay_img` is not None)
overlay_img = None
# overlay_img = cv2.imread("path_to_logo.png", cv2.IMREAD_UNCHANGED)


# ---------------------- MAIN LOOP ------------------------- #
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame from webcam.")
        break

    # Flip the frame horizontally for mirror effect; resize for consistency
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (600, 400))

    # ---------------- GESTURE DETECTION ---------------- #
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    detected_gesture = None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            detected_gesture = detect_gesture(
                hand_landmarks,
                frame_width=frame.shape[1],
                is_mirror=True
            )

    # Key press logic
    if detected_gesture:
        if detected_gesture == 'down':
            press_key(detected_gesture)  # Press and hold 'down'
        else:
            click_key(detected_gesture)  # Press once for other directions
    else:
        release_key()

    # ---------------- EMOTION DETECTION ---------------- #
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_face_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)
    faces = face_cascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    for (x, y, w_face, h_face) in faces:
        face_roi = rgb_face_frame[y:y+h_face, x:x+w_face]
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        emotion_counts[emotion] += 1

        cv2.rectangle(frame, (x, y), (x + w_face, y + h_face), (0, 0, 255), 2)
        cv2.putText(
            frame,
            emotion,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )

    # ---------------- CUSTOM UI + LOGO ---------------- #
    draw_custom_ui(frame)

    # Optional: place your logo in the bottom-right corner
    if overlay_img is not None:
        h_logo, w_logo, _ = overlay_img.shape
        x_offset = frame.shape[1] - w_logo - 10
        y_offset = frame.shape[0] - h_logo - 10

        if overlay_img.shape[2] == 4:
            # If the logo has an alpha channel
            bgr_img = overlay_img[:, :, :3]
            alpha_channel = overlay_img[:, :, 3] / 255.0
            for c in range(3):
                frame[y_offset:y_offset+h_logo, x_offset:x_offset+w_logo, c] = (
                    frame[y_offset:y_offset+h_logo, x_offset:x_offset+w_logo, c] *
                    (1 - alpha_channel) +
                    bgr_img[:, :, c] * alpha_channel
                )
        else:
            frame[y_offset:y_offset+h_logo, x_offset:x_offset+w_logo] = overlay_img

    # Show the final integrated view
    cv2.imshow("Gesture + Emotion Detection (Modern UI)", frame)

    # Print emotion counts (optional)
    print("Emotion Counts:", emotion_counts)

    # --------------- Key Handling for Quit & Reset --------------- #
    key = cv2.waitKey(1) & 0xFF
    # Press 'q' to quit
    if key == ord('q'):
        break
    # Press 'r' to reset both gesture and emotion counters
    elif key == ord('r'):
        for g in gesture_counts:
            gesture_counts[g] = 0
        for e in emotion_counts:
            emotion_counts[e] = 0
        print("All counters have been reset.")

# After collecting emotion and gesture counts
analytics_data = {
    "emotion_counts": emotion_counts,
    "gesture_counts": gesture_counts,
    "performance": {
        "level": current_level,
        "score": current_score
    },
}

# Send data to the backend
response = requests.post('http://127.0.0.1:5000/submit-data', json=analytics_data)
print(response.json())

# ---------------------- CLEANUP ------------------------- #
cap.release()
cv2.destroyAllWindows()

# Optionally save the final emotion counts
with open("emotion_counts.txt", "w") as f:
    for emotion, count in emotion_counts.items():
        f.write(f"{emotion}: {count}\n")