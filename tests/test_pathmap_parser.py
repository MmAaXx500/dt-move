from typing import Dict
import unittest
from dtmove.dtmove import parse_pathmap


class TestPathmapPerser(unittest.TestCase):

    def test_pathmap_parser(self):
        pathmap = [
            "# This is a comment",
            "",
            "/the/old/folder /> /the/new/folder",
            "/folder/with space /> /new/folder/with space",
            "this /> is /> an /> invalid /> line"
        ]

        basepaths = {
            "/the/old/folder": [
                "/the/old/folder/subfolder"
            ],
            "/folder/with space": [
                "/folder/with space/subfolder"
            ],
            "/the/plus/path": [
                "/the/plus/path/subfolder"
            ]
        }
        rewritemap: Dict[str, str] = {}
        parse_pathmap(pathmap, basepaths, rewritemap)
        expected_basepaths = {
            "/the/plus/path": [
                "/the/plus/path/subfolder"
            ]
        }
        expected_rewritemap = {
            "/the/old/folder": "/the/new/folder",
            "/folder/with space": "/new/folder/with space"
        }
        self.assertEqual(basepaths, expected_basepaths)
        self.assertEqual(rewritemap, expected_rewritemap)


if __name__ == '__main__':
    unittest.main()
