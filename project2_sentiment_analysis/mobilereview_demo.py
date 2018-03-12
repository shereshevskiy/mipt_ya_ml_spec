__author__ = 'dmitry_sh'
from mobilereview_classifier import MobilereviewClassifier
from codecs import open
import time
from flask import Flask, render_template, request
import os

# определяем и используем абсолютный путь, потому что в консоле на винде
# относительный путь не "прокатывает", как в ноутбуке или в отладчике на Spyder
abs_path_todir = os.path.dirname(os.path.realpath(__file__))

path_to_data = 'data'

app = Flask(__name__)

print("Preparing classifier")
start_time = time.time()
classifier = MobilereviewClassifier()
print ("Classifier is ready")
print (time.time() - start_time, "seconds")

@app.route("/mobilereview-demo", methods=["POST", "GET"])
def index_page(text="", prediction_message=""):
    if request.method == "POST":
        text = request.form["text"]
        with open(os.path.join(abs_path_todir, path_to_data, 'mobilereview_demo_logs.txt'), "a", "utf-8") as logfile:
            text = request.form["text"]
            print(text)
            print("<response>", file=logfile)
            print("<date_time>" + time.strftime('[%d/%b/%Y %H:%M:%S]') + "</date_time>", file=logfile)
            print("<text>", file=logfile)
            print(text, file=logfile)
            print("</text>", file=logfile)
            prediction_message = classifier.get_prediction_message(text)
            print('ОЦЕНКА:', prediction_message)
            print("<prediction_message>" + prediction_message + "</prediction_message>", file=logfile)
            print("</response>", file=logfile)
            print('---------------------------------')
    return render_template('index.html', text=text, prediction_message=prediction_message)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)