#using list of IDs 
#open each image and categorize into 6 (5+colorless) separate array lists based on color

#combine the 6 arrays back into 1 list of IDs that will now be organized by color
#returning that combined/organized list

#run image generator that takes list of IDs and creates combined image of them all



#one issue is that ending segments of each color
#their arrayys will need an "empty" or somethjing to fill so that the empty slots are accounted for
#cause i think otherwise it wont combine correctly at the end vertically from what I tested.


#function example
# def get_portraits_img(file_name):
#     if file_name not in card_imgs:
#         file_path = os.path.join(args.input_dir, file_name)
#         if not os.path.exists(file_path):
#             return None
#         card_imgs[file_name] = Image.open(file_path)
#     return card_imgs[file_name]

#to split between multiple files. 
#ypu just import myfile
#file myfile example
#def get_user_age():
#   return int(input("Enter your age: "))
#file main example
#import myfile
# try:
#     myfile.get_user_age()
# except ValueError:
#     print("That's not a valid value for your age!")


from PIL import Image
import numpy as np

# three test cases. 1 of each color
# one with wrong id names
# one with two reds (for organizing)
realIds = [1, 5, 9, 13, 17, 7434]
fakeIds = [1.1, 2.2]
multipleRedIdsOutOfOrder = [1, 5, 9, 13, 17, 7434, 36]  # 36 is the second red

# convert Into np array
realIdsArray = np.array(realIds)
fakeIdsArray = np.array(fakeIds)
multipleRedIdsOutOfOrderArray = np.array(multipleRedIdsOutOfOrder)

# make empty list for each color
global red
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


print("run getColor 1")
getColor("1")

# idFile = open("C:/Users/Patrick/Desktop/Coding/PaDBox/idsList.txt")
# print(idFile.readline())


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

# I cant use this return match style to call red.append(id) for example
# python doesn't work this way.
# it would call the functions and the returned value from those functions as assigned to that key of the dictionary
# so instead I have to call individual add functions, and have it use current_id
# if i called the individual functions passing id. 
#  it would be the same problem as if I just did red.append(id)
# not a fan of this system but without doing a different type of switch statement or case match
# i do not believe it is possible. I'm on Python 3.8.xx so I am missing some features


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
#okay forget everything
#this above thing will not work
#it still jsut executes addRed for every id for the same reason i think
#going to have to figure out a different type of switch case way in python.
#going to push for the sake of history

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

# do the full run with fake ids first of course

# data = np.asarray(image)
# collage = np.vstack([data, data])
# data2 = np.vstack([data, np.zeros((124, 124, 3), np.uint8)])
# collage = np.hstack([collage, data2])
#append to add to a list (normal python list, not np array)

