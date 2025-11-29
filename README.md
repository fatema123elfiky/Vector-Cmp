# Vector Quantization Image Compressor
A simple Streamlit-based application that compresses and decompresses grayscale images using Vector Quantization (LBG Algorithm).
Vector Quantization (VQ) is a lossy image compression technique that reduces the size of an image by replacing groups of pixels (called blocks or vectors) with representative patterns known as codewords.

Instead of storing every pixel in the image, VQ stores:
- A codebook → a small set of representative blocks
- Indices → each image block is replaced by the index of its closest codeword

The app allows the user to upload an image, define block size and codebook size, compress the image, then decompress it again using saved metadata.

1. Clone the repository

2. Install dependencies

3. Run Project
```bash
streamlit run app.py
```
