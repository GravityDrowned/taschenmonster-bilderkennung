import numpy as np
import cv2

def read_video(path):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print("Error opening video stream or file")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()



def main():
    read_video("data/fight.MOV")


    print("Hello from pkmn!")


if __name__ == "__main__":
    main()
