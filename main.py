import cv2
from doctr.models import ocr_predictor

from controller import play, init
from state_machine import get_states

predictor = ocr_predictor(pretrained=True)

def get_text_from_frame(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = predictor([rgb])
    return result.render()

def draw_bounding_boxes_on_frame(img):
    h_img, w_img = img.shape[:2]
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = predictor([rgb])
    get_states(result.render())
    for block in result.pages[0].blocks:
        for line in block.lines:
            for word in line.words:
                geo = word.geometry
                x = int(geo[0][0] * w_img)
                y = int(geo[0][1] * h_img)
                x2 = int(geo[1][0] * w_img)
                y2 = int(geo[1][1] * h_img)
                cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 2)
    cv2.imshow('Frame', img)

def read_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("Error opening video stream or file")

    controller_index = init()

    i = 1
    while cap.isOpened():
        ret, frame = cap.read()
        if i % 60 != 0:
            i += 1
            continue
        i = 1
        if ret:
            cv2.imshow('Frame', frame)

            text = get_text_from_frame(frame)
            draw_bounding_boxes_on_frame(frame)
            states = get_states(text)
            print(states)

            play(controller_index, states)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

def main():
    read_video("data/fight.MOV")

if __name__ == "__main__":
    main()
