from typing import Dict
import unittest
from dtmove.dtmove import filter_bases, find_bases


class TestFindBasePaths(unittest.TestCase):

    def test_1_simple(self):
        paths = [
            '/path/to/folder1',
            '/path/to/folder2',
            '/path/to/folder3'
        ]
        res = {
            '/path': [
                '/path/to'
            ],
            '/path/to': [
                '/path/to/folder1',
                '/path/to/folder2',
                '/path/to/folder3'
            ]
        }
        bases: Dict[str, list] = {}
        bases = find_bases(paths, bases)
        self.assertEqual(bases, res)

    def test_2_diffroot(self):
        paths = [
            '/path/to/folder1',
            '/path/to/folder2',
            '/path/to/folder3',
            '/path/to-another/folder1',
            '/path/to-another/folder2'
        ]
        res = {
            '/path': [
                '/path/to',
                '/path/to-another'
            ],
            '/path/to': [
                '/path/to/folder1',
                '/path/to/folder2',
                '/path/to/folder3'
            ],
            '/path/to-another': [
                '/path/to-another/folder1',
                '/path/to-another/folder2'
            ]
        }
        bases: Dict[str, list] = {}
        bases = find_bases(paths, bases)
        self.assertEqual(bases, res)

    def test_3_difflen(self):
        paths = [
            '/path/to/folder1',
            '/path/to/folder2',
            '/path/to/folder3',
            '/path/to/folder4/subfolder',
            '/path/to/folder5/subfolder'
        ]
        res = {
            '/path': [
                '/path/to'
            ],
            '/path/to': [
                '/path/to/folder1',
                '/path/to/folder2',
                '/path/to/folder3',
                '/path/to/folder4',
                '/path/to/folder5'
            ],
            '/path/to/folder4': [
                '/path/to/folder4/subfolder'
            ],
            '/path/to/folder5': [
                '/path/to/folder5/subfolder'
            ]
        }
        bases: Dict[str, list] = {}
        bases = find_bases(paths, bases)
        self.assertEqual(bases, res)

    def test_4_combined(self):
        paths = [
            '/path/to/folder1',
            '/path/to/folder2',
            '/path/to/folder3',
            '/a/path/to/folder',
            '/a/path/to_another/folder'
        ]
        res = {
            '/path': [
                '/path/to'
            ],
            '/path/to': [
                '/path/to/folder1',
                '/path/to/folder2',
                '/path/to/folder3'
            ],
            '/a': [
                '/a/path'
            ],
            '/a/path': [
                '/a/path/to',
                '/a/path/to_another'
            ],
            '/a/path/to': [
                '/a/path/to/folder'
            ],
            '/a/path/to_another': [
                '/a/path/to_another/folder'
            ]
        }
        bases: Dict[str, list] = {}
        bases = find_bases(paths, bases)
        self.assertEqual(bases, res)


class TestFilterBasePaths(unittest.TestCase):

    def test_1_filter(self):
        bases = {
            '/path': [
                '/path/to'
            ],
            '/path/to': [
                '/path/to/folder1',
                '/path/to/folder2',
                '/path/to/folder3',
                '/path/to/folder4',
                '/path/to/folder5'
            ],
            '/path/to/folder4': [
                '/path/to/folder4/subfolder'
            ],
            '/path/to/folder5': [
                '/path/to/folder5/subfolder'
            ]
        }
        res = {
            '/path/to': [
                '/path/to/folder1',
                '/path/to/folder2',
                '/path/to/folder3',
                '/path/to/folder4',
                '/path/to/folder5'
            ],
            '/path/to/folder4': [
                '/path/to/folder4/subfolder'
            ],
            '/path/to/folder5': [
                '/path/to/folder5/subfolder'
            ]
        }
        self.assertEqual(filter_bases(bases), res)


if __name__ == '__main__':
    unittest.main()
