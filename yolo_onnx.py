from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO(r"E:\repository\model\yolov8_9_21.onnx")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
# results = model.predict(source="0")
# results = model.predict(source="folder", show=True) # Display preds. Accepts all YOLO predict arguments

# from PIL
# im1 = Image.open()
img_path = r"E:\repository\ultralytics\img\mixture11.jpeg"
results = model.predict(source=img_path, save=True)  # save plotted images
img = cv2.imread(img_path)
for box in results[0].boxes.cpu().numpy():
    r = box.xyxy[0].astype(int)
    print(r)
    img = cv2.rectangle(img,[r[0],r[1]] ,[r[2],r[3]] , (255, 255, 255), 2)
cv2.imshow('draw',img)
cv2.waitKey(0)
# # from ndarray
# im2 = cv2.imread(r"E:\repository\Smart-Trash-Can\datasets\smart_can\images\train\WIN_20230901_17_19_41_Pro.jpg")
# results = model.predict(source=im2, save=True, save_txt=True)  # save predictions as labels

# # from list of PIL/ndarray
# results = model.predict(source=[im1, im2])
