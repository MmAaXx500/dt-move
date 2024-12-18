import unittest
from dtmove.dtmove import filter_bases


class TestFilterBases(unittest.TestCase):
    def test_filterbases_simple(self):
        basepaths = {
            "C:\\the": ["C:\\the\\old"],
            "C:\\the\\old": ["C:\\the\\old\\folder", "C:\\the\\old\\folder2"],
            "C:\\the\\old\\folder": [
                "C:\\the\\old\\folder\\a",
                "C:\\the\\old\\folder\\b",
            ],
        }

        basepaths_filtered = filter_bases(basepaths)

        expected_basepaths = {
            "C:\\the\\old": ["C:\\the\\old\\folder", "C:\\the\\old\\folder2"],
            "C:\\the\\old\\folder": [
                "C:\\the\\old\\folder\\a",
                "C:\\the\\old\\folder\\b",
            ],
        }
        self.assertEqual(basepaths_filtered, expected_basepaths)

    def test_filterbases_single(self):
        basepaths = {
            "C:\\the": ["C:\\the\\old"],
            "C:\\the\\old": ["C:\\the\\old\\folder"],
            "C:\\the\\old\\folder": ["C:\\the\\old\\folder\\a"],
        }

        basepaths_filtered = filter_bases(basepaths)

        expected_basepaths = {
            "C:\\the\\old\\folder": ["C:\\the\\old\\folder\\a"],
        }
        self.assertEqual(basepaths_filtered, expected_basepaths)

    def test_filterbases_nested_singlebranch(self):
        basepaths = {
            "C:\\the": ["C:\\the\\old1", "C:\\the\\old2"],
            "C:\\the\\old1": ["C:\\the\\old1\\folder"],
            "C:\\the\\old2": ["C:\\the\\old2\\folder"],
            "C:\\the\\old1\\folder": ["C:\\the\\old1\\folder\\a"],
        }

        basepaths_filtered = filter_bases(basepaths)

        expected_basepaths = {
            "C:\\the": ["C:\\the\\old1", "C:\\the\\old2"],
            "C:\\the\\old1": ["C:\\the\\old1\\folder"],
            "C:\\the\\old2": ["C:\\the\\old2\\folder"],
            "C:\\the\\old1\\folder": ["C:\\the\\old1\\folder\\a"],
        }
        self.assertEqual(basepaths_filtered, expected_basepaths)


if __name__ == "__main__":
    unittest.main()
