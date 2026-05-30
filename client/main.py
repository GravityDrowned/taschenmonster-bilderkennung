import sys
import os
import time

import cv2
import httpx
from doctr.models import ocr_predictor

# Allow importing state_machine.py from the repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from state_machine import get_states

PI_URL = "http://192.168.178.52:8000"

predictor = None


def wait_for_server(url: str, timeout: int = 60):
    print(f"Waiting for Pi server at {url}...", flush=True)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = httpx.get(url + "/health", timeout=3)
            if resp.status_code == 200:
                print("Pi server is ready.", flush=True)
                return
        except Exception:
            pass
        print("  Server not ready yet, retrying in 2s...", flush=True)
        time.sleep(2)
    raise TimeoutError(f"Pi server at {url} did not respond within {timeout} seconds.")


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


def send_states(states: list):
    if not states:
        return
    try:
        resp = httpx.post(PI_URL + "/play", json={"states": states}, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        print(f"Warning: failed to send states {states} to Pi: {e}", flush=True)


def read_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error opening video stream or file", flush=True)
        return

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
            print(states, flush=True)

            send_states(states)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


def main():
    global predictor
    print("Loading OCR model...", flush=True)
    predictor = ocr_predictor(pretrained=True)
    print("OCR model loaded.", flush=True)
    wait_for_server(PI_URL)
    read_webcam()


if __name__ == "__main__":
    main()
