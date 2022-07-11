# PadPortraitCombineTest
from PIL import Image
from PadBoxImageGenerator import * 
import numpy as np


# three test cases. 1 of each color
# one with wrong id names
# one with two reds (for organizing)
realIds = ["1", "5", "9", "13", "17", "7434"]
fakeIds = ["1.1", "2.2"]
multipleRedIdsOutOfOrder = ["1", "5", "9", "13", "17", "7434", "36"]  # 36 is the second red

# convert Into np array
realIdsArray = np.array(realIds)
fakeIdsArray = np.array(fakeIds)
multipleRedIdsOutOfOrderArray = np.array(multipleRedIdsOutOfOrder)

print("run getColor test FILE 1")
getColor("1")

separateIds(realIds)

print(red)
print(blue)