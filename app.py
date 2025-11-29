import streamlit as st
from PIL import Image
import numpy as np
import VectorQuantization as comp
import os

st.set_page_config(page_title="Image Compressor", layout="centered")
st.title("Image Compression")

file = st.file_uploader("Upload image", type=["png","jpg","bmp"])

if file:
    img = Image.open(file).convert("L")
    st.image(img, caption="Original", width=200)

bh = st.number_input("Block Height", min_value=1, value=4, step=1)
bw = st.number_input("Block Width", min_value=1, value=4, step=1)
cs = st.number_input("Codebook Size", min_value=2, value=16, step=1)

compressbtn = st.button("Compress")

cmp_img = st.file_uploader("Upload compressed image", type=["npy"])
codebook = st.file_uploader("Upload codebook ", type=["npy"])
meta_data = st.file_uploader("Upload meta data ", type=["txt"])
decompressbtn = st.button("Decompress")

if compressbtn and file:

    ratio = comp.compress(file, bh, bw, cs)
    st.success(f"Compressed Successfully !! \n")
    st.success(

        f"Original size : {ratio[0]}  \n"
        f"Compressed size : {ratio[1]}  \n"
        f"Compression Ratio : {ratio[2]}"
    )

if decompressbtn and codebook and cmp_img and meta_data:

    comp.decompress(codebook, cmp_img, meta_data)
    st.image(Image.open("C:\\Users\Fatma\PycharmProjects\DataCompression\VecCmp\images\decompressed_image.png"), caption="Decompressed", width=200)
    st.success("Decompression Finished !!")

    #if os.path.exists("decompressed.png"):
     #   comp.decompress()

    #else:
        #st.warning("No compressed image found. Please compress first")