import unittest
from dtmove.dtmove import filter_bases


class TestFilterBases(unittest.TestCase):
    def test_filterbases_simple(self):
        basepaths = {
            "/the": ["/the/old"],
            "/the/old": ["/the/old/folder", "/the/old/folder2"],
            "/the/old/folder": ["/the/old/folder/a", "/the/old/folder/b"],
        }

        basepaths_filtered = filter_bases(basepaths)

        expected_basepaths = {
            "/the/old": ["/the/old/folder", "/the/old/folder2"],
            "/the/old/folder": ["/the/old/folder/a", "/the/old/folder/b"],
        }
        self.assertEqual(basepaths_filtered, expected_basepaths)

    def test_filterbases_single(self):
        basepaths = {
            "/the": ["/the/old"],
            "/the/old": ["/the/old/folder"],
            "/the/old/folder": ["/the/old/folder/a"],
        }

        basepaths_filtered = filter_bases(basepaths)

        expected_basepaths = {
            "/the/old/folder": ["/the/old/folder/a"],
        }
        self.assertEqual(basepaths_filtered, expected_basepaths)

    def test_filterbases_nested_singlebranch(self):
        basepaths = {
            "/the": ["/the/old1", "/the/old2"],
            "/the/old1": ["/the/old1/folder"],
            "/the/old2": ["/the/old2/folder"],
            "/the/old1/folder": ["/the/old1/folder/a"],
        }

        basepaths_filtered = filter_bases(basepaths)

        expected_basepaths = {
            "/the": ["/the/old1", "/the/old2"],
            "/the/old1": ["/the/old1/folder"],
            "/the/old2": ["/the/old2/folder"],
            "/the/old1/folder": ["/the/old1/folder/a"],
        }
        self.assertEqual(basepaths_filtered, expected_basepaths)


if __name__ == "__main__":
    unittest.main()
