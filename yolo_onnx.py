from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO(r"E:\竞赛科研\工训赛\model\best.onnx")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
# results = model.predict(source="0")
# results = model.predict(source="folder", show=True) # Display preds. Accepts all YOLO predict arguments

# from PIL
# im1 = Image.open()
results = model.predict(source=r"E:\repository\yolov8_smart_can\data_test\tudou.png", save=True)  # save plotted images
img = cv2.imread(r"E:\repository\yolov8_smart_can\data_test\tudou.png")
for box in results[0].boxes.cpu().numpy():
    r = box.xyxy[0].astype(int)
    print(r)
    img_draw = cv2.rectangle(img, [0,0],[300,100] , (255, 255, 255), 2)
    cv2.imshow('draw',img_draw)
    cv2.waitKey(0)
# # from ndarray
# im2 = cv2.imread(r"E:\repository\Smart-Trash-Can\datasets\smart_can\images\train\WIN_20230901_17_19_41_Pro.jpg")
# results = model.predict(source=im2, save=True, save_txt=True)  # save predictions as labels

# # from list of PIL/ndarray
# results = model.predict(source=[im1, im2])
