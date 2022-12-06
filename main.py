from flask import Flask, render_template, request
from tf_utils import preds
import cv2
from colorMap import get_new_color_img

app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():
    return render_template("index.html")

def main():
    return render_template("index.html")

ALLOWED_EXTENSIONS = {'java', 'py', 'php', 'js', 'go'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/predict", methods = ['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file is None or file.filename == "":
            # return jsonify({'error': 'no file'})
            return render_template("index.html", prediction = 'No File Submitted', img_path = 'static/images/no_file.png')
        if not allowed_file(file.filename):
            # return jsonify({'error': 'format not supported'})
            return render_template("index.html", prediction = 'Format Not Supported', img_path = 'static/images/not_supported.png')

        fileCode = "/devops-dtl-app/app/static/predict_result/" + file.filename

        file.save(fileCode)

        im = get_new_color_img(fileCode)
        
        img_path = fileCode + '.png'

        cv2.imwrite(img_path, im)

    try:
        p = preds(img_path)
        return render_template("index.html", prediction = p, img_path = 'static/images/predictive.png')
    except Exception as err:
        # return jsonify({'error': 'Error during prediction'})
        return render_template("index.html", prediction = err)

if __name__ == '__main__':

    app.run(host="0.0.0.0")