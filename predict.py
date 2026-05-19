from ultralytics import YOLO
import cv2

# Load the best trained model
model = YOLO('runs/detect/train/weights/best.pt')

# Run detection on an image
results = model.predict(source='test.jpg', show=True)  # change to your image path

# To detect in video or webcam:
# results = model.predict(source=0, show=True)  # for webcam
# results = model.predict(source='video.mp4', show=True)  # for video file