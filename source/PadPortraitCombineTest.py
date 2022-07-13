# PadPortraitCombineTest
from PadBoxImageGenerator import *
import unittest

# three test cases. 1 of each color
# one with wrong id names
# one with two reds (for organizing)
realIds = ["1", "5", "9", "13", "17", "7434"]
fakeIds = ["1.1", "2.2"]
multipleRedIdsOutOfOrder = ["1", "5", "9", "13", "17", "7434", "36"]  # 36 is the second red


class TestIdSeparation(unittest.TestCase):

    def setUp(self):
        # clearIds between runs
        clearIds()

    def tearDown(self):
        # clearIds between runs
        clearIds()

    def test_real_ids(self):
        print("Testing real existing Ids, one of each color")
        separateIds(realIds)
        self.assertEqual(['1'], red, "red: should be ['1']")
        self.assertEqual(['5'], blue, "blue: should be ['5']")
        self.assertEqual(['9'], green, "green: should be ['9']")
        self.assertEqual(['13'], light, "light: should be ['13']")
        self.assertEqual(['17'], dark, "dark: should be ['17']")
        self.assertEqual(['7434'], blank, "blank: should be ['7434']")

    def test_fake_ids(self):
        print("Testing fake existing Ids, should throw error")
        self.assertRaises(FileNotFoundError, separateIds, fakeIdsArray)

    def test_real_ids_two_reds(self):
        print("Testing real ids, two for red")
        separateIds(multipleRedIdsOutOfOrder)
        print(red)
        print(blue)
        self.assertEqual(['1', '36'], red, "red: should be ['1', '36']")
        self.assertEqual(['5'], blue, "blue: should be ['5']")
        self.assertEqual(['9'], green, "green: should be ['9']")
        self.assertEqual(['13'], light, "light: should be ['13']")
        self.assertEqual(['17'], dark, "dark: should be ['17']")
        self.assertEqual(['7434'], blank, "blank: should be ['7434']")

    def end_of_test(self):
        print("COMPLETE: Testing complete")


class TestCollageMaking(unittest.TestCase):

    # NOTE: this swuite is a bit of a manual test.
    # at present time. You have to comment one of the two tests
    # as the image will overwrite if you run both
    # either way you will only get one image result

    def setUp(self):
        # clearIds between runs
        clearIds()

    def tearDown(self):
        # clearIds between runs
        clearIds()

    def test_two_columns_empty_fill(self):
        """
        Testing that real ids can be identified by color and put into correct separated lists
        """
        print("Testing collage making")
        separateIds(multipleRedIdsOutOfOrder)
        generateBoxCollage(2)

    def test_1_column_no_empty(self):
        print("Testing collage 1 column")
        separateIds(multipleRedIdsOutOfOrder)
        generateBoxCollage(1)


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestIdSeparation))
    test_suite.addTest(unittest.makeSuite(TestCollageMaking))
    return test_suite


mySuit = suite()


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(mySuit)
#   unittest.main()
