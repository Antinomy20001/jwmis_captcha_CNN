from flask import Flask, request, jsonify
import base64
import tensorflow as tf
import numpy as np
import keras
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import io
import os
from PIL import Image
from handle_image import handle

app = Flask(__name__)


CHARS = {'4': 2, '5': 3, 'D': 11, 'B': 9, 'R': 22, 'F': 13, '9': 7, 'A': 8, '3': 1, 'V': 26, 'U': 25, '6': 4, 'J': 16, 'T': 24, 'X': 28,
         'M': 18, '2': 0, 'Y': 29, 'H': 15, 'G': 14, 'C': 10, '7': 5, 'Q': 21, 'N': 19, '8': 6, 'W': 27, 'S': 23, 'K': 17, 'E': 12, 'P': 20, 'Z': 30}

index = [0] * 31
for k, v in CHARS.items():
    index[v] = k


img_rows, img_cols = 30, 54


def init():
    path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'first_try.h5')
    model = load_model(path)
    graph = tf.get_default_graph()
    return model, graph


def get(model, path):
    image = load_img(path, grayscale=True, target_size=(img_rows, img_cols))
    image = img_to_array(image)
    image = np.resize(image, (1, img_rows, img_cols, 1))
    image /= 255
    y_prob = model.predict(image)
    y_classes = y_prob.argmax(axis=-1)
    return index[y_classes[0]]


def handle_image(path):
    pic = io.BytesIO(path)
    pic = handle(pic)
    result = ''

    model, graph = init()
    with graph.as_default():
        for i in pic:
            bitio = io.BytesIO()
            i.save(bitio, 'png')
            bitio.seek(0)
            result += get(model, bitio)
    return result


@app.route('/', methods=['POST'])
def checkcode_detect():
    try:
        content = base64.b64decode(request.values.get('image', None))
        return jsonify(status='yes', result=handle_image(content))
    except:
        return jsonify(status='no', result=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2333, debug=True)
