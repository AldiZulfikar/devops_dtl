from flask import Flask, render_template, request
import cv2
import colorMap
import codeVis
from pred import predict

app = Flask(__name__)
port = 5100

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

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

    return render_template("index.html", prediction = p, img_path = img_path)

if __name__ =='__main__':
    app.run(host="0.0.0.0", port=port)