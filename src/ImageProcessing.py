
def black(pixel):
    """
    Determinates if a pixel is black

    Parameters
    ----------
    pixel(color) : RGB pixel

    Returns
    -------
    bool : T if black || F if not black
    """
    if(pixel[0]== 255):
        return False
    else:
        return True


def getCharBound(row, x, y):
    """
    Gets the char bounds in a text row image, starting the search in x coord

    Parameters
    ----------
    row(numpy.ndarray) : Text row image
    x(int) : Starting right columns of the char, obtained by getNextFirstCharColumn()
    y(int) : Starting top row of the char, by default 0

    Returns
    -------
    int : Top coord of the char
    int : Down coord of the char
    int : Left coord of the char
    int : Right coord of the char

    Uses functions
    ------------------
    bool : :func:`black()`
    """
    top = 9999
    down = 0
    left = x
    right = 0
    isBlankColumn = True
    rows,columns, channel = row.shape
    for j in range(x, columns):
        isBlankColumn = True
        for i in range(rows):
            pixel = row[i,j]
            if(black(pixel)):
                top = min(top, i)
                isBlankColumn = False
                break
        
        for i in range(rows):
            pixel = row[rows-(i+1),j]
            if(black(pixel)):
                down = max(down, rows-i)
                break

        if(isBlankColumn):
            right = max(right, j)
            break

    return top, down, left, right

def getNextFirstCharColumn(row, x):
    """
    Gets the first right pixel culumn of a char in a text row image

    Parameters
    ----------
    row(numpy.ndarray) : Text row image
    x(int) : Starting x coord to search

    Returns
    -------
    int : X coord indicating the columns starting pixel of char

    Uses functions
    --------------
    bool : :func:`black()`
    """
    nextPixel = -1
    rows,columns, channel = row.shape
    for j in range(x, columns):
        for i in range(rows):
            pixel = row[i,j]
            if black(pixel):
                nextPixel = j
                break
        if(nextPixel > -1):
            break
    return nextPixel

def getCharsBounds(row):
    """
    Gets the bounds of all char segments in text row image

    Parameters
    ----------
    row(numpy.ndarray) : Text row image

    Returns
    -------
    list : List of chars bounds

    Uses functions
    --------------
    int[4] : :func:`getCharBound()`
    int : :func:`getNextFirstCharColumn()`
    """
    bounds = []
    columnStartPixel = 0
    while(columnStartPixel != -1):
        top, down, left, right = getCharBound(row, columnStartPixel, 0)
        bounds += [[top, down, left, right]]
        columnStartPixel = getNextFirstCharColumn(row, right+1)
    return bounds

def getCharsSegments(rows, bounds):
    """
    Gets the char segments of text row images acording to chars bounds. rows and bounds

    are list of the same matching sizes.

    Parameters
    ----------
    rows(list) : The list of segmented text row images
    bounds(list) : Bounds matching chars iamges sizes in a text rows

    Returns
    -------
    list : List of segment char images in text row images

    """
    charsSegments = []
    boundsIndex = 0
    for row in rows:
        rowCharBounds = bounds[boundsIndex]
        rowCharsSegments = []
        for charBound in rowCharBounds:
            rowCharsSegments += [ row[(charBound[0]):(charBound[1]),(charBound[2]):(charBound[3])] ]
        boundsIndex += 1
        charsSegments += [rowCharsSegments]
        rowCharsSegments = []
    return charsSegments

def getRowCharBounds(rows):
    """
    Gets the segment image of chars in a text row image
    
    For every row segment gets a list of char segments
    Parameters
    ----------
    rows(list[numpy.ndarray,...]) : The list of segmented text row images

    Returns
    -------
    list : List of segment chars images of the text row images as list = [(list = [char, ...]), ...]

    Uses functions
    --------------
    list : :func:`getCharsBounds()`
    list : :func:`getCharsSegments()`
    """
    bounds = []
    for row in rows:
        bounds += [getCharsBounds(row)]
    return getCharsSegments(rows, bounds)

