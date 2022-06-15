
### Import libraries

import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time
import numpy as np

from PIL import Image
from prediction_image import prediction_cnn, prediction_mobile, prediction_vgg
from prediction_video import prediction_video_cnn, prediction_video_mobile, prediction_video_vgg
import cv2


from keras.preprocessing.image import load_img
from keras.models import load_model


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

#logo
st.sidebar.image(image="driver_2.png") 

#sidebar index
with st.sidebar:
    st.header('Deep Learning for Image Classification')
    
#define a radio button in the sidebar

with st.sidebar:
    
    add_radio = st.radio('',       
        ('Introduction', 'Data Visualization', 'Compare Models','Examine Models', 'Image Classifier', 'Video Classifier', 'Conclusion')
    )




#######################################################
if add_radio == 'Introduction':

    st.header('distracted-driver-detection-using-deep-learning')
    st.write('Driving a :car: is a complex task, and it requires :exclamation: complete attention :exclamation:') 
    st.write('Distracted driving is any activity that takes away the driver’s attention from the road.')
    st.write('**Several studies have identified three main types of distraction:**')
    st.write(':eye: _visual distractions (driver’s eyes off the road)_')
    st.write(':hand: _manual distractions (driver’s hands off the wheel)_')
    st.write(':exploding_head: _cognitive distractions (driver’s mind off the driving task)_')
    
    st.subheader('dataset')
    st.markdown("""The State Farm Distracted Driver dataset was used and taken from [Kaggle]( https://www.kaggle.com/c/state-farm-distracted-driver-detection/data)
    """)
    st.write('It contained snapshots from a video captured by a camera mounted in the car.')
    st.write('The dataset has ~22.4 K labeled samples with equal distribution among the classes.')
    st.write('**There are 10 classes (activities) of images:**')
    with st.expander('activities of images'):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.image('./driver_selected/safe_driving.jpg', caption='safe driving')
        with col2:
            st.image('./driver_selected/texting_right.jpg', caption='texting on the phone - right hand')

        with col3:
            st.image('./driver_selected/talking_right.jpg', caption='talking on the phone - right hand')   
     
    
        col4, col5, col6 = st.columns(3)

        with col4:
            st.image('./driver_selected/texting_left.jpg', caption='texting on the phone - left hand')

        with col5:
            st.image('./driver_selected/talking_left.jpg', caption='talking on the phone - left hand')

        with col6:
            st.image('./driver_selected/operating_radio.jpg', caption='operating the radio')   
    
        col7, col8, col9 = st.columns(3)

        with col7:
            st.image('./driver_selected/drinking.jpg', caption='drinking something')

        with col8:
            st.image('./driver_selected/reaching_behind.jpg', caption='reaching behind')

        with col9:
            st.image('./driver_selected/hair_makeup.jpg', caption='hair and make up')

        col10, col11, col12 = st.columns(3)

        with col10:
            st.image('./driver_selected/talking_passenger.jpg', caption='talking to the passenger')

        with col11:
            st.write('')

        with col12:
            st.write('')

    st.write('---')
    st.write(':x: Any of these above distractions can endanger you, your passengers, and others on the road.')
    st.image('crash.png')
    st.write('---')
    st.write(':calling: Texting is the most dangerous and alarming distraction on the road.')
    with st.expander('video'):
        st.video('https://www.youtube.com/watch?v=LjIEEp856Lw&list=PPSV')
    st.image('texting.png')
    st.write('---')
    st.write(' The project goal :dart: is to predict the likelihood of what the driver is doing in each picture.')
    st.write('The algorithm automatically detects the distracted activity of the drivers and :email: alerts them.')


#######################################################

if add_radio == 'Data Visualization':
    st.header('Here comes some data visualization')
       

    with st.expander('Images by driver activities'):
        st.write("""
         The chart below shows number of images regarding the driver activities in the car.
         There are 10 activities.
         """)
     
        df = pd.read_csv('driver_imgs_list.csv')
        df.replace({'classname': activities},inplace=True)    
        st.subheader('Number of images by driver activities')
        fig = px.histogram(df, x='classname', color='classname')
        st.plotly_chart(fig)

    st.write("---")

    with st.expander('Images by driver ids'):
        st.write("""
         The chart below shows number of images by driver ids.
         There are 26 drivers.
         """)
        drivers_id = pd.DataFrame((df['subject'].value_counts()).reset_index())
        drivers_id.columns = ['driver_id', 'Counts']
        st.subheader('Number of images by driver ids')
        fig = px.histogram(drivers_id, x="driver_id",y="Counts" ,color="driver_id")
        st.plotly_chart(fig)

