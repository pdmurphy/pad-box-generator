from PIL import Image
import numpy as np
import argparse
import csv

# Main function calls at bottom.

parser = argparse.ArgumentParser(description="Generates P&D image collage from a list of Ids.", add_help=False)

inputGroup = parser.add_argument_group("Input")
inputGroup.add_argument("--id_file", required=True, help="Path to text file of id numbers separated by comma")
inputGroup.add_argument("--portraits_dir", required=True, help="Path to card portraits")
inputGroup.add_argument("--imgs_per_row", const=6, default=6, nargs="?", type=int, help="Number of portraits per row. Default is 6")
inputGroup.add_argument("--id_test", action="store_true", help="this will test if your id file can find all portraits")
inputGroup.add_argument("--no_ordering", action="store_true", help="Preserves order of ids for each color. Still color separated (including subatt)")

helpGroup = parser.add_argument_group("Help")
helpGroup.add_argument("-h", "--help", action="help", help="Displays this help message and exits.")
args = parser.parse_args()


# make empty list for each color and subattribute per color
# also current id to use in separateIds
global current_id
red = []
redRed = []
redBlue = []
redGreen = []
redLight = []
redDark = []
redBlank = []

blue = []
blueRed = []
blueBlue = []
blueGreen = []
blueLight = []
blueDark = []
blueBlank = []

green = []
greenRed = []
greenBlue = []
greenGreen = []
greenLight = []
greenDark = []
greenBlank = []

light = []
lightRed = []
lightBlue = []
lightGreen = []
lightLight = []
lightDark = []
lightBlank = []

dark = []
darkRed = []
darkBlue = []
darkGreen = []
darkLight = []
darkDark = []
darkBlank = []

blank = []
blankRed = []
blankBlue = []
blankGreen = []
blankLight = []
blankDark = []

current_id = 0
portraitsPath = args.portraits_dir


def testIds():
    # reads file and calls separate Ids
    readIdFile(args.id_file)


def readIdFile(idfilePath):
    with open(idfilePath) as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        rowcount = 0
        for row in csvReader:
            if(rowcount >= 1):
                print("Your ID file is incorrect. Multiple rows")
                exit()
                # not robust and could be worked around but don't want to deal with it as I don't need it
            else:
                separateIds(row)
                rowcount += 1


# Pixel locations to check
# x:26, y:3 this is a spot on the border
# x:85, y:85 for subattribute within the circle spot itself
# technically there is a chance that some art could have the same
# color pixel as a subatt pixel. im willing to take that chance

def getColor(filePath, fileName):
    combinedPath = filePath + fileName + ".png"
    image = Image.open(combinedPath)
    color = image.getpixel((26, 3))
    subColor = image.getpixel((85, 85))
    return (colorHelper(color), colorSubAttHelper(subColor))


def colorHelper(RGBValue):
    return {
        (255, 153, 102, 255): "red",
        (153, 187, 221, 255): "blue",
        (136, 238, 119, 255): "green",
        (255, 255, 119, 255): "light",
        (238, 153, 238, 255): "dark",
        (255, 255, 255, 255): "blank"  # No Main Attribute
    }.get(RGBValue, "???")


def colorSubAttHelper(RGBValue):
    return {
        (255, 119, 51, 255): "red",
        (34, 68, 102, 255): "blue",
        (85, 255, 68, 255): "green",
        (255, 238, 68, 255): "light",
        (68, 34, 102, 255): "dark",
    }.get(RGBValue, "blank")


# this is where things get a bit wonky
# current_id has to be a global variable that is changed so it can be used by the add functions
# refer to comment section before addId
def separateIds(allIds):
    for i in range(len(allIds)):
        global current_id
        current_id = allIds[i]
        addId(getColor(portraitsPath, allIds[i]))

# I cant use the same return match style as getColor to call red.append(id) for example
# python doesn't work this way.
# it would call the functions and the returned value from those functions as assigned to that key of the dictionary
# so instead I have to call individual add functions, and have it use current_id
# if i called the individual functions passing id.
# it would be the same problem as if I just did red.append(id)
# not a fan of this system but without doing a different type of switch statement or case match
# i do not believe it is possible.


def addId(colors):
    switcher = {
        # red
        ("red", "red"): addRedRed,
        ("red", "blue"): addRedBlue,
        ("red", "green"): addRedGreen,
        ("red", "light"): addRedLight,
        ("red", "dark"): addRedDark,
        ("red", "blank"): addRed,
        # blue
        ("blue", "red"): addBlueRed,
        ("blue", "blue"): addBlueBlue,
        ("blue", "green"): addBlueGreen,
        ("blue", "light"): addBlueLight,
        ("blue", "dark"): addBlueDark,
        ("blue", "blank"): addBlue,
        # green
        ("green", "red"): addGreenRed,
        ("green", "blue"): addGreenBlue,
        ("green", "green"): addGreenGreen,
        ("green", "light"): addGreenLight,
        ("green", "dark"): addGreenDark,
        ("green", "blank"): addGreen,
        # light
        ("light", "red"): addLightRed,
        ("light", "blue"): addLightBlue,
        ("light", "green"): addLightGreen,
        ("light", "light"): addLightLight,
        ("light", "dark"): addLightDark,
        ("light", "blank"): addLight,
        # dark
        ("dark", "red"): addDarkRed,
        ("dark", "blue"): addDarkBlue,
        ("dark", "green"): addDarkGreen,
        ("dark", "light"): addDarkLight,
        ("dark", "dark"): addDarkDark,
        ("dark", "blank"): addDark,
        # No Main Attribute
        ("blank", "red"): addBlankRed,
        ("blank", "blue"): addBlankBlue,
        ("blank", "green"): addBlankGreen,
        ("blank", "light"): addBlankLight,
        ("blank", "dark"): addBlankDark
    }
    func = switcher.get(colors, 'Invalid colors')
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
        mergeColors()
        allColors = [red, blue, green, light, dark, blank]
    else:
        sortColors()
        mergeColors()
        allColors = [red, blue, green, light, dark, blank]
    # start with empty collage
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
    redBlank.append(current_id)


