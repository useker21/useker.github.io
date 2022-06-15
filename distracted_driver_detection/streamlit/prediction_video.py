# Importing all necessary libraries
import os
import re
import cv2
import shutil
import numpy as np
from matplotlib import pyplot as plt
import tensorflow as tf
from keras.models import load_model

import ffmpeg

import warnings
warnings.filterwarnings("ignore")

import tensorflow.keras as keras
from tensorflow.keras.preprocessing.image import load_img


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

###############################################

def prediction_video_cnn(video):

	try:
	
		# creating a folder named data
		if not os.path.exists('frame'):
			os.makedirs('frame')

	# if not created then raise error
	except OSError:
		print ('Error: Creating directory of data')
	
	cam = cv2.VideoCapture(video)

# frame
	currentframe = 0

	while(True):
	
		# reading from frame
		ret,frame = cam.read()

		if ret:
			# if video is still left continue creating images
			name = 'frame/' + str(currentframe) + '.jpg'
			print ('Creating...' + name)

			# writing the extracted images
			cv2.imwrite(name, frame)

			# increasing counter so that it will
			# show how many frames are created
			currentframe += 1
		else:
			break

	X = []
	base_path = './frame/'


	files = os.listdir(base_path)
	for file in files:
		# load the image
		img = load_img(base_path+'/'+file,target_size=(224, 224) )
    	# convert it to an array
		img_array = np.array(img)
        
    	# append the array to X
		X.append(img_array)

	X = np.array(X)

	X = X.astype('float32')/255

	ypred = model_cnn.predict(X)

	clean_image = []
	i = 0

	files = sorted(os.listdir('./frame'))
	for i in range(len(files)):
		img = cv2.imread('./frame/'+files[i])
		clean_image.append(img)
# labels is the image array

	i = 0
	situations_previous = ''
	cntr = 0
	
	for i in range(len(ypred)):
		predicted_class = 'c'+str(np.where(ypred[i] == np.amax(ypred[i]))[0][0])
		font = cv2.FONT_HERSHEY_SIMPLEX
		text = activities[predicted_class].upper()+':'+str(round(ypred[i].max()*100,0))+'%'
		if activities[predicted_class] != situations_previous:
			cntr = 0
		if activities[predicted_class] == 'Safe driving':
			cv2.putText(clean_image[i],text,(40,35), font, 0.8 ,(0,256,0),2)
		else:
			if cntr >= 0:
				cv2.putText(clean_image[i],text,(40,35), font, 0.8 ,(0,0,256),2)
			else:
				text = str(cntr+1)
				cntr = cntr+1
				cv2.putText(clean_image[i],text,(40,35), font, 0.8 ,(0,0,256),2)

		situations_previous = activities[predicted_class]
	fourcc = cv2.VideoWriter_fourcc(*'X264')
	new_video = cv2.VideoWriter('New_cnn.mp4',fourcc, 3, (640,480))
 
	for i in range(len(clean_image)):
		new_video.write(clean_image[i])
	new_video.release()
	
	shutil.rmtree('./frame')

	return new_video

def prediction_video_mobile(video):

	try:
	
		# creating a folder named data
		if not os.path.exists('frame'):
			os.makedirs('frame')

	# if not created then raise error
	except OSError:
		print ('Error: Creating directory of data')
	
	cam = cv2.VideoCapture(video)

# frame
	currentframe = 0

	while(True):
	
		# reading from frame
		ret,frame = cam.read()

		if ret:
			# if video is still left continue creating images
			name = 'frame/' + str(currentframe) + '.jpg'
			print ('Creating...' + name)

			# writing the extracted images
			cv2.imwrite(name, frame)

			# increasing counter so that it will
			# show how many frames are created
			currentframe += 1
		else:
			break

	X = []
	base_path = './frame/'


	files = os.listdir(base_path)
	for file in files:
		# load the image
		img = load_img(base_path+'/'+file,target_size=(224, 224) )
    	# convert it to an array
		img_array = np.array(img)
        
    	# append the array to X
		X.append(img_array)

	X = np.array(X)

	X = X.astype('float32')/255

	ypred = model_mobile.predict(X)

	clean_image = []
	i = 0

	files = sorted(os.listdir('./frame'))
	for i in range(len(files)):
		img = cv2.imread('./frame/'+files[i])
		clean_image.append(img)
