from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import cv2
import numpy as np
import tensorflow as tf

import colorMap
import codeVis

app = Flask(__name__)
port = 5100

with open('sdp_resnet_model.json', 'r') as json_file:
    json_savedModel= json_file.read()

model = tf.keras.models.model_from_json(json_savedModel)
model.load_weights('resnet_model.h5')
model.compile(optimizer='adam',loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

class_names = ["buggy", "clean"]

def predict(x):
    image=cv2.imread(x)
    image_resized= cv2.resize(image, (180,180))
    image=np.expand_dims(image_resized,axis=0)
    pred=model.predict(image)
    output_class=class_names[np.argmax(pred)]
    return output_class

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("test.html")

@app.route("/about")
def about_page():
    return "Hai"

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        sourceCode = request.files['my_image']

        fileCode = "static/" + sourceCode.filename

        sourceCode.save(fileCode)

        im = colorMap.get_new_color_img(fileCode)
        
        img_path = fileCode + '.png'

        cv2.imwrite(img_path, im)

        p = predict(img_path)

        # img_path = "static/" + img.filename	
        # img.save(img_path)

        # p = predict(img_path)

    return render_template("test.html", prediction = p, img_path = img_path)

if __name__ =='__main__':
    app.run(host="0.0.0.0", port=port)