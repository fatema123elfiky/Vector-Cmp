import numpy as np
from PIL import Image

def lbg(vectors, numCodewords, epsilon = 0.01):
    codewords = [np.mean(vectors, axis=0)]

    # Split codewords until reach needed number of codewords
    while len(codewords) < numCodewords:
        newCodewords = []
        for cw in codewords:
            newCodewords.append(cw * (1 + epsilon))
            newCodewords.append(cw * (1 - epsilon))
        codewords = newCodewords

    prevDistortion = float('inf')

    while True:
        clusters = {}
        for i in range(len(codewords)):
            clusters[i] = []

        # Assign each vector to the best cluster
        for vector in vectors:
            mnDistance = float('inf')
            bestCluster = 0

            # Get the shortest distance
            for i, codeword in enumerate(codewords):
                distance = np.sum(np.abs(vector - codeword))
                if distance < mnDistance:
                    mnDistance = distance
                    bestCluster = i

            clusters[bestCluster].append(vector)

        # Update codewords as the mean of their clusters
        newCodewords = []
        totalDistortion = 0
        vectorsAssigned = 0
        currDistortion = float('inf')

        for i in range(len(codewords)):
            if len(clusters[i]) > 0:
                clusterVectors = np.array(clusters[i])
                newCodeword = np.mean(clusterVectors, axis=0)
                newCodewords.append(newCodeword)

                for vector in clusters[i]:
                    totalDistortion += np.sum(np.abs(vector - newCodeword))
                vectorsAssigned += len(clusters[i])

            else:
                newCodewords.append(codewords[i])

        if vectorsAssigned > 0:
            currDistortion = totalDistortion / vectorsAssigned

        if abs(prevDistortion - currDistortion) < epsilon * prevDistortion:
            break

        prevDistortion = currDistortion
        codewords = newCodewords

    return codewords

def compress():
    # Input data
    imgPath = input("Enter the image path:")
    img = Image.open(imgPath).convert("L")
    imgArray = np.array(img)
    print("Enter block dimensions")
    blockHeight = int(input("Block height:"))
    blockWidth = int(input("Block width:"))
    numCodewords = int(input("Enter number of blocks in the codebook:"))

    # Pad image with zeros if needed
    imgH, imgW = imgArray.shape
    padH = (blockHeight - imgH % blockHeight) % blockHeight
    padW = (blockWidth - imgW % blockWidth) % blockWidth
    paddedImg = np.pad(imgArray, ((0, padH), (0, padW)), mode='constant')

    # Split image to block vectors
    imgH, imgW = paddedImg.shape
    vectors = []
    for i in range(0, imgH, blockHeight):
        for j in range(0, imgW, blockWidth):
            block = paddedImg[i:i+blockHeight, j:j + blockWidth].flatten()
            vectors.append(block)

    vectors = np.array(vectors)

    codebook = lbg(vectors, numCodewords)

    # Assign each block to nearest codeword
    indices = []
    for vector in vectors:
        bestIndex = 0
        bestDistance = float('inf')

        for i, codeword in enumerate(codebook):
            distance = np.sum(np.abs(vector - codeword))
            if distance < bestDistance:
                bestDistance = distance
                bestIndex = i

        indices.append(bestIndex)

    indices = np.array(indices)
    np.save("codebook.npy", np.array(codebook))
    np.save("compressed_image.npy", indices)
    print("Codebook saved to codebook.npy")
    print("Compressed file saved to compressed_image.npy")

    # Calculate compression ratio
    originalSize = paddedImg.size  # pixels (bytes)
    bitsPerIndex = int(np.ceil(np.log2(numCodewords)))
    compressedSize = len(indices) * bitsPerIndex / 8

    compressionRatio = originalSize / compressedSize
    print("Original size = ", originalSize)
    print("Compressed size = ", compressedSize)
    print("Compression Ratio = ", compressionRatio)

    with open("meta_data.txt", "w") as f:
        f.write(f"{imgH} {imgW} {blockHeight} {blockWidth} {padH} {padW}\n")

def decompress():
    return None
