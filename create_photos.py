import cv2
from datetime import datetime
from PIL import Image

def main():
    cap = cv2.VideoCapture(0)
    direction="no"
    while True:
        ret, frame = cap.read()
        display_frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (320,240))
        display_frame = cv2.resize(display_frame, (960,720))

        key = cv2.waitKey(1)
        cv2.putText(display_frame, direction, (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Lmao", display_frame)

        if key == 13:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            filename = direction + "_" +datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + f"_{datetime.now().microsecond // 1000:03d}"+".jpg"
            image = Image.fromarray(gray_frame)
            image = image.convert("L") 
            image.save(filename)
            print(f"pstryk!! [{filename}] ")

        if key == 97:
            direction="left"
        if key == 115:
            direction="no"
        if key == 100:
            direction="right"

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()