####################################################### 
if add_radio == 'Compare Models':
    st.header(add_radio)
    st.write('In this study, the convolution-neural-network (CNN) technique, MobileNetv2 and VGG16 as a pre-trained model were applied to learn the machine and further classify the real image.')
    df = pd.read_csv('compare_models_sum.csv', index_col=0, )
    
    def format_color_groups(df):
        colors = ['gold', 'lightblue']
        x = df.copy()
        factors = list(x['optimizer'].unique())
        i = 0
        for factor in factors:
            style = f'background-color: {colors[i]}'
            x.loc[x['optimizer'] == factor, :] = style
            i = not i
        return x

    df = df.style.apply(format_color_groups, axis=None )
    st.dataframe(df)

#######################################################       

if add_radio == 'Examine Models':
    st.header(add_radio)
    
    option = st.selectbox('Select the prediction model to have a look at performance parameters.',
     ('','CNN', 'Mobilenetv2', 'VGG16'))

    if option=='':
        st.write(option)
    else:
        st.write(option, 'is selected.')

    if option == 'CNN':
        df_cnn = pd.read_csv('history_cnn_scalling_full.csv', index_col=0)
        st.markdown('**_Training Loss vs. Validation Loss_**')
        st.line_chart(df_cnn[['loss', 'val_loss']][:10])
        st.dataframe(df_cnn[['loss', 'val_loss']][:10])
        st.write('---')
        st.markdown('**_Training Accuracy vs. Validation Accuracy_**')
        st.line_chart(df_cnn[['accuracy', 'val_accuracy']][:10])
        st.dataframe(df_cnn[['accuracy', 'val_accuracy']][:10])
        st.write('---')
        st.markdown('**_Confusion Matrix_**')
        col1,col2 = st.columns([1,4])
        with col1:
            st.image('classes.png')
        with col2:
            st.image('cnn_con_matrix.png')
    
    if option == 'Mobilenetv2':
        df_mobilnet = pd.read_csv('history_mobilnet_sample.csv', index_col=0)
        st.markdown('**_Training Loss vs. Validation Loss_**')
        st.line_chart(df_mobilnet[['loss', 'val_loss']][:10])
        st.dataframe(df_mobilnet[['loss', 'val_loss']][:10])
        st.write('---')
        st.markdown('**_Training Accuracy vs. Validation Accuracy_**')
        st.line_chart(df_mobilnet[['accuracy', 'val_accuracy']][:10])
        st.dataframe(df_mobilnet[['accuracy', 'val_accuracy']][:10])
        st.write('---')
        st.markdown('**_Confusion Matrix_**')
        col1,col2 = st.columns([1,4])
        with col1:
            st.image('classes.png')
        with col2:
            st.image('mobile_con_matrix.png')

    if option == 'VGG16':
        df_vgg = pd.read_csv('history_vgg_sample.csv', index_col=0)
        st.markdown('**_Training Loss vs. Validation Loss_**')
        st.line_chart(df_vgg[['loss', 'val_loss']][:10])
        st.dataframe(df_vgg[['loss', 'val_loss']][:10])
        st.write('---')
        st.markdown('**_Training Accuracy vs. Validation Accuracy_**')
        st.line_chart(df_vgg[['accuracy', 'val_accuracy']][:10])
        st.dataframe(df_vgg[['accuracy', 'val_accuracy']][:10])
        st.write('---')
        st.markdown('**_Confusion Matrix_**')
        col1,col2 = st.columns([1,4])
        with col1:
            st.image('classes.png')
        with col2:
            st.image('vgg16_con_matrix.png')
    

#######################################################

