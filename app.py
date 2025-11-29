import streamlit as st
from PIL import Image
import numpy as np
import VectorQuantization as comp
import os

st.set_page_config(page_title="Image Compressor", layout="centered")
st.title(" * Compressor * ")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #89CFF0 ;
    }
   
    .main {
        background-color:#89CFF0;
    }
    .body{
    background-color:#89CFF0;
    }

    
    h1 {
        color: #000000 !important;
        text-align: center;
        font-weight: 800;
    }

    
    .stButton>button {
        background-color: #3f72af;
        color: white;
        border-radius: 8px;
        padding: 10px 18px;
        font-size: 16px;
        transition: 0.3s;
    }

    
    .stButton>button:hover {
        background-color: #112d4e;
        transform: scale(1.05);
    }

    
    .stFileUploader {
        border: 2px dashed #3f72af;
        border-radius: 10px;
        padding: 15px;
        background-color: #ffffffdd;
    }

    .stFileUploader:hover {
        border-color: #112d4e;
    }

    
    .stNumberInput>div>div>input {
        border-radius: 6px;
        border: 1px solid #3f72af;
    }

    
    .stSuccess {
        background-color: #d4edda !important;
        border-left: 5px solid #28a745 !important;
    }

    
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .block-container {
    max-width: 60% !important;
    padding: 10rem 8rem !important;
    
    border-radius: 12px;
    
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.subheader("Upload & Compress")

file = st.file_uploader("Upload image", type=["png","jpg","bmp"])

if file:
    img = Image.open(file).convert("L")
    st.image(img, caption="Original", width=200)

bh = st.number_input("Block Height", min_value=1, value=4, step=1)
bw = st.number_input("Block Width", min_value=1, value=4, step=1)
cs = st.number_input("Codebook Size", min_value=2, value=16, step=1)

compressbtn = st.button("Compress")
if compressbtn and file:
    ratio = comp.compress(file, bh, bw, cs)
    st.success(f"Compressed Successfully !! \n")
    st.success(

        f"Original size : {ratio[0]}  \n"
        f"Compressed size : {ratio[1]}  \n"
        f"Compression Ratio : {ratio[2]}"
    )



st.subheader("Decompress")

cmp_img = st.file_uploader("Upload compressed image", type=["npy"])
codebook = st.file_uploader("Upload codebook ", type=["npy"])
meta_data = st.file_uploader("Upload meta data ", type=["txt"])
decompressbtn = st.button("Decompress")


if decompressbtn and codebook and cmp_img and meta_data:

    comp.decompress(codebook, cmp_img, meta_data)
    st.image(Image.open("C:\\Users\Fatma\PycharmProjects\DataCompression\VecCmp\images\decompressed_image.png"), caption="Decompressed", width=200)
    st.success("Decompression Finished !!")

