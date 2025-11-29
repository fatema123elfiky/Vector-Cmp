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

        # Assign each vector to    best cluster
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

def compress(image,bh ,bw,cs):
    # Input data
    #imgPath = input("Enter the image path:")
    img = Image.open(image).convert("L")
    imgArray = np.array(img)
    #print("Enter block dimensions")
    blockHeight = int(bh)
    blockWidth = int(bw)
    numCodewords = int(cs)

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
    np.save("C:\\Users\Fatma\PycharmProjects\DataCompression\VecCmp\data\codebook.npy", np.array(codebook))
    np.save("C:\\Users\Fatma\PycharmProjects\DataCompression\VecCmp\data\compressed_image.npy", indices)
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

    with open("C:\\Users\Fatma\PycharmProjects\DataCompression\VecCmp\data\meta_data.txt", "w") as f:
        f.write(f"{imgH} {imgW} {blockHeight} {blockWidth} {padH} {padW}\n")

    return [originalSize, compressedSize, compressionRatio]
def decompress(codebookPath ,compressedImagePath , metadataPath):

    #codebookPath = input("Enter the codebook path: ")
    codebook = np.load(codebookPath)
    #compressedImagePath = input("Enter the compressed image path: ")
    compressedImage = np.load(compressedImagePath)
    #metadataPath = input("Enter the meta data path: ")


    #with open(metadataPath, "r") as f:
    content = metadataPath.read().decode()
    imgH, imgW, blockHeight, blockWidth, padH , padW = content.split();

    imgH =int(imgH)
    imgW = int(imgW)
    blockHeight = int(blockHeight)
    blockWidth = int(blockWidth)


    reImage = np.zeros((imgH, imgW), dtype=np.uint8)
    i_block = 0
    for i in range(0, imgH, blockHeight):
        for j in range(0, imgW, blockWidth):
            block = codebook[compressedImage[i_block]].reshape((blockHeight, blockWidth))
            reImage[i:i + blockHeight, j:j + blockWidth] = block
            i_block += 1

    img=Image.fromarray(np.uint8(reImage))
    img.save("C:\\Users\Fatma\PycharmProjects\DataCompression\VecCmp\images\decompressed_image.png")

    return None