#.....................................
def getRowBound(image, x, y):
    """
    Gets the top, down, left and right coordenates of  text row in an image.

    Parameters
    ----------
    image(numpy.ndarray) : Image to search the text row bounds
    x(int) : starting x coord of the row, 0 by default
    y(int) : starting y coord of the row, obtained by getNextPixel()

    Returns
    -------
    int : Top coord of the text row
    int : Down coord of the text row
    int : Left coord of the text row
    int : Right coord of the text row

    Uses functions
    --------------
    bool : :func:`black()`
    """
    top = y
    down = -1
    left = 9999
    right = 0
    isBlankRow = True
    rows,columns, channel = image.shape
    for i in range(y, rows):
        isBlankRow = True
        for j in range(columns):
            pixel = image[i,j]
            if(black(pixel)):
                left = min(left, j)
                isBlankRow = False
                break
        for j in range(columns):
            pixel = image[i,columns-(j+1)]
            if(black(pixel)):
                right = max(right, columns-j)
                break
        if (isBlankRow):
            down = max(down, i)
            break
    return top, down, left, right

def getNextFirstRowPixel(image, y):
    """
    Gets the first top pixel of a row in the image. This pixel is searched after y position in the image

    Parameters
    ----------
    image(numpy.ndarray) : Image to search a starting row pixel
    y(int) : Starting position in the image to searcha row first pixel

    Returns
    -------
    int : Y position indicating a starting text row in a image

    Uses functions
    --------------
    bool : :func:`black()`
    """
    nextPixel = -1
    rows,columns, channel = image.shape
    for i in range(y, rows):
        for j in range(columns):
            pixel = image[i,j]
            if black(pixel):
                nextPixel = i
                break
        if(nextPixel > -1):
            break
    return nextPixel

def getSegments(image,bounds):
    """
    Gets separated images acording to bounds provided

    Parameters
    ----------
    image(numpy.ndarray) : Image to obtain segmented image from
    bounds(list) : List of bounds for segment images as lists [top, down, left, right]

    Returns
    -------
    list : The list of segments of an image
    """
    segments = []
    for bound in bounds:
        segments += [image[(bound[0]):(bound[1]),(bound[2]):(bound[3]+1)]]
    return segments


def getImageRowBounds(image):
    """
    Gets the bounds of text rows of the image. 

    NOTE: Is implemented as custom, NOT using libraries

    Parameters
    ----------
    image(numpy.ndarray) : Image to be proccessed and get row bounds

    Returns
    -------
    list : All rows as separated images

    Uses functions
    --------------
    int : :func:`getNextFirstRowPixel()`
    int[4] : :func:`getRowBound()`
    list : :func:`getSegments()`
    """
    bounds = []
    rowStartPixel = getNextFirstRowPixel(image, 0)
    while(rowStartPixel != -1):
        top, down, left, right = getRowBound(image, 0, rowStartPixel)
        bounds += [[top,down,left,right]]
        rowStartPixel = getNextFirstRowPixel(image, down+1)
    return getSegments(image, bounds)

#.....................................

def rgbTogray(rgb):
    """
    Converts a RGB pixel to a grayscale pixel.

    Done by calculating every RGB value divided by 3

    rgb[i]/3
    Parameters
    ----------
    pixel(color) : The pixel as color(R,G,B)

    Returns
    -------
    tuple : (R/3, G/3, B/3)

    """
    grayValue = int(rgb[0]/3 + rgb[1]/3 + rgb[2]/3)
    grayScale = (grayValue, grayValue, grayValue)
    return grayScale

def getGrayScale(image):
    """
    Takes an image and converts it pixels into grayscale image

    NOTE: Does the convertion pixel by pixel, NOT optimized

    Parameters
    ----------
    image(numpy.ndarray) : Image to be converted into grayscale

    Returns
    -------
    image(numpy.ndarray) : The grayscale image

    Uses functions
    --------------
    tuple : :func:`rgbTogray()`
    """
    rows,columns, channel = image.shape
    for i in range(rows):
        for j in range(columns):
            rgbPixel = image[i,j]
            grayPixel = rgbTogray(rgbPixel)
            image[i,j] = grayPixel
    return image

#.................................

