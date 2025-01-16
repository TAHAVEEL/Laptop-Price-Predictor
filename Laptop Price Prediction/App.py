import streamlit as st
import pickle
import numpy as np
import warnings
import os
import base64
from PIL import Image
warnings.filterwarnings('ignore')

image_paths = [
r"C:\Users\mssuh\OneDrive\Pictures\Laptop project\MACBOOK.webp",
r"C:\Users\mssuh\OneDrive\Pictures\Laptop project\ASUS.jpg",
r"C:\Users\mssuh\OneDrive\Pictures\Laptop project\ACER.jpg"

]
page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"]
    {
        background-image:url('https://img.freepik.com/premium-photo/cyber-security-background-hd-8k-wallpaper-background-stock-photographic-image_915071-48024.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
     .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 200%;
        background-color: rgba(0, 0, 0, 0.5); 
        z-index: -1;
    }

     </style>
    """
st.markdown(page_bg_img,unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .image-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .image-container img {
        height: 200px;
        border-radius: 10px;
        box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.5);
        transition: transform 0.2s;
    }
    .image-container img:hover {
        transform: scale(1.09);
    }

     h1,h2,h3,h4,h5,h6 .stText, .stButton, .stSelectbox {
        font-family: cursive;
        color: #000000; }
    </style>
    """,
    unsafe_allow_html=True,
)


def encode_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return None


image_html = '<div class="image-container">'
for image_path in image_paths:
    encoded_image = encode_image(image_path)
    if encoded_image:
        image_html += f'<img src="data:image/jpeg;base64,{encoded_image}" alt="Image">'
    else:
        image_html += '<p>Image not found</p>'
image_html += '</div>'
st.markdown(image_html, unsafe_allow_html=True)


pipe = pickle.load(open('pipeline.pkl','rb'))
df = pickle.load(open('df1.pkl','rb'))

st.markdown("<h1 style='color:white;'>Laptop Price Predictor</h1>", unsafe_allow_html=True)

company = st.selectbox('Brand',df['Company'].unique())

type = st.selectbox('Type',df['TypeName'].unique())

ram = st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])

weight = st.number_input('Weight of the Laptop')

touchscreen = st.selectbox('Touchscreen',['No','Yes'])

ips = st.selectbox('IPS',['Yes','No'])

screen_size = st.slider('Scrensize in inches', 10.0, 18.0, 13.0)

resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

cpu = st.selectbox('CPU',df['Cpu brand'].unique())

hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])

ssd = st.selectbox('SSD(in GB)',[0,8,128,256,512,1024])

gpu = st.selectbox('GPU',df['Gpu brand'].unique())

os = st.selectbox('OS',df['os'].unique())

if st.button('Predict Price'):

    ppi = None
    if touchscreen == 'Yes':
        touchscreen = 1
    else:
        touchscreen = 0

    if ips == 'Yes':
        ips = 1
    else:
        ips = 0

    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])

    ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size

    query = np.array([company,type,ram,weight,touchscreen,ips,ppi,cpu,hdd,ssd,gpu,os])

    query = query.reshape(1,12)
    st.title("Laptop Predicted Price :  ₹ " + str(int(np.exp(pipe.predict(query)[0]))))