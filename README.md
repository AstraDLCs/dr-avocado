### Proyecto Dr-Avocado (Detección de Enfermedades en Palta utilizando Redes NeuronalesConvolucionales)

#### Introducción

El Proyecto Dr-Avocado esta diseñado específicamente para detectar enfermedades y patógenos, con un enfoque principal en la cercospora purpurea, que afecta las hojas de palta.
Esta Red Neuronal Convolucional (CNN) se creará para contribuir a la agricultura, permitiendo una diagnosis temprana y precisa que sea crucial para la producción sostenible y segura del consumidor final.

#### Instalación

Para ejecutar Dr-Avocado en tu entorno de desarrollo local con Python 3.x en Windows, sigue los pasos a
continuación:

1. **Instalar las Dependencias**
   Primero necesitas instalar todas las bibliotecas requeridas para que el proyecto funcione correctamente. Para
hacer esto, utiliza el siguiente comando que te llevará a través del proceso de instalación rápido y eficiente:

    ```bash
    pip install -r requirements.txt
    ```

   Asegúrate de tener Pip previamente instalado en tu sistema. Si no lo tienes, puedes descargarlo
[aquí](https://pip.pypa.io/en/stable/).

2. **Configurar el Entorno de Ejecución**
   Una vez que hayas instalado las dependencias necesarias, inicies tu entorno de ejecución utilizando los
siguientes comandos:

    ```bash
    flask run --host=0.0.0.0 --port=5000
    ```

   Esto configurará el entorno para que Dr-Avocado esté disponible en cualquier dispositivo conectado a tu red
local (usando la dirección IP 0.0.0.0) y escuchará en el puerto 5000, lo cual te permite acceder fácilmente desde
navegadores web o interacciones similares.

#### Configuración Preliminar

Antes de comenzar con las pruebas y ajustes del modelo, es importante tener los siguientes elementos configurados:

- Python instalado en tu sistema y Pip funcionando correctamente.
- (Opcional-recomendado) Un entorno virtual para el proyecto (si no tienes uno ya creado, puedes hacerlo ejecutando `python -m venv
avocadoenv`).