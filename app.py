from __future__ import division, print_function
# coding=utf-8
import face_recognition
import sys
import os
import glob
import re
import numpy as np
import re
import scipy.misc
import warnings
import face_recognition.api as face_recognition
import sys
import glob
import operator
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from skimage.measure import compare_ssim as ssim 
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)


def model_predict(img_path ):
    input_image = face_recognition.load_image_file(img_path)
    inp_encoding = face_recognition.face_encodings(input_image)[0]

    #Dict
    Di = {} 

    for f in glob.iglob("images/*"):
        image = face_recognition.load_image_file(f)
        encodings = face_recognition.face_encodings(image)[0]
        score = face_recognition.face_distance([encodings], inp_encoding)
        Di[f] = score[0]

    #to short dict.
    sorted(Di.items(), key=lambda x: x[1]) 
    #get first pair
    dict_pairs = Di.items()
    pairs_iterator = iter(dict_pairs)
    first_pair = next(pairs_iterator)
    #get first value of dict.
    values_view = Di.values()
    value_iterator = iter(values_view)
    first_value = next(value_iterator)

    

    return first_pair
 

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # finding match
        predict = model_predict(file_path) 
        return str("Image Score Value:" + str(predict) +"\n" +"The value of score lies between 0 to 1. " "\n" + "The Images with a smaller values(close to 0) are more similar to each other than ones with a larger values(close to 1)" )
    return None


if __name__ == '__main__':
    app.run(debug=True)

