import cv2
import mediapipe as mp
import random
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

balloons = []
score = 0
width, height = 640, 480
radius = 30
font = cv2.FONT_HERSHEY_SIMPLEX

balloon_colors = [
    (0, 255, 0),   
    (255, 0, 0),   
    (0, 0, 255),  
    (255, 255, 0), 
    (255, 0, 255),  
    (0, 255, 255),  
]

class Balloon:
    def __init__(self):
        self.x = random.randint(50, width - 50)
        self.y = 0
        self.speed = random.randint(2, 5)
        self.color = random.choice(balloon_colors)  

    def move(self):
        self.y += self.speed

    def draw(self, frame):
        cv2.circle(frame, (self.x, self.y), radius, self.color, -1)

    def is_popped(self, finger_x, finger_y):
        return (self.x - finger_x)**2 + (self.y - finger_y)**2 < radius**2

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    finger_x = finger_y = -1

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            index_finger_tip = hand_landmarks.landmark[8]
            finger_x = int(index_finger_tip.x * width)
            finger_y = int(index_finger_tip.y * height)
            cv2.circle(frame, (finger_x, finger_y), 10, (255, 0, 0), -1)

    if random.randint(1, 40) == 1:
        balloons.append(Balloon())

    new_balloons = []
    for balloon in balloons:
        balloon.move()
        if balloon.y < height:
            if balloon.is_popped(finger_x, finger_y):
                score += 1
            else:
                new_balloons.append(balloon)

    balloons = new_balloons

    for balloon in balloons:
        balloon.draw(frame)

    cv2.putText(frame, f'Score: {score}', (10, 40), font, 1, (255, 255, 255), 2)

    cv2.imshow("Gesture Shooter", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()