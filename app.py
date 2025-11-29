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
decompressbtn = st.button("Decompress")

if compressbtn and file:
    tmp = "temp.png"
    img.save(tmp)
    ratio = comp.compress(tmp, bh, bw, cs)
    st.success(f"Compression Finished Ratio: {round(ratio,2)}")
    comp.decompress()
    if os.path.exists("decompressed.png"):
        st.image(Image.open("decompressed.png"), caption="Compressed", width=200)

if decompressbtn:
    if os.path.exists("decompressed.png"):
        comp.decompress()
        st.image(Image.open("decompressed.png"), caption="Decompressed", width=200)
        st.success("Decompression Finished")
    else:
        st.warning("No compressed image found. Please compress first")