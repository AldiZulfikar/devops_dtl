import cv2
import numpy as np
import torch

weights = torch.load("/model/weights_best.pth", map_location='cpu')

class_names = ["buggy", "clean"]

# def predict(x):
#     image=cv2.imread(x)
#     image_resized= cv2.resize(image, (180,180))
#     image=np.expand_dims(image_resized,axis=0)
#     pred=model.predict(image)
#     output_class=class_names[np.argmax(pred)]
#     return output_class