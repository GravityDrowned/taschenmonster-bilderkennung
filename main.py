import numpy as np
import cv2
import pytesseract
from matplotlib import pyplot as plt

def get_text_from_frame(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #extracted_text = pytesseract.image_to_string(gray, 'eng')
    data = pytesseract.image_to_data(gray, lang='eng', output_type=pytesseract.Output.DICT)

    n_boxes = len(data['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    plt.figure(figsize=(10, 6))
    plt.imshow(img)
    plt.title("Image with Text Bounding Boxes")
    plt.axis("off")
    plt.show()

def read_video(path):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print("Error opening video stream or file")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Frame', frame)

            text = get_text_from_frame(frame)

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
