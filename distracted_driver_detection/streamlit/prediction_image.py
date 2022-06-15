
import tensorflow as tf
from keras.models import load_model
import numpy as np

                          

model_cnn = load_model('model_cnn_sgd_scaling_full.h5')
model_mobile = load_model('model_mobilnet_v2.h5')
model_vgg = load_model('model_vgg16.h5')

classes = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']
activities = {
                'c0': 'Safe driving', 
                'c1': 'Texting on the phone - right hand', 
                'c2': 'Talking on the phone - right hand', 
                'c3': 'Texting on the phone - left hand', 
                'c4': 'Talking on the phone - left hand', 
                'c5': 'Operating the radio', 
                'c6': 'Drinking', 
                'c7': 'Reaching behind', 
                'c8': 'Hair and makeup', 
                'c9': 'Talking to passenger'
             }


def prediction_cnn(img):
     
    img = img.resize((224,224))
    img = np.array(img)
    img = img.astype('float32')/255
    img = np.expand_dims(img, axis=0)

    prediction_cnn = model_cnn.predict(img)
    scores = tf.nn.softmax(prediction_cnn[0])
    scores = scores.numpy()
    result = f"The activity of driver =>> {activities[classes[np.argmax(prediction_cnn)]]} =>> { (100 * np.max(prediction_cnn)).round(2) } % confidence."
    

    return result

def prediction_mobile(img):
    img = img.resize((224,224))
    img = np.array(img)
    img = img.astype('float32')/255
    img = np.expand_dims(img, axis=0)

    prediction_mobile = model_mobile.predict(img)
    scores = tf.nn.softmax(prediction_mobile[0])
    scores = scores.numpy()
    result = f"The activity of driver =>> {activities[classes[np.argmax(prediction_mobile)]]} =>> { (100 * np.max(prediction_mobile)).round(2) } % confidence."
    
    return result

def prediction_vgg(img):
    img = img.resize((224,224))
    img = np.array(img)
    img = img.astype('float32')/255
    img = np.expand_dims(img, axis=0)

    prediction_vgg = model_vgg.predict(img)
    scores = tf.nn.softmax(prediction_vgg[0])
    scores = scores.numpy()
    result = f"The activity of driver =>> {activities[classes[np.argmax(prediction_vgg)]]} =>> { (100 * np.max(prediction_vgg)).round(2) } % confidence."
    
    return result

if __name__=='__main__':
    pass

