# Vector Quantization Compression Technique
Vector Quantization (VQ) is a lossy image compression technique that reduces the size of an image by replacing groups of pixels (called blocks or vectors) with representative patterns known as codewords.

Instead of storing every pixel in the image, VQ stores:
- A codebook → a small set of representative blocks
- Indices → each image block is replaced by the index of its closest codeword

This significantly reduces storage requirements.
