from keras.models import load_model
import cv2
import numpy as np
import tensorflow as tf

with open('static/model/sdp_resnet_model_log4.json', 'r') as json_file:
    json_savedModel= json_file.read()

model = tf.keras.models.model_from_json(json_savedModel)
model.load_weights('static/model/resnet_model_log4.h5')
model.compile(optimizer='adam',loss = tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])

class_names = ["Buggy", "Clean"]

def preds(x):
    image=cv2.imread(x)
    image_resized= cv2.resize(image, (180,180))
    image=np.expand_dims(image_resized,axis=0)
    pred=model.predict(image)
    output_class=class_names[np.argmax(pred)]
    return output_class