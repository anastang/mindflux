import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np
from deepface import DeepFace
import requests

# ------------------ GESTURE DETECTION SETUP ------------------ #
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# To track whether a key is currently being held down
current_key = None
last_press_time = time.time()  # Track the last press time
press_delay = 0.2  # Delay between key presses (in seconds)

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
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

emotion_counts = {
    "happy": 0, "sad": 0, "angry": 0,
    "fear": 0, "surprise": 0, "disgust": 0, "neutral": 0
}

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
        thumb_tip.x = 1 - thumb_tip.x
        index_tip.x = 1 - index_tip.x
        middle_tip.x = 1 - middle_tip.x
        ring_tip.x = 1 - ring_tip.x
        pinky_tip.x = 1 - pinky_tip.x
        wrist.x = 1 - wrist.x

    # Gesture: Up (all fingers extended and well spread)
    if (all([
        index_tip.y < wrist.y,  # Above wrist
        middle_tip.y < wrist.y,
        ring_tip.y < wrist.y,
        pinky_tip.y < wrist.y
    ]) and abs(thumb_tip.x - pinky_tip.x) > 0.3):
        return 'up'

    # Gesture: Down (fist gesture, all fingers curled)
    if (
        all([
            index_tip.y > wrist.y,
            middle_tip.y > wrist.y,
            ring_tip.y > wrist.y,
            pinky_tip.y > wrist.y
        ]) and abs(index_tip.x - thumb_tip.x) < 0.1
    ):
        return 'down'

    # Gesture: Left (index and thumb extended, others curled)
    if (
        index_tip.y < wrist.y
        and middle_tip.y > index_tip.y
        and abs(index_tip.x - thumb_tip.x) > 0.1
        and (index_tip.x < thumb_tip.x if not is_mirror else index_tip.x > thumb_tip.x)
    ):
        return 'left'

    # Gesture: Right (index and thumb extended, others curled)
    if (
        index_tip.y < wrist.y
        and middle_tip.y > index_tip.y
        and abs(index_tip.x - thumb_tip.x) > 0.1
        and (index_tip.x > thumb_tip.x if not is_mirror else index_tip.x < thumb_tip.x)
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
#  Overlay helper functions (counts, performance, etc.)
# ----------------------------------------------------------------- #
def draw_background(frame, text_position, color, transparency=0.6):
    x, y = text_position
    text = f"Up: {gesture_counts['up']} | Down: {gesture_counts['down']} | Left: {gesture_counts['left']} | Right: {gesture_counts['right']}"
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    overlay = frame.copy()
    cv2.rectangle(overlay, (x - 10, y - 50), (x + text_width + 10, y + text_height + 10), color, -1)
    cv2.addWeighted(overlay, transparency, frame, 1 - transparency, 0, frame)
    cv2.putText(frame, text, (x, y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

def draw_performance(frame):
    total_gestures = sum(gesture_counts.values())
    if total_gestures == 0:
        performance_percentage = 0
    else:
        # Arbitrary "performance" definition
        performance_percentage = (total_gestures / (4 * max(gesture_counts.values(), default=1))) * 100

    performance_text = f"Performance: {performance_percentage:.2f}%"
    cv2.putText(frame, performance_text, (10, frame.shape[0] - 10), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

# ---------------------- SETUP WEBCAM ---------------------- #
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Suppose you have some variables for performance analytics
current_level = 1
current_score = 0

# Optionally, if you have a logo image, load it here (ensure overlay_img is not None if you have an image)
overlay_img = None
# overlay_img = cv2.imread("path_to_your_logo_image.png", cv2.IMREAD_UNCHANGED)

# ---------------------- MAIN LOOP ------------------------- #
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame from webcam.")
        break

    # Flip the frame horizontally for mirror effect; resize for consistency
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (600, 400))

    # Draw a thick border around the frame
    border_thickness = 25
    frame_height, frame_width, _ = frame.shape
    border_color = (0, 46, 0)  # Border colour
    cv2.rectangle(frame, (0, 0), (frame_width - 1, frame_height - 1), border_color, border_thickness)

    # ---------------- GESTURE DETECTION ---------------- #
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    detected_gesture = None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            detected_gesture = detect_gesture(hand_landmarks, frame_width=frame.shape[1], is_mirror=True)

    # Key press logic
    if detected_gesture:
        if detected_gesture == 'down':
            press_key(detected_gesture)    # press and hold 'down'
        else:
            click_key(detected_gesture)    # press once for other directions
    else:
        release_key()

    # ---------------- EMOTION DETECTION ---------------- #
    # For face detection, we need a grayscale image
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # For DeepFace, we can use an RGB version of the grayscale or the original frame
    rgb_face_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        face_roi = rgb_face_frame[y:y+h, x:x+w]
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        emotion_counts[emotion] += 1

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # ---------------- OVERLAYS & LOGGING ---------------- #
    # Draw gesture counts
    draw_background(frame, (10, 50), (0, 0, 0))
    # Draw performance
    draw_performance(frame)

    # Show the final integrated view
    cv2.imshow("Gesture + Emotion Detection", frame)

    # Print emotion counts (optional, remove if too spammy)
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
    "performance": {"level": current_level, "score": current_score},
}

# Send data to the backend
response = requests.post('http://127.0.0.1:5000/submit-data', json=analytics_data)
print(response.json())
# ---------------------- CLEANUP ------------------------- #
cap.release()
cv2.destroyAllWindows()

with open("emotion_counts.txt", "w") as f:
    for emotion, count in emotion_counts.items():
        f.write(f"{emotion}: {count}\n")
