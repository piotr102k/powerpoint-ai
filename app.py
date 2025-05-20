import cv2
import numpy as np
import time
import ctypes
from keras.models import load_model
from keras.preprocessing import image

# Load your single 3-class model
model = load_model('prawus.keras')  # replace with your model path
VK_LEFT = 0x25
VK_RIGHT = 0x27
KEYEVENTF_KEYDOWN = 0
KEYEVENTF_KEYUP = 2

def press_key(hexKeyCode):
    ctypes.windll.user32.keybd_event(hexKeyCode, 0, KEYEVENTF_KEYDOWN, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(hexKeyCode, 0, KEYEVENTF_KEYUP, 0)


def preprocess_image(frame, target_size=(320, 240)):
    # Grayscale
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Resize to model input size (240x320)
    img = cv2.resize(img, target_size)
    img_array = img / 255.0
    img_array = np.expand_dims(img_array, axis=-1)
    img_array = np.expand_dims(img_array, axis=-0)
    # Expand dims to (1, height, width, channels=1)
   # add batch dim
    return img_array

def predict_direction(img):
    preds = model.predict(img)  # preds shape: (1, 3)
    preds = preds[0]  # remove batch dim
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

            # Optionally, only update direction if confidence > threshold
            if confidence < 0.7:
                direction = "no"
            # Press left arrow
            if direction=="left":
                press_key(VK_LEFT)
            if direction=="right":
                press_key(VK_RIGHT)

            print(f"Predicted: {direction} (confidence: {confidence:.2f})")

        cv2.putText(frame, direction, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Direction Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()