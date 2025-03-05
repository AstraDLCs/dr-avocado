from flask import Flask, request, render_template, jsonify
import numpy as np
from PIL import Image
import tensorflow as tf
import json

app = Flask(__name__)

# Variable global para almacenar el modelo actual
current_model_name = "dr_palta_v5"

def load_model(model_name):
    interpreter = tf.lite.Interpreter(model_path=f'./models/{model_name}.tflite')
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    with open(f'./models/{model_name}_class_names.json', 'r') as f:
        class_names = json.load(f)
    return interpreter, input_details, output_details, class_names

# Cargar el modelo inicial
interpreter, input_details, output_details, class_names = load_model(current_model_name)

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

@app.route('/model', methods=['POST'])
def model():
    global current_model_name
    modelo = request.form.get('modelo')
    
    if modelo == 'multiclasificacion':
        current_model_name = "dr_palta_v5"
        respuesta = "Modelo de Multiclasificación."
    elif modelo == 'binaria':
        current_model_name = "dr_palta_B_V1"
        respuesta = "Modelo de Clasificación binaria."
    else:
        respuesta = "Opción no válida."

    global interpreter, input_details, output_details, class_names
    interpreter, input_details, output_details, class_names = load_model(current_model_name)

    return render_template('index.html', respuesta=respuesta)

if __name__ == '__main__':
    app.run(debug=True)