def addRedRed():
    redRed.append(current_id)


def addRedBlue():
    redBlue.append(current_id)


def addRedGreen():
    redGreen.append(current_id)


def addRedLight():
    redLight.append(current_id)


def addRedDark():
    redDark.append(current_id)


def addBlue():
    blueBlank.append(current_id)


def addBlueRed():
    blueRed.append(current_id)


def addBlueBlue():
    blueBlue.append(current_id)


def addBlueGreen():
    blueGreen.append(current_id)


def addBlueLight():
    blueLight.append(current_id)


def addBlueDark():
    blueDark.append(current_id)


def addGreen():
    greenBlank.append(current_id),


def addGreenRed():
    greenRed.append(current_id),


def addGreenBlue():
    greenBlue.append(current_id),


def addGreenGreen():
    greenGreen.append(current_id),


def addGreenLight():
    greenLight.append(current_id),


def addGreenDark():
    greenDark.append(current_id),


def addLight():
    lightBlank.append(current_id),


def addLightRed():
    lightRed.append(current_id),


def addLightBlue():
    lightBlue.append(current_id),


def addLightGreen():
    lightGreen.append(current_id),


def addLightLight():
    lightLight.append(current_id),


def addLightDark():
    lightDark.append(current_id),


def addDark():
    darkBlank.append(current_id)


def addDarkRed():
    darkRed.append(current_id)


def addDarkBlue():
    darkBlue.append(current_id)


def addDarkGreen():
    darkGreen.append(current_id)


def addDarkLight():
    darkLight.append(current_id)


def addDarkDark():
    darkDark.append(current_id)


def addBlank():
    blank.append(current_id)


def addBlankRed():
    blankRed.append(current_id)


def addBlankBlue():
    blankBlue.append(current_id)


def addBlankGreen():
    blankGreen.append(current_id)


def addBlankLight():
    blankLight.append(current_id)


def addBlankDark():
    blankDark.append(current_id)


def sortColors():
    sortReds()
    sortBlues()
    sortGreens()
    sortLights()
    sortDarks()
    sortBlanks()


def mergeColors():
    mergeReds()
    mergeBlues()
    mergeGreens()
    mergeLights()
    mergeDarks()
    mergeBlanks()


def sortReds():
    redRed.sort()
    redBlue.sort()
    redGreen.sort()
    redLight.sort()
    redDark.sort()
    redBlank.sort()


def sortBlues():
    blueRed.sort()
    blueBlue.sort()
    blueGreen.sort()
    blueLight.sort()
    blueDark.sort()
    blueBlank.sort()


def sortGreens():
    greenRed.sort()
    greenBlue.sort()
    greenGreen.sort()
    greenLight.sort()
    greenDark.sort()
    greenBlank.sort()


def sortLights():
    lightRed.sort()
    lightBlue.sort()
    lightGreen.sort()
    lightLight.sort()
    lightDark.sort()
    lightBlank.sort()


def sortDarks():
    darkRed.sort()
    darkBlue.sort()
    darkGreen.sort()
    darkLight.sort()
    darkDark.sort()
    darkBlank.sort()


def sortBlanks():
    blankRed.sort()
    blankBlue.sort()
    blankGreen.sort()
    blankLight.sort()
    blankDark.sort()


def mergeReds():
    red.extend(redRed)
    red.extend(redBlue)
    red.extend(redGreen)
    red.extend(redLight)
    red.extend(redDark)
    red.extend(redBlank)


def mergeBlues():
    blue.extend(blueRed)
    blue.extend(blueBlue)
    blue.extend(blueGreen)
    blue.extend(blueLight)
    blue.extend(blueDark)
    blue.extend(blueBlank)


def mergeGreens():
    green.extend(greenRed)
    green.extend(greenBlue)
    green.extend(greenGreen)
    green.extend(greenLight)
    green.extend(greenDark)
    green.extend(greenBlank)


def mergeLights():
    light.extend(lightRed)
    light.extend(lightBlue)
    light.extend(lightGreen)
    light.extend(lightLight)
    light.extend(lightDark)
    light.extend(lightBlank)


def mergeDarks():
    dark.extend(darkRed)
    dark.extend(darkBlue)
    dark.extend(darkGreen)
    dark.extend(darkLight)
    dark.extend(darkDark)
    dark.extend(darkBlank)


def mergeBlanks():
    blank.extend(blankRed)
    blank.extend(blankBlue)
    blank.extend(blankGreen)
    blank.extend(blankLight)
    blank.extend(blankDark)


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
    # if I want to have a correct "unordered" option. I would need to check and have readIdFile run differently (or make a secondReadIdFile for unordered specifically)
    readIdFile(args.id_file)
    generateBoxCollage(args.imgs_per_row)