def pixelTobitpixel(pixel):
    """
    Converts a grayscale pixel to a black or white pixel.

    Done by using T=150 as the value to decide between B & W

    pixel > 150 = White || pixel < 150 = Black
    Parameters
    ----------
    pixel(color) : The pixel as color(R,G,B)

    Returns
    -------
    tuple : (R, G, B)

    """
    T = 150    
    if (pixel[0] > T):
        return (255, 255, 255)
    else:
        return (0, 0, 0)


def getBinaryImage(image):
    """
    Takes an image and converts it pixels into binary B & W image

    NOTE: Does the convertion pixel by pixel, NOT optimized
    Parameters
    ----------
    image(numpy.ndarray) : Image to be converted into B & W

    Returns
    -------
    image(numpy.ndarray) : The binary image

    Uses functions
    --------------
    tuple : :func:`pixelTobit()`
    """
    rows, columns, channel = image.shape
    for i in range(rows):
        for j in range(columns):
            pixel = image[i,j]
            bitpixel = pixelTobitpixel(pixel)
            image[i,j] = bitpixel
    return image

#..................................


def matrix(rows,columns,val):
    """
    Bulds a matrix of size rows x columns, with val values in cells

    NOTE: Does not checks negative values
    Parameters
    ----------
    rows(int) : The number of rows of the matrix
    columns(int) : The number of columns of the matrix
    val(int) : The value in every cell of the matrix

    Returns
    -------
    list : The matrix
    """
    matrix = []
    for i in range(rows):
        row = []
        for j in range(columns):
            column = val
            row += [column]
        matrix += [row]
    return matrix


def hadamard(n):
    """
    Builds a hadamard matrix of size n, this matrix is created from a cero matrix of size n x n

    Parameters
    ----------
    n(int) : The size of the hadamard matrix n x n

    Returns
    -------
    list : A hardamard matrix of size n x n

    Uses functions
    --------------
    list : :func:`matrix()`
    """
    i1 = 1
    H = matrix(n,n,1)
    while(i1 < n):
        for i2 in range(i1):
            for i3 in range(i1):
                H[i2+i1][i3] = H[i2][i3]
                H[i2][i3+i1] = H[i2][i3]
                H[i2+i1][i3+i1] = -1 * H[i2][i3]
        i1 += i1
    return H

def binaryValue(pixel):
    """
    Teterminates if a RGB pixel is black  or white, to return a 0 or 1 respectively

    NOTE: uses black(pixel) function

    Parameters
    ----------
    pixel(color) : The pixel in color(R,G,B) form

    Returns
    -------
    int : 0 or 1 depending on the pixel value

    Uses functions
    --------------
    bool : :func:`black()`
    """
    if(black(pixel)):
        return 0
    else:
        return 1


def getBinaryValues(image):
    """
    Returns a matrix the same size of an image, containing the binary values of pixels

    NOTE: Pixel by pixel, NOT optimized
    Parameters
    ----------
    image(numpy.ndarray) : Image to obtain binary matrix from

    Returns
    -------
    list : Matrix containing the binary values

    Uses functions
    --------------
    int : :func:`binaryValue()`
    """
    matrix = []
    rows, columns, channel = image.shape
    for i in range(rows):
        newRow = []
        for j in range(columns):
            pixel = image[i,j]
            newColumn = [binaryValue(pixel)]
            newRow += newColumn
        matrix += [newRow]
    return matrix


def mulmat(X,Y):
    """
    Multiplies a matrix X to a matrix Y

    NOTE: Does no checks any matrix sizes.

    Parameters
    ----------
    X(list) : The X list as matrix
    Y(list) : The Y list as matrix

    Returns
    -------
    list : Result multiplied matrix X*Y
    """
    result = matrix(len(X), len(Y[0]), 0)
    for i in range(len(X)):
        for j in range(len(Y[0])):
            for k in range(len(Y)):
                result[i][j] += X[i][k] * Y[k][j]
    return result


def mulsca(scalar, matrix):
    """
    Multiplies a matrix to a scalar

    NOTE: Does not validates any matrix sizes or 0 scalar

    Parameters
    ----------
    scalar(int) : Number scalar to multiply
    matrix(list) : Matrix to be multiplied

    Returns
    -------
    list : multiplied matrix
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = matrix[i][j] * scalar
    return matrix
