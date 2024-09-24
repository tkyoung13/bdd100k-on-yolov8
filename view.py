from ultralytics import YOLO
# 加载训练好的模型或者网络结构配置文件
model = YOLO('/home/yangtengkun/yolov8/runs/detect/train/weights/best.pt')
# 打印模型参数信息
print(model.info())
print(model.info(detailed=True))

