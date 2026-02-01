import cv2

backends = [
    ("CAP_ANY", cv2.CAP_ANY),
    ("CAP_DSHOW", cv2.CAP_DSHOW),
    ("CAP_MSMF", cv2.CAP_MSMF),
]

for name, backend in backends:
    cap = cv2.VideoCapture(1, backend)
    opened = cap.isOpened()
    read_ok = False
    if opened:
        ret, frame = cap.read()
        read_ok = ret
    cap.release()
    print(f"{name}: opened={opened}, read={read_ok}")
