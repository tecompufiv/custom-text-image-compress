Index
    1 - COMPLETION
    2 - RUN
    3 - STRENGHTS
    4 - WEAKNESES
    5 - ANNOTATION
    6 - CODE EXPLANATION
    7 - CONCLUSION


COMPLETION
    
    Implement a custom data structure:- -   -   -   -   -   -   -   -   -   [OPTIONAL][DONE WITH NATIVE PYTHON LINKEDLISTS]

    Linked list which contain segments of the picture-  -   -   -   -   -   [DONE]
    - Segment's starting x and y coords
    - Segment height and width
    - Boolean if its an indvidual character or not
    - 64x64 binary picture of the character (initially empty)
    - 64 int array (result of the Hadamard transform)
    - Final character code

    [OBLIGATORI]
    Workflow of the program:
    - Open an image file (color) which contain text (could use OpenCV). -   [DONE][See App.py, line 37]

    - Convert to grayscale (could use OpenCV, but better a custom 
    implementation).-   -   -   -   -   -   -   -   -   -   -   -   -   -   [DONE][See ImageProcessing.py, line 317]

    - Treshold the grayscale to get a binary picture (should be own 
    implementation, not OCV). - -   -   -   -   -   -   -   -   -   -   -   [DONE][See ImageProcessing.py, line 368]

    - Segment vertically, finding not empty rows and building the 
    linked list (aka. finding the bounding box of text rows)-   -   -   -   [DONE][See ImageProcessing.py, line 267]

    - Running through the list, segmenting horizontally, 
    seeking empty pixel columns, so finding the bounding box 
    of individual chars, inserting them into, "replacing" the row segment.- [DONE][See ImageProcessing.py, line 150]

    - Cuting out empy rows or columns from the characters bounding box.-    [DONE][By avoiding this empty rows]

    - Transforming each character's picture (the bounding box 
    part of the original picture) to a 64x64 binary image, 
    and storing this in the linked list element-    -   -   -   -   -   -   [DONE][See App.py, line 14]

    - Applying Hadamard-Walsh tranformation to each 64x64 picture, 
    storing the result of the transform into the 
    array-  -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   [DONE][See App.py, line 81]

    The program should finally compare H-W transform value to a 
    pre-built "database" of various characters with 
    various fonts (the English ABC with maybe Ariel, Times New Roman, 
    and something else)-    -   -   -   -   -   -   -   -   -   -   -   -   [OPTIONAL][NOT DONE][BUT IT DOES WORKS WITH VARIUS FONTS]

RUN

    The program is ready to run with

    $ - App.py | If you have python installed and added to the native System PATH

    $ - ../py App.py | If you need to call the python binarie compiler in order to execute the programm

    NOTE: The programm can show a partial work done by modifying the variable haveToWork in the App.py file, at the top of the code

STRENGHTS

    -The program resulted in a modular program, you can get an HW array of chars from an image by calling
    the main function and giving it the path to your image, I recommend using complete paths NOT relative paths.

    -The program is using full stringdoc showing params, returns, and function being usen inside a function

    -The programm succesfully gets chars without blank spaces or fixel sizes, this is done by a custom code

    -The programm succesfully applies the HW transform to the 64x64 matrixes, the Hadamard Walsh matrix is being 
    generated inside the code as custom

    -All images convertions and modifications are made custom pixel by pixel.

    -The proof of works as "I practiced and learned how to do it", is correctly shown in the code. This is
    possible thanks to the custom code made.

    -The program needs only a single path to and image and it will get the HW vectors.

    -Dependencies between functions are minimal and said functions are modular, following modularity rules


WEAKNESES


    -The programm is Slow, this depends on the machine proccessing power BUT, overall is slow.

    -The program uses sequential modification on images, this is not optimal, but due to the goal
    of the task beaing a "learning" task, this is acceptable i suposse-

    -The program is not optimal, the proccessing of an image can take several minutes depending on the size.
    For this task a 8 million pixel images was tested and took around 2 minutes of proccessing.

    -The optional task was not done, but this seems not to be a problem. This optional part can be
    achived easy due to the single call modularity provided.

    -Is not using object oriented programming, even knowing this is not hard to change I DON'T recommend
    using OOP, because this paradigm reduces proccessing speed. Changing this is up to you.

    -The programm is not capable to proccess phone pictures, specially when peper sound is in the image.
    I tested som clean phone images and seems to work but is not entirely accurate. This might require
    a more complex solution like a gauss transform


ANNOTATION

    -Overall the programm is working great, I added the docstring for you to understand easier.

    -The App.py code includes som statements used to show the proff of work, you can get rid off this lines with no problem

    -I recommend an IDE with intellisense such as vscode to check the code, this is so you can
    see the documentation with the pop ups and save time navigating through the code.

    -Due to the paradigm used, the docstring includes wich functions are being used. E.g. inside
    foo(), foo1() and foo2() are being used, this is specified in the docstring of foo() for a better
    comprehension.

    -The HW transform is done with matrix of single vale cell, not pixels, I'm adding this couse
    i did as i investigated.

CODE EXPLANATION

    Getting the row segments
        1 - sequential horizontal search until a black pixel is found
        2 - starting from the pixel founded searchs horizontally until it finds a blank pixel row. This blank row is the bottom part of the row
        3 - while the step 2 is happening the program finds the left smalles pixel and the right greater pixel.
        4 - When step 2 is done, the bounds are saved and the algorithm looks for the next starting pixel row until it reach the end 
        of the image
        5 - segment the original image acording to the segments obtained.
        6 - time is saved by stopping the search at the momment a black pixel apears, this redices time searching

    Getting the char segmentes
        1 - sequential vertical search until a black pixel is found
        2 - starting from the pixel founded searchs vertical until it finds a blank pixel column. This blank column is the right part of the char
        3 - while the step 2 is happening the program finds the top smalles pixel and the bottom greater pixel.
        4 - When step 2 is done, the bounds are saved and the algorithm looks for the next starting pixel column until it reach the end 
        of the image
        5 - segment the original image acording to the segments obtained.
        6 - time is saved by stopping the search at the momment a black pixel apears, this redices time searching

    HW function
        1 - Creates the binary matrixes with 0 and 1 acording to the binary images
        2 - Creates the HW matrix
        3 - Being H = HW matrix & M the binary matrix & a option scalar sometimes used as S = 1 / len(H)
        4 - for each M in M's: M = H * M * H [* scalar]
        5 - for each M in M's: sumColumns(M)

CONCLUSION

    -The code is as specified, it can be improve but this means using non custom functions.

    -The goal of the task was accomplished

    -A basic level explanation diagram was included.

    -I would love to see the programm running in a more powered machine

    -I think the optional part is not hard to get done is problably taking the converted HW vectors and compare element by element.
    i still don't entirely understand this part