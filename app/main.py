from flask import Flask, render_template, request, jsonify
import cv2
import colorMap
from torch_utils import transform_image, get_predict

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

label_data = ['Buggy', 'Clean']

ALLOWED_EXTENSIONS = {'java', 'py', 'php'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename == "":
            # return jsonify({'error': 'no file'})
            return render_template("index.html", prediction = 'No File Submitted', img_path = 'static/images/no_file.png')
        if not allowed_file(file.filename):
            # return jsonify({'error': 'format not supported'})
            return render_template("index.html", prediction = 'Format Not Supported', img_path = 'static/images/not_supported.png')

        fileCode = "static/predict_result/" + file.filename

        file.save(fileCode)

        im = colorMap.get_new_color_img(fileCode)
        
        img_path = fileCode + '.png'

        cv2.imwrite(img_path, im)

    try:
        img_bytes = cv2.imread(img_path)
        tensor = transform_image(img_bytes)
        prediction = get_predict(tensor)
        data = label_data[prediction.item()]
        # return jsonify(data)
        return render_template("index.html", prediction = data, img_path = img_path)
    except:
        # return jsonify({'error': 'Error during prediction'})
        return render_template("index.html", prediction = 'Error during prediction')