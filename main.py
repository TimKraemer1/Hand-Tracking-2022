
import cv2
import mediapipe as mp
import pyautogui
import math

# mediapipe initializations
cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions .drawing_utils

width  = cap.get(3)  # float `width`
height = cap.get(4)  # float `height`
print(width, height)

index_point = (0, 0)
thumb_point = (0, 0)
middle_point = (0, 0)

click_status = False

up_status = True
down_status = False

scroll_status = True

while(True):
    ret, frame = cap.read()
    imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y*h)
                if id == 8:
                    index_point = (cx, cy)
                if id == 4:
                    thumb_point = (cx, cy)
                if id == 9:
                    cv2.circle(frame, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                    pyautogui.moveTo((1920-3*cx), (2.5*cy))
                if id == 12:
                    middle_point = (cx, cy)

                index_distance = math.sqrt((thumb_point[0] - index_point[0])**2 + (thumb_point[1] - index_point[1])**2)
                middle_distance = math.sqrt((thumb_point[0] - middle_point[0])**2 + (thumb_point[1] - middle_point[1])**2)
                if index_distance <= 35 and click_status == False:
                    click_status = True
                    pyautogui.click()
                elif index_distance > 35 and click_status == True:
                    click_status = False

                if middle_distance <= 35 and scroll_status == False:
                    scroll_status = True
                    pyautogui.scroll(-500)
                    print(True)
                elif middle_distance > 35 and scroll_status == True:
                    scroll_status = False


            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow('Output', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
