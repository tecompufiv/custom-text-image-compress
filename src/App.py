import numpy as np
import cv2
from ImageProcessing import getGrayScale, getBinaryImage
from ImageProcessing import getImageRowBounds
from ImageProcessing import getRowCharBounds
from ImageProcessing import getBinaryValues
from ImageProcessing import hadamard
from ImageProcessing import mulmat
from ImageProcessing import mulsca


#T show proff of work inside work folder
haveToShowWork = False

def resizeChars(rowsChars):
    """
    Resize the images to a 64x64 size and converts them into binary images
    
    Parameters
    ----------
    rowChars : List = [image: numpy.ndarray, ...]

    Returns
    -------
    list : a list containing the resized binary images of chars
    """
    rows = len(rowsChars)
    for i in range(rows):
        columns = len(rowsChars[i])
        for j in range(columns):
            rowsChars[i][j] = getBinaryImage(cv2.resize(rowsChars[i][j], (64, 64)))
    return rowsChars



def main(path):

    img = cv2.imread(path,1) #opens the image (color)    

    #1 - Gets the grayscale image
    img = getGrayScale(img)

    if haveToShowWork:
        cv2.imwrite('./../work/grayText.png',img)
    #2 - Gets the binary image of the grayscale image
    img = getBinaryImage(img)

    if haveToShowWork:
        cv2.imwrite('./../work/binaryText.png',img)
    #3 - Gets the text row segments images
    imgRows = getImageRowBounds(img)

    if haveToShowWork:
        cv2.imwrite('./../work/row.png',imgRows[0])
    #4 - Gets the char images segments of text row segments
    rowsChars = getRowCharBounds(imgRows)

    if haveToShowWork:
        cv2.imwrite('./../work/originalsizechar.png',rowsChars[0][0])

    #5 - Gets the char images resized to 64x64 (converted again to binary due to the scaling pixels)
    binaryChars = resizeChars(rowsChars) #The resize requires to apply the binary transform

    if haveToShowWork:
        cv2.imwrite('./../work/binaryresizedchar.png',binaryChars[0][0])
        binary = getBinaryValues(binaryChars[0][0])
        #[print(row) for row in binary]
        #print(len(binary), len(binary[0]))
    

    #6 - Converts the binary char images to binary matrixes
    i = 0
    j = 0
    for row in binaryChars:
        for char in row:
            binaryChars[i][j] = getBinaryValues(binaryChars[i][j])
            j+=1
        i+=1
        j=0
    
    # Hadammard Walsh matrix of size 64x64
    H = hadamard(64)
    H = mulsca((1/len(H)), H) #This line can be removed
    #7 - Multiply all binary matrixes one by one to the H-W matrix
    i = 0
    j = 0
    for row in binaryChars:
        for char in row:
            Y = char
            multed = mulmat(H, Y)
            multed = mulmat(multed, H)
            binaryChars[i][j] = multed
            j+=1
        i+=1
        j=0

    #8 - generates the H-W vectors of size 64
    i = 0
    j = 0
    transform = []
    for row in binaryChars:
        for char in row:
            for charRow in char:
                transform += [sum(charRow)]
            binaryChars[i][j] = transform
            j+=1
            transform = []
        i+=1
        j=0
    
    if haveToShowWork:
        print("Vector size:", len(binaryChars[0][0]))
        print( "Vector:" , binaryChars[0][0])
    

imageCharsTransforms = main('./../images/text2.png')

