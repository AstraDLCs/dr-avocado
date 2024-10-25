from flask import Flask, request, render_template, jsonify
import numpy as np
from PIL import Image
import tensorflow as tf
import cv2
from io import BytesIO
import json
import base64

app = Flask(__name__)

interpreter = tf.lite.Interpreter(model_path='./models/dr_palta_tfv3.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


with open('./models/dr_palta_fv1_class_names.json', 'r') as f:
    class_names = json.load(f)


def preprocess_image(image):

    img = image.convert('RGB')

    img = img.resize((224, 224))
    img = np.array(img).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def categorize(image):

    img = preprocess_image(image)
    
    interpreter.set_tensor(input_details[0]['index'], img)
    
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    indice_clase = np.argmax(output_data[0], axis=-1)
    
    print("Salida del modelo:", output_data)
    print("Índice de clase predicho:", indice_clase)
    print(class_names[indice_clase])

    return class_names[indice_clase]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'La imagen no se ha podido subir'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se ha seleccionado ninguna imagen'}), 400
    
    image = Image.open(file.stream)
    class_name = categorize(image)
    
    return jsonify({'class_name': class_name})


@app.route('/camera', methods=['POST'])
def camera():

    data = request.json.get('image')
    if not data:
        return jsonify({'error': 'No hay datos en la imagen'}), 400
    
    image_bytes = BytesIO(base64.b64decode(data.split(',')[1]))
    image = Image.open(image_bytes)
    
    class_name = categorize(image)
    
    return jsonify({'class_name': class_name})


if __name__ == '__main__':
    app.run(debug=True)
