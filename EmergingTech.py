# Conor Tighe - G00314417
import gzip
import numpy as np
import PIL.Image as pil


def read_labels_from_file(filename): # Does work for reading in the labels from desired file
    with gzip.open(filename,'rb') as f: # open file and have f represent the file in python
        magic = f.read(4) # read desired bytes
        magic = int.from_bytes(magic,'big') # find magic number by converting to int and rounding up
        print("Magic is:", magic)

        nolab = f.read(4) # re-read bytes
        nolab = int.from_bytes(nolab,'big') # store number of labels 
        print("Num of labels is:", nolab) # show user number of labels

        labels = [f.read(1) for i in range(nolab)] # read through labels and store raw data
        labels = [int.from_bytes(label, 'big') for label in labels] # round off to ints

    return labels

def read_images_from_file(filename): # Does work for reading in the images in a desired file
    with gzip.open(filename,'rb') as f:  # open file and have f represent the file in python
        magic = f.read(4) # read desired bytes
        magic = int.from_bytes(magic,'big') # find magic number by converting to int and rounding up
        print("Magic is:", magic) # print magic

        noimg = f.read(4) # read number of images
        noimg = int.from_bytes(noimg,'big') # round up number of images and convert to int
        print("Number of images is:", noimg)

        norow = f.read(4) # read number of rows
        norow = int.from_bytes(norow,'big') # round up and convert to int
        print("Number of rows is:", norow) # show user number of rows

        nocol = f.read(4) # read columns
        nocol = int.from_bytes(nocol,'big') # round up and convert to int
        print("Number of cols is:", nocol) # show user number of column

        images = [] # image array

        for i in range(noimg): # loop through total images
            rows = [] # array for rows
            for r in range(norow): # loop through rows
                cols = [] # array for cols
                for c in range(nocol): # loop throught columns
                    cols.append(int.from_bytes(f.read(1), 'big')) # update cols array with location contents
                rows.append(cols) # add columns belonging to row
            images.append(rows) # add row to images array
    return images

def printNum(images, i):
    for row in images[i]: # loop thorugh image array
        for col in row: # for every column in a row
            print('.' if col <= 127 else '#', end='') # print the columns with a value less or equal to 127 as '.' and anything greater as '#' also add a space after for readability
        print()   


def saveImages(images, labels):
    i = 0
    for img in images: # loop though images in image array
        pngImg = img # store current image
        pngImg = np.array(pngImg) # store in numpy array
        pngImg = pil.fromarray(pngImg) # convert from array using PIL
        pngImg = pngImg.convert('RGB') # convert to RGB format
        pngImg.save("CreatedImgs/train-"+str(i)+"-"+str(labels[i])+".png") # save as train-XXXXX-Y.png where x is image number and y is label
        i += 1

def Menu():
    i = 0
    choice = 0
    e = False
    print("Loading in files, this takes a while...")
    print("Train Images:")
    train_images = read_images_from_file("train-images-idx3-ubyte.gz") # Importing the images from the .gz file
    print("Train Labels:")
    train_labels = read_labels_from_file("train-labels-idx1-ubyte.gz") # Importing the labels from the .gz file

    # Tests and raw data prints
    #test_images = read_images_from_file("t10k-images-idx3-ubyte.gz")
    #test_labels = read_labels_from_file("t10k-labels-idx1-ubyte.gz")
    #print(train_labels)
    #print(test_labels)

    while (e != True):
        print("Enter 1. Print Number of choice, 2. Save images to CreateImgs folder 3. Exit")
        choice = int(input()) # get user input

        if choice == 1:
            print("Enter number to select an image from the dataset array")
            i = int(input())
            printNum(train_images, i) # print image of choice
        elif choice == 2:
            print("Saving images....")
            saveImages(train_images,train_labels) # save images locally
            print("Images saved to CreatedImgs folder....")
        else:
            print("exiting..")
            e = True

Menu()