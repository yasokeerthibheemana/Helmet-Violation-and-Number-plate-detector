from ultralytics import YOLO

# Load the YOLO model
model = YOLO('yolov8n.pt')

# Train the model
model.train(data=r"C:\Users\Yaso keerthi\OneDrive\Desktop\helmet detection\data.yaml"),
epochs=10,        # number of training rounds
imgsz=640,        # image size
device='cpu'      # use CPU
