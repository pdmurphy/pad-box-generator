from PIL import Image
import numpy as np

# make empty list for each color
# also current id to use in separateIds
global current_id
red = []
green = []
blue = []
dark = []
light = []
blank = []
current_id = 0

filePath = "C:/Users/Patrick/Desktop/Coding/PaDBox/resources/PaDTextures/portraits/"

# Pixel location to check
# x:26, y:3 this is a spot on the border
# red: (255,153,102,255)
# blue: (153, 187, 221, 255)
# green: (136, 238, 119, 255)
# light: (255, 255, 119, 255)
# dark:(238, 153, 238, 255)
# empty/noMain attribute (255, 255, 255, 255)


def getColor(fileName):
    combinedPath = filePath + fileName + ".png"
    image = Image.open(combinedPath)
    color = image.getpixel((26, 3))
    print("color check")
    print(colorHelper(color))
    return colorHelper(color)


def colorHelper(RGBValue):
    return {
        (255, 153, 102, 255): "red",
        (153, 187, 221, 255): "blue",
        (136, 238, 119, 255): "green",
        (255, 255, 119, 255): "light",
        (238, 153, 238, 255): "dark",
        (255, 255, 255, 255): "blank"  # No Main Attribute
    }.get(RGBValue, "???")

# this is where things get a bit wonky
# current_id has to be a global variable that is changed so it can be used by the add functions
# refer to comment section before addId
def separateIds(allIds):
    for i in range(len(allIds)):
        print("id:", allIds[i])
        global current_id
        current_id = allIds[i]
        print("current id in separate", current_id)
        addId(getColor(allIds[i]))

# I cant use the same return match style as getColor to call red.append(id) for example
# python doesn't work this way.
# it would call the functions and the returned value from those functions as assigned to that key of the dictionary
# so instead I have to call individual add functions, and have it use current_id
# if i called the individual functions passing id. 
#  it would be the same problem as if I just did red.append(id)
# not a fan of this system but without doing a different type of switch statement or case match
# i do not believe it is possible. 


def addId(color):
    print("add id with current id", current_id, "and color", color)
    switcher = {
        "red": addRed,
        "blue": addBlue,
        "green": addGreen,
        "light": addLight,
        "dark": addDark,
        "blank": addBlank  # No Main Attribute
    }
    func = switcher.get(color, 'Invalid color')
    return func()
# Gotta figure out some error handling type stuff


def generateBoxRow(index, portraitsPerRow, colorArray):
    # 100,100,4 are the dimensions for a portrait in terms of np
    # you need the dimensions of empty spot to match the normal portrait dimensions otherwise it errors
    # figured out these dimensions via little test like imageData.shape or .ndim
    row = np.zeros((100, 100, 4), np.uint8)
    i = 0
    while i < portraitsPerRow:  # loop for amount of portraits per row
        # need to use passed index so the id we grab for colorArray is correct
        if index < len(colorArray):
            id = colorArray[index]
            idPath = filePath + id + ".png"
            image = Image.open(idPath)
            imageData = np.asarray(image)
            if i == 0:
                # if first image in row, you just add it by itself
                row = np.hstack([imageData])
            else:
                row = np.hstack([row, imageData])
        else:
            row = np.hstack([row, np.zeros((100, 100, 4), np.uint8)])
        i = i + 1
        index = index + 1
    return (row, index)


def generateBoxCollage(portraitsPerRow):
    allColors = [red, blue, green, light, dark, blank]
    #start with empty collage
    collage = np.zeros((100, 100, 4), np.uint8)
    for colorArray in allColors:
        index = 0
        while index < len(colorArray):
            row, updatedIndex = generateBoxRow(index, portraitsPerRow, colorArray)
            if colorArray == red and index == 0:
                collage = np.vstack([row])
            else:
                collage = np.vstack([collage, row])
            index = updatedIndex
            # update index to the number given from generateBoxRow

    finalImage = Image.fromarray(collage)
    finalImage.save("PaDBox.png")


# if id = 0 

# do the full run with fake ids first of course
# image = Image.open(r"C:\Users\Patrick\Pictures\2na71g3.jpg")
# data = np.asarray(image)
# collage = np.vstack([data, data])
# data2 = np.vstack([data, np.zeros((124, 124, 3), np.uint8)])
# collage = np.hstack([collage, data2])
# append to add to a list (normal python list, not np array)


def addRed():
    red.append(current_id)


def addBlue():
    blue.append(current_id)


def addGreen():
    green.append(current_id),


def addLight():
    light.append(current_id),


def addDark():
    dark.append(current_id)


def addBlank():
    blank.append(current_id)


def clearIds():
    red.clear()
    blue.clear()
    green.clear()
    light.clear()
    dark.clear()
    blank.clear()

import csv

#with open("C:/Users/Patrick/Desktop/Coding/PaDBox/idsListNoSpace.txt") as csvfile:
   # csvReader = csv.reader(csvfile, delimiter=',')
#    for row in csvReader:
 #       print("row", row)
#        print(type(row))
 #       print(len(row))
     #   #separateIds(row)
        
# uncomment later^



        # premake for lists/arrays/whatever they are that are used to do collages
        # one for each color
        # loop through each id in row
        # for each id. run the color getter.
        # here is where im unsure
        # either
        # do the arary conversion thing for the image and add it to the correct color array
        # or just do list of ids for each color first
        # then run thing that does the collage-ing for each color array
        # then run collaging thing that combines all of them
        # i like the doing id list for each better
        # but it is almost assurdely less performant.

