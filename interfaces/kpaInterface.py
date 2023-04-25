"""
import infery
import numpy as np
from tensorflow import keras
from PIL import Image

class KPAia:
    def __init__(self, modelPath='/code/apiutils/models/model.zip', modelType='tf2', inputSize=(640,640)) -> None:
        self.modelPath = modelPath
        self.modelType = modelType
        self.inputSize = inputSize
        self.model = infery.load(modelPath, framework_type=modelType, inference_hardware='cpu')

    def predict(self, preImg) -> object:    
        image_pil_res = preImg.resize( size=self.inputSize, resample=Image.Resampling.NEAREST) 
        image_pil_res_arr = keras.preprocessing.image.img_to_array(image_pil_res)
        del image_pil_res
        image_pil_res_arr /= 255
        model_preds = self.model.predict(np.asarray([image_pil_res_arr]) )
        return model_preds[0][0]

    
    def resize(self, img) -> object:
        return img.resize(self.inputSize)
    
KPAia_model = KPAia('/code/apiutils/models/model.zip', 'tf2', (224, 224))
"""

import torch
from PIL import Image
from io import BytesIO
class yoloMultDetect:
    def __init__(self) -> None:
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s') 
    def predict(self, img):
        self.results = self.model(img)
    
    def digest2JSON(self):
        data = {}
        data['objects'] = []
        for detection in self.results.pred:
            for x1, y1, x2, y2, conf, cls in detection:
                obj = {}
                obj['label'] = self.model.names[int(cls)]
                obj['confidence'] = float(conf)
                obj['coordinates'] = [int(x1), int(y1), int(x2), int(y2)]
                obj['width'] = int(x2)-int(x1)
                obj['height'] = int(y2)-int(y1)
                obj['center'] = [int(obj['width']/2) , int(obj['height']/2)]
                data['objects'].append(obj)
        return data
    
    def digest2Image(self):
        img_jpg = Image.fromarray(self.results.render()[0])
        buffer = BytesIO()
        img_jpg.save(buffer, format='JPEG')
        buffer.seek(0)
        del img_jpg
        return buffer
    
KPAia_model = yoloMultDetect()