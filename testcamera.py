import cv2

def test_camera(index):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # use DirectShow backend on Windows
    if not cap.isOpened():
        print(f"Camera {index}: failed to open")
        return False
    ret, frame = cap.read()
    if not ret:
        print(f"Camera {index}: opened but failed to read a frame")
        cap.release()
        return False
    print(f"Camera {index}: opened successfully ({frame.shape[1]}x{frame.shape[0]})")
    cap.release()
    return True

for idx in range(4):
    test_camera(idx)