# labels is the image array

	i = 0
	situations_previous = ''
	cntr = 0
	
	for i in range(len(ypred)):
		predicted_class = 'c'+str(np.where(ypred[i] == np.amax(ypred[i]))[0][0])
		font = cv2.FONT_HERSHEY_SIMPLEX
		text = activities[predicted_class].upper()+':'+str(round(ypred[i].max()*100,0))+'%'
		if activities[predicted_class] != situations_previous:
			cntr = 0
		if activities[predicted_class] == 'Safe driving':
			cv2.putText(clean_image[i],text,(40,35), font, 0.8 ,(0,256,0),2)
		else:
			if cntr >= 0:
				cv2.putText(clean_image[i],text,(40,35), font, 0.8 ,(0,0,256),2)
			else:
				text = str(cntr+1)
				cntr = cntr+1
				cv2.putText(clean_image[i],text,(40,35), font, 0.8 ,(0,0,256),2)

		situations_previous = activities[predicted_class]

	fourcc = cv2.VideoWriter_fourcc(*'X264')
	new_video = cv2.VideoWriter('New_mobile.mp4',fourcc, 3, (640,480))
	
 
	for i in range(len(clean_image)):
		new_video.write(clean_image[i])
	new_video.release()
	
	
	shutil.rmtree('./frame')

	return new_video

###############################################

def prediction_video_vgg(video):

	try:
	
		# creating a folder named data
		if not os.path.exists('frame'):
			os.makedirs('frame')

	# if not created then raise error
	except OSError:
		print ('Error: Creating directory of data')
	
	cam = cv2.VideoCapture(video)

# frame
	currentframe = 0

	while(True):
	
		# reading from frame
		ret,frame = cam.read()

		if ret:
			# if video is still left continue creating images
			name = 'frame/' + str(currentframe) + '.jpg'
			print ('Creating...' + name)

			# writing the extracted images
			cv2.imwrite(name, frame)

			# increasing counter so that it will
			# show how many frames are created
			currentframe += 1
		else:
			break

	X = []
	base_path = './frame/'


	files = os.listdir(base_path)
	for file in files:
		# load the image
		img = load_img(base_path+'/'+file,target_size=(224, 224) )
    	# convert it to an array
		img_array = np.array(img)
        
    	# append the array to X
		X.append(img_array)

	X = np.array(X)

	X = X.astype('float32')/255

	ypred = model_vgg.predict(X)

	clean_image = []
	i = 0

	files = sorted(os.listdir('./frame'))
	for i in range(len(files)):
		img = cv2.imread('./frame/'+files[i])
		clean_image.append(img)
# labels is the image array

	i = 0
	situations_previous = ''
	cntr = 0
	
	for i in range(len(ypred)):
		predicted_class = 'c'+str(np.where(ypred[i] == np.amax(ypred[i]))[0][0])
		font = cv2.FONT_HERSHEY_SIMPLEX
		text = activities[predicted_class].upper()+':'+str(round(ypred[i].max()*100,0))+'%'
		if activities[predicted_class] != situations_previous:
			cntr = 0
		if activities[predicted_class] == 'Safe driving':
			cv2.putText(clean_image[i],text,(40,35), font, 0.8 ,(0,256,0),2)
		else:
			if cntr >= 0:
				cv2.putText(clean_image[i],text,(40,35), font, 0.8 ,(0,0,256),2)
			else:
				text = str(cntr+1)
				cntr = cntr+1
				cv2.putText(clean_image[i],text,(40,35), font, 0.8 ,(0,0,256),2)

		situations_previous = activities[predicted_class]

	fourcc = cv2.VideoWriter_fourcc(*'X264')
	new_video = cv2.VideoWriter('New_vgg.mp4',fourcc, 3, (640,480))
	
 
	for i in range(len(clean_image)):
		new_video.write(clean_image[i])
	new_video.release()
	
	
	shutil.rmtree('./frame')

	return new_video

if __name__=='__main__':
    pass
