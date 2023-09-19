from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO(r"E:\竞赛科研\工训赛\model\best.onnx")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
# results = model.predict(source="0")
# results = model.predict(source="folder", show=True) # Display preds. Accepts all YOLO predict arguments

# from PIL
im1 = Image.open(r"D:\desktop\Snipaste_2023-09-18_16-52-54.png")
results = model.predict(source=im1, save=True)  # save plotted images
print(results)
# # from ndarray
# im2 = cv2.imread(r"E:\repository\Smart-Trash-Can\datasets\smart_can\images\train\WIN_20230901_17_19_41_Pro.jpg")
# results = model.predict(source=im2, save=True, save_txt=True)  # save predictions as labels

# # from list of PIL/ndarray
# results = model.predict(source=[im1, im2])
