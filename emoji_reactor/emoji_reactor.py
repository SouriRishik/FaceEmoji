import cv2
import mediapipe as mp
import numpy as np
import pygame

mp_face = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

face = mp_face.FaceMesh(min_detection_confidence=0.6, min_tracking_confidence=0.6)
hands = mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6)
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Emoji Output")

emojis = {
    "straight_face": pygame.image.load("emojis/straight.jpg"),
    "smiling": pygame.image.load("emojis/smile.jpg"),
    "hands_up": pygame.image.load("emojis/handsup.jpg")
}

current_state = "straight_face"
state_buffer = []
STABILITY_FRAMES = 7  
smile_confidence_buffer = []
CONFIDENCE_BUFFER_SIZE = 3 

def detect_smile_with_confidence(landmarks, w, h):
    left_corner = (int(landmarks[61].x * w), int(landmarks[61].y * h))
    right_corner = (int(landmarks[291].x * w), int(landmarks[291].y * h))
    top_lip = (int(landmarks[13].x * w), int(landmarks[13].y * h))
    bottom_lip = (int(landmarks[14].x * w), int(landmarks[14].y * h))

    left_upper = (int(landmarks[84].x * w), int(landmarks[84].y * h))
    right_upper = (int(landmarks[314].x * w), int(landmarks[314].y * h))
    
    mouth_width = abs(right_corner[0] - left_corner[0])
    mouth_height = abs(bottom_lip[1] - top_lip[1])

    mouth_center_y = (top_lip[1] + bottom_lip[1]) / 2
    left_lift = mouth_center_y - left_upper[1]
    right_lift = mouth_center_y - right_upper[1]
    avg_lift = (left_lift + right_lift) / 2

    width_height_ratio = mouth_width / mouth_height if mouth_height != 0 else 0

    width_score = min(width_height_ratio / 2.5, 1.0) 
    lift_score = min(max(avg_lift / 5.0, 0.0), 1.0)
    
    confidence = (width_score + lift_score) / 2
    return confidence

def is_smiling_with_hysteresis(confidence, current_state):

    ENTER_SMILE_THRESHOLD = 0.3 
    EXIT_SMILE_THRESHOLD = 0.2
    
    if current_state == "smiling":
        return confidence > EXIT_SMILE_THRESHOLD
    else:
        return confidence > ENTER_SMILE_THRESHOLD


def detect_hands_up(hand_landmarks, img_h, img_w):

    for hand in hand_landmarks:
        wrist_y = hand.landmark[0].y * img_h
        if wrist_y < img_h * 0.5:
            return True
    return False

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_results = face.process(rgb)
    hand_results = hands.process(rgb)

    emotion_state = "straight_face"

    if face_results.multi_face_landmarks:
        for f_landmarks in face_results.multi_face_landmarks:
            smile_confidence = detect_smile_with_confidence(f_landmarks.landmark, w, h)

            smile_confidence_buffer.append(smile_confidence)
            if len(smile_confidence_buffer) > CONFIDENCE_BUFFER_SIZE:
                smile_confidence_buffer.pop(0)

            avg_confidence = sum(smile_confidence_buffer) / len(smile_confidence_buffer)
            
            if is_smiling_with_hysteresis(avg_confidence, current_state):
                emotion_state = "smiling"


    if hand_results.multi_hand_landmarks:
        if detect_hands_up(hand_results.multi_hand_landmarks, h, w):
            emotion_state = "hands_up"

    state_buffer.append(emotion_state)
    if len(state_buffer) > STABILITY_FRAMES:
        state_buffer.pop(0)

    if len(state_buffer) >= STABILITY_FRAMES:
        if all(state == emotion_state for state in state_buffer):
            current_state = emotion_state

    text = f"STATE: {current_state.upper()} ???"
    cv2.putText(frame, text, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    quit_text = "Press q to quit"
    cv2.putText(frame, quit_text, (30, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imshow("Camera Feed", frame)

    screen.fill((0, 0, 0))
    emoji_img = emojis[current_state]
    rect = emoji_img.get_rect(center=(200, 200))
    screen.blit(emoji_img, rect)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            exit()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
