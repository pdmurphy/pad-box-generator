from PIL import Image
import numpy as np
import argparse
import csv

parser = argparse.ArgumentParser(description="Generates P&D image collage from a list of Ids.", add_help=False)

inputGroup = parser.add_argument_group("Input")
inputGroup.add_argument("--id_file", required=True, help="Path to text file of id numbers separated by comma")
inputGroup.add_argument("--portraits_dir", required=True, help="Path to card portraits")
inputGroup.add_argument("--imgs_per_row", const=6, default=6, nargs="?", type=int, help="Number of portraits per row. Default is 6")
inputGroup.add_argument("--id_test", action="store_true", help="this will test if your id file can find all portraits")
inputGroup.add_argument("--no_ordering", action="store_true", help="Preserves order of ids for each color. Still color separated")

# outputGroup = parser.add_argument_group("Output")
# outputGroup.add_argument("--output_dir", help="Path to a folder where output should be saved")
helpGroup = parser.add_argument_group("Help")
helpGroup.add_argument("-h", "--help", action="help", help="Displays this help message and exits.")
args = parser.parse_args()

#card_templates_file = args.imgs_per_row
#output_dir = args.output_dir

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
portraitsPath = args.portraits_dir

def testIds():
    #reads file and calls separate Ids
    readIdFile(args.id_file)

def readIdFile(idfilePath):
    # C:/Users/Patrick/Desktop/Coding/PaDBox/idsListNoSpace.txt
    with open(idfilePath) as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        #print("csvreader len", len(csvReader))
        rowcount = 0
        for row in csvReader:
            if(rowcount>=1):
                print("Your ID file is incorrect. Multiple rows")
                exit()
                # not robust and could be worked around but don't want to deal with it as I don't need it
            else:
                separateIds(row)
                rowcount += 1


# myFilePath = "C:/Users/Patrick/Desktop/Coding/PaDBox/resources/PaDTextures/portraits/"

# Pixel location to check
# x:26, y:3 this is a spot on the border
# red: (255,153,102,255)
# blue: (153, 187, 221, 255)
# green: (136, 238, 119, 255)
# light: (255, 255, 119, 255)
# dark:(238, 153, 238, 255)
# empty/noMain attribute (255, 255, 255, 255)


def getColor(filePath, fileName):
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
        addId(getColor(portraitsPath, allIds[i]))

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
# Currently no real error handling 


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
            idPath = portraitsPath + id + ".png"
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
    allColors = None
    # figure out if preserving order or if sorting
    if (args.no_ordering):
        allColors = [red, blue, green, light, dark, blank]
    else:
        sortColors()
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

def sortColors():
    red.sort()
    blue.sort()
    green.sort()
    light.sort()
    dark.sort()
    blank.sort()

def clearIds():
    red.clear()
    blue.clear()
    green.clear()
    light.clear()
    dark.clear()
    blank.clear()

if(args.id_test):
    testIds()
else:
    readIdFile(args.id_file)
    generateBoxCollage(args.imgs_per_row)        