if add_radio=='Image Classifier':
    st.title(add_radio)
    st.markdown('Upload an image, choose a model and then press **_Classify_** to see the prediction of driver activities')
    
    uploaded_files = st.file_uploader("Choose an image", accept_multiple_files=False, type=["png","jpg","jpeg"])
    cnn = st.checkbox('CNN')
    mobilenetv2 = st.checkbox('MobileNetv2')
    vgg16 = st.checkbox('VGG16')

    class_btn = st.button("Classify")

    if uploaded_files is not None:
        image = Image.open(uploaded_files)
        width = 224
        height = 224
        width, height = image.size
        st.image(image, use_column_width=True)

    if class_btn:
        if uploaded_files is None:
            st.write("Please upload a valid image")
        else:
            if cnn:
                with st.spinner('Classifying...'):
                    plt.imshow(image)
                    plt.axis("off")
                    prediction = prediction_cnn(image)
                    time.sleep(1)
                    st.success('Classified by CNN')
                    st.write(prediction)
                    


            if mobilenetv2:
                with st.spinner('Classifying...'):
                    plt.imshow(image)
                    plt.axis("off")
                    prediction = prediction_mobile(image)
                    time.sleep(1)
                    st.success('Classified by MobileNetV2')
                    st.write(prediction)

            if vgg16:
                with st.spinner('Classifying...'):
                    plt.imshow(image)
                    plt.axis("off")
                    prediction = prediction_vgg(image)
                    time.sleep(1)
                    st.success('Classified by VGG16')
                    st.write(prediction)
              
#######################################################                
if add_radio == 'Video Classifier':
    st.title(add_radio) 
    st.markdown('Upload a video, choose a model, and then press **_Classify_** to see the prediction of driver activities as a video')
   
    video_uploaded = st.file_uploader('Choose a video', accept_multiple_files=False, type = 'mp4')
    cnn_v = st.checkbox('CNN')
    mobilenetv2_v = st.checkbox('MobileNetv2')
    vgg16_v = st.checkbox('VGG16') 

    class_btn = st.button("Classify")
   

    if video_uploaded is not None:
        with open(os.path.join('temp','temp_video.mp4'),"wb") as f:
            f.write((video_uploaded).getbuffer())

        video_bytes = video_uploaded.read()
        st.video(video_bytes)
       
   
    if class_btn:
        if video_uploaded is None:
            st.write("Please upload a valid video")
        else:
            if cnn_v:
                with st.spinner('Classifying...'):
                    prediction = prediction_video_cnn('temp/temp_video.mp4')
                    time.sleep(1)
                    st.success('Classified by CNN')
                    st.video('New_cnn.mp4')
            if mobilenetv2_v:
                with st.spinner('Classifying...'):
                    prediction = prediction_video_mobile('temp/temp_video.mp4')
                    time.sleep(1)
                    st.success('Classified by MobileNetV2')
                    st.video('New_mobile.mp4')
            if vgg16_v:
                with st.spinner('Classifying...'):
                    prediction = prediction_video_vgg('temp/temp_video.mp4')
                    time.sleep(1)
                    st.success('Classified by VGG16')
                    st.video('New_vgg.mp4')
                
        
if add_radio == 'Conclusion':
    st.header(add_radio)
    with st.expander('wishes'):
        st.write(':cinema: We can envision this type of product being embedded in cars to prevent accidents due to distracted driving.')
        st.write(':cityscape: This technology also could be applied in smart cities.')
        st.write(':male-detective: Driver distractions coluld be detected automatically and then send a warning message to the driver.')
    with st.expander('libraries'):
        col1,col2, col3 =st.columns(3)
        with col1:
            st.image('python.png')
            st.image('pandas.png')
            
        with col2:
            st.image('tensorflow.png')
            st.image('opencv.png')
            st.image('numpy.png')
            
        with col3:
            st.image('streamlit.png')
            st.image('plotty.png')

    with st.expander('thanks'):
        st.write(':+1: bootcamp was enjoyable and productive.')
        st.write(':clap: thank you for your support and smiles.')
        st.write(':open_hands:see you in another place and at different times.')
        st.write(':gift_heart: you are all so precious.')
            
#############################################



   




 


