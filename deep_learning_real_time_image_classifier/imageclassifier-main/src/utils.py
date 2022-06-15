import logging
import os
from datetime import datetime
import cv2
import numpy as np


from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from pprint import pprint
from keras.models import load_model



def write_image(out, frame):
    """
    writes frame from the webcam as png file to disk. datetime is used as filename.
    """
    if not os.path.exists(out):
        os.makedirs(out)
    now = datetime.now() 
    dt_string = now.strftime("%H-%M-%S-%f") 
    filename = f'{out}/{dt_string}.png'
    logging.info(f'write image {filename}')
    cv2.imwrite(filename, frame)


def key_action():
    # https://www.ascii-code.com/
    k = cv2.waitKey(1)
    if k == 113: # q button
        return 'q'
    if k == 32: # space bar
        return 'space'
    if k == 112: # p key
        return 'p'
    return None


def init_cam(width, height):
    """
    setups and creates a connection to the webcam
    """

    logging.info('start web cam')
    cap = cv2.VideoCapture(0)

    # Check success
    if not cap.isOpened():
        raise ConnectionError("Could not open video device")
    
    # Set properties. Each returns === True on success (i.e. correct resolution)
    assert cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    assert cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    return cap


def add_text(text, frame):
    # Put some rectangular box on the image
    # cv2.putText()
    return NotImplementedError

def predict_frame(image):
    # reverse color channels
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #image = image.resize((224,224))
    
    # reshape image to (1, 224, 224, 3)
    #numpy_image = np.array(image)
    #image = np.expand_dims(numpy_image, axis=0)

    # apply pre-processing
    a = np.array(image)
    a = np.expand_dims(a, axis=0)
    a = preprocess_input(a)
    m = load_model('./models/mobilnet.h5')


    p = m.predict(a)
    l=decode_predictions(p)
    
    #vgg_model = load_model('./imageclassifier-main/models/vgg.h5')
    #processed_image = keras.applications.vgg16.preprocess_input(image)
    #prediction = vgg_model.predict(processed_image)
    #label_vgg = keras.applications.imagenet_utils.decode_predictions(prediction)
    #print(f'{label_vgg[0][0][1]} or {label_vgg[0][1][1]}')
    #logging.info(f'{label_vgg[0][0][1]} or {label_vgg[0][1][1]}')
  
    #return label_vgg[0][0][1], label_vgg[0][1][1]
    return l
 
