import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model


def getPrediction(filename):
    # Load Models

    classification_model = load_model("model/BCC_CNN.model")
    unet_model = load_model("model/U-NetModel.h5")

    # Define variables
    CLASSES = ['Normal', 'Benign', 'Malignant']
    IMG_SIZE = 256
    filepath = 'static/images/' + filename

    # Prepare image for classification
    img = np.asarray(Image.open(filepath).resize((IMG_SIZE, IMG_SIZE)).convert("L"))
    img = np.expand_dims(img, axis=0)
    img = img/255.0

    prediction = classification_model.predict(img)
    predicted_class = CLASSES[np.argmax(prediction)]

    # Prepare image for segmentation
    img2 = np.asarray(Image.open(filepath).resize((IMG_SIZE, IMG_SIZE)))
    img2 = np.expand_dims(img2, axis=0)
    img2 = img2/255.0
    prediction_mask = unet_model.predict(img2)

    # Reshape images
    img2 = img2.reshape(256,256,3)
    prediction_mask = prediction_mask.reshape(256,256,1)
    return predicted_class, img2, prediction_mask