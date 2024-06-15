import os
import shutil
import cv2
import numpy as np
import json
from ultralytics import YOLO

class Predict():
    def __init__(self, _s, _r, _g):
        # 首次加载模型
        # 先删除上次预测的文件夹
        if os.path.exists("./workspace/results/predict"):
            shutil.rmtree("./workspace/results/predict")

        self.model = YOLO(_g["MODEL"])
        # 主要是一个空检测，让加载模型到内存中
        self.model.predict(source="./variable/configs/verify.png")
        # 创建消息回调函数
        def _predict_(it):
            _g["PREDICT_INFO"] = it.infos
        # 添加回调函数
        self.model.add_callback("predict", _predict_)
        _g["LOADMODELFINISH"]=True
        with open(f"./variable/configs/types.json", "r", encoding="utf-8") as fp:
            self.typ = json.load(fp)

        while True:
            # 检测单张或者多张图片
            # 开启检测任务
            if len(_s) >0:
                for source in _s:
                    predict_name = source.split("/")[-1]
                    typ = predict_name.split(".")[-1]
                    if typ in self.typ["image"]:
                        # 保存对象结果
                        _g["VIDEOMODE"] = False
                        results = self.model.predict(source=source, save=True)
                        clist = results[0].boxes.cls.tolist()
                        classes = results[0].names
                        obj_text = ""
                        cset = set(clist)
                        for item in cset:
                            obj_text += f"{clist.count(item)}项{classes[item]};"
                        _r.append({"name": predict_name, "brief": obj_text})
                    # 检测视频
                    else:
                        _g["VIDEOMODE"] = True
                        self.model.predict(source=source, save=True)
                        _r.append({"name": predict_name, "brief": "检测完成!"})

                del _s[:]
                _r.append("finished")

            elif _g["CAMERASTREAM"] and len(_g["CAMERASTREAM"])>0:
                self.model.predict(source=_g["CAMERASTREAM"][0], save=True)
                _g["CAMERASTREAM"]=[]

def closePredict(dats):
    ret = {}
    # src = cv2.imread(dats["IMAGE"])
    src = cv2.imdecode(np.fromfile(dats["IMAGE"], dtype=np.uint8), -1)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if dats["BITNOT"]:
        thresh = cv2.bitwise_not(thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        if hierarchy[0][i][2] != -1:
            cv2.drawContours(src, [contours[i]], -1, (0, 255, 0), dats["LINEWIDTH"])
        else:
            cv2.drawContours(src, [contours[i]], -1, (0, 0, 255), dats["LINEWIDTH"])
        # print(cv2.isContourConvex(contours[i]))
        # print(cv2.contourArea(contours[i]))
    if not os.path.exists("./workspace/results/closed"):
        os.makedirs("./workspace/results/closed")
    # print(os.path.dirname(dats['IMAGE']))

    name = dats['IMAGE'].split('/')[-1]
    typ = name.split(".")[-1]
    cv2.imencode(f".{typ}", src)[1].tofile(f"./workspace/results/closed/{name}")
    ret["name"] = name

    return ret

def measureObject(dats):
    ret = {}
    # image = cv2.imread(dats["image"])
    image = cv2.imdecode(np.fromfile(dats["image"], dtype=np.uint8), -1)
    # 灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 二值化
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    dst = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    # 轮廓检测
    contours, hireachy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):
        # 求取轮廓的面积
        area = cv2.contourArea(contour)
        # 得到轮廓的外接矩形
        x, y, w, h = cv2.boundingRect(contour)
        # 求出宽高比
        rate = min(w, h) / max(w, h)
        # print("rectangle rate : %s" % rate)
        # 求取几何矩
        try:
            mm = cv2.moments(contour)
            # 得到中心位置
            cx = mm['m10'] / mm['m00']
            cy = mm['m01'] / mm['m00']
            # 绘制圆
            cv2.circle(image, (int(cx), int(cy)), 3, (0, 0, 255), -1)
        except:
            pass

        # 对每个轮廓绘制外接矩形
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), dats["linewidth"])
        # print("contour area %s" % area)


        cv2.circle(image, (int(x), int(y)), 3, (255, 0, 0), -1)
        cv2.circle(image, (int(x + w), int(y)), 3, (255, 0, 0), -1)
        cv2.circle(image, (int(x), int(y + h)), 3, (255, 0, 0), -1)
        cv2.circle(image, (int(x + w), int(y + h)), 3, (255, 0, 0), -1)

        cv2.putText(image, str(w), (int((x + w / 2)), y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), dats["fontsize"])
        cv2.putText(image, str(h), (x + w, y + int(h / 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), dats["fontsize"])
    if not os.path.exists("./workspace/results/measure"):
        os.makedirs("./workspace/results/measure")

    ret["name"] = dats['image'].split('/')[-1]
    typ = ret["name"].split(".")[-1]
    cv2.imencode(f".{typ}", image)[1].tofile(f"./workspace/results/measure/{ret['name']}")

    return ret

