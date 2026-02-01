import cv2

# Try camera index 0 with MSMF backend
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
print(f"Camera 0 opened: {cap.isOpened()}")
if cap.isOpened():
    ret, frame = cap.read()
    print(f"Read success: {ret}, shape: {frame.shape if ret else 'N/A'}")
cap.release()