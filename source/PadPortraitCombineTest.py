# PadPortraitCombineTest
from PIL import Image
from PadBoxImageGenerator import * 
import numpy as np
import unittest

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





#order of colors
# red, blue, green, light, dark, blank
# print("Testing real existing Ids, one of each color")
# assert ['1'] == red, "red: should be ['1']"
# assert ['5'] == blue, "blue: should be ['5']"
# assert ['9'] == green, "green: should be ['9']"
# assert ['13'] == light, "light: should be ['13']"
# assert ['17'] == dark, "dark: should be ['17']"
# assert ['7434'] == blank, "blank: should be ['7434']"


#print("COMPLETE: Testing real existing Ids, one of each color")

class TestIdSeparation(unittest.TestCase):

    def test_real_ids(self):
        """
        Testing that real ids can be identified by color and put into correct separated lists
        """
        realIds = ["1", "5", "9", "13", "17", "7434"]
        print("Testing real existing Ids, one of each color")
        separateIds(realIds)
        print(red)
        print(blue)
        self.assertEqual(['1'], red, "red: should be ['1']")
        self.assertEqual(['5'], blue, "blue: should be ['5']")
        self.assertEqual(['9'], green, "green: should be ['9']")
        self.assertEqual(['13'], light, "light: should be ['13']")
        self.assertEqual(['17'], dark, "dark: should be ['17']")
        self.assertEqual(['7434'], blank, "blank: should be ['7434']")

    def test_fake_ids(self):
        print("Testing fake existing Ids, should throw error")
        self.assertRaises(FileNotFoundError, separateIds, fakeIdsArray)

    def end_of_test(self):
        print("COMPLETE: Testing complete")


if __name__ == '__main__':
    unittest.main()


