import os
import cv2
import numpy as np
import time
import ctypes
from keras.models import load_model

model = load_model(os.getcwd() + '/prawus.keras')
VK_LEFT = 0x25
VK_RIGHT = 0x27
KEYEVENTF_KEYDOWN = 0
KEYEVENTF_KEYUP = 2

def press_key(hexKeyCode):
    ctypes.windll.user32.keybd_event(hexKeyCode, 0, KEYEVENTF_KEYDOWN, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(hexKeyCode, 0, KEYEVENTF_KEYUP, 0)


def preprocess_image(frame, target_size=(320, 240)):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, target_size)

    img_array = img / 255.0
    img_array = np.expand_dims(img_array, axis=-1)
    img_array = np.expand_dims(img_array, axis=-0)

    return img_array

def predict_direction(img):
    preds = model.predict(img)
    preds = preds[0]
    classes = ['left', 'right', 'no']
    predicted_class_idx = np.argmax(preds)
    confidence = preds[predicted_class_idx]
    return classes[predicted_class_idx], confidence

def main():
    cap = cv2.VideoCapture(0)
    direction = "no"
    last_capture = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        if current_time - last_capture >= 0.5:
            last_capture = current_time

            input_img = preprocess_image(frame)
            direction, confidence = predict_direction(input_img)

            if confidence < 0.7:
                direction = "no"

            if direction=="left":
                press_key(VK_LEFT)
            if direction=="right":
                press_key(VK_RIGHT)

            print(f"Predicted: {direction} (confidence: {confidence:.2f})")

        cv2.putText(frame, direction, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Direction Detection", frame)

        if cv2.waitKey(1) == 27 or cv2.getWindowProperty("Direction Detection", 4) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
