import json
import os

def bdd100k_json_txt(categories,jsonFile,writepath):
    f = open(jsonFile)
    info = json.load(f)
    #print(len(info))
    #print(info["name"])

    for obj in info["frames"]:
        #print(obj["objects"])
        strs = ""
        for objects in obj["objects"]:
            #print(objects)
            if objects["category"] in categories:
                dw = 1.0 / 1280
                dh = 1.0 / 720
                strs += str(categories.index(objects["category"]))
                strs += " "
                strs += str(((objects["box2d"]["x1"] + objects["box2d"]["x2"]) / 2.0) * dw)[0:8]
                strs += " "
                strs += str(((objects["box2d"]["y1"] + objects["box2d"]["y2"]) / 2.0) * dh)[0:8]
                strs += " "
                strs += str(((objects["box2d"]["x2"] - objects["box2d"]["x1"])) * dw)[0:8]
                strs += " "
                strs += str(((objects["box2d"]["y2"] - objects["box2d"]["y1"])) * dh)[0:8]
                strs += "\n"
        if strs!="":
            write = open(writepath + "%s.txt" % info["name"], 'w')
            write.writelines(strs)
            write.close()
            # print("%s has been dealt!" % info["name"])
        else:
            print("%s has been dealt!" % info["name"])


# 加载JSON文件
def load_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 转换为YOLO格式标签的函数
def convert_to_yolo_format(annotation, img_info):
    category_id = annotation['category_id']
    # 检查 category_id 是否在映射字典中
    if category_id not in category_mapping:
        # 如果 category_id 不在映射字典中，则忽略这个注释
        return None
    bbox = annotation['bbox']
    
    # 获取图像的宽度和高度
    img_width = img_info['width']
    img_height = img_info['height']
    
    # YOLO 格式为 (class_id, center_x, center_y, width, height)，归一化为[0, 1]
    x_min, y_min, box_width, box_height = bbox
    center_x = (x_min + box_width / 2) / img_width
    center_y = (y_min + box_height / 2) / img_height
    norm_width = box_width / img_width
    norm_height = box_height / img_height
    
    # 返回 YOLO 格式的标签
    return f"{category_mapping[category_id]} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}"

# 保存YOLO标签到文件
def save_yolo_labels(output_dir, image_file_name, labels):
    label_file_name = image_file_name.replace('.jpg', '.txt')
    label_file_path = os.path.join(output_dir, label_file_name)
    
    with open(label_file_path, 'w') as f:
        f.write('\n'.join(labels))

# 主函数：读取 JSON 并转换标签格式
def json_to_yolo(json_file_path, output_dir):
    data = load_json(json_file_path)
    
    # 提取图像信息
    image_info = {img['id']: img for img in data['images']}
    
    # 创建一个字典，用于按 image_id 收集每张图片的所有标注
    annotations_by_image = {}

    # 遍历所有注释
    for annotation in data['annotations']:
        img_id = annotation['image_id']
        img_info = image_info[img_id]
        
        # 获取 YOLO 格式的标签
        label = convert_to_yolo_format(annotation, img_info )
        # 如果 label 为 None，说明这个类别不需要处理，跳过
        if label is None:
            continue
        
        # 如果该图片还没有标签，初始化一个空列表
        if img_id not in annotations_by_image:
            annotations_by_image[img_id] = []
        
        # 将该注释的标签加入该图片的标签列表
        annotations_by_image[img_id].append(label)
    
    # 保存每张图片的所有标签到对应的文件
    for img_id, labels in annotations_by_image.items():
        image_file_name = image_info[img_id]['file_name']
        save_yolo_labels(output_dir, image_file_name, labels)



if __name__ == "__main__":
    ####################args#####################
    # categories = ['traffic light', 'traffic sign', 'car', 'person', 'bus', 'truck', 'riderss',
    #              'bike', 'motor', 'cone', 'barrier', 'opendoor', 'wheel', 'tail']    # 自己需要从BDD数据集里提取的目标类别
    # readpath = r"SSLAD-2D/labeled/annotations/train"   # BDD数据集标签读取路径，这里需要分两次手动去修改train、val的地址
    # writepath = r"/home/yangtengkun/yolov8/data/SSLAD-2D/labels/train"	# BDD数据集转换后的标签保存路径

    # fileList = os.listdir(readpath)
    # #print(fileList)
    # for file in fileList:
    #     # print(file)
    #     filepath = readpath + file
    #     bdd100k_json_txt(categories, filepath, writepath)
    # 定义类别映射，从category_id转换为yolo格式中的类别索引
    
    # soda10m
    # category_mapping = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}

    # coda
    # category_mapping = {1: 0, 2: 1, 3: 2, 4: 3, 7: 4, 8: 7, 10: 6, 26: 9, 27: 8}
    # soda10m
    category_mapping = {1: 0, 2: 1, 3: 2, 4: 3, 6: 5}
    # 设置路径并调用转换函数
    json_file_path = '/home/yangtengkun/yolov8/data/CODA2022/annotations_val.json'  # 替换为你的JSON文件路径
    output_dir = '/home/yangtengkun/yolov8/data/CODA2022/val/labels'  # 替换为你想保存标签文件的目录

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 执行转换
    json_to_yolo(json_file_path, output_dir)
