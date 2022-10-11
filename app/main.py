from flask import Flask, request, jsonify
import cv2
import colorMap
from torch import tensor
from torch_utils import transform_image, get_predict
import json

app = Flask(__name__)

label_data = ['buggy', 'clean']

ALLOWED_EXTENSIONS = {'java', 'py', 'php'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route("/", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({'error': 'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'format not supported'})

        fileCode = "../static/" + file.filename

        file.save(fileCode)

        im = colorMap.get_new_color_img(fileCode)
        
        img_path = fileCode + '.png'

        cv2.imwrite(img_path, im)

        # try:
        img_bytes = cv2.imread(img_path)
        tensor = transform_image(img_bytes)
        prediction = get_predict(tensor)
        data = {'prediction': label_data[prediction.item()]}
        return jsonify(data)
        # except:
        #     return jsonify({'error': file})
