from typing import Dict
import unittest
from dtmove.dtmove import filter_bases, find_bases


class TestFindBasePaths(unittest.TestCase):

    def test_1_simple(self):
        paths = [
            'E:\\path\\to\\folder1',
            'E:\\path\\to\\folder2',
            'E:\\path\\to\\folder3'
        ]
        res = {
            'E:': [
                'E:\\path'
            ],
            'E:\\path': [
                'E:\\path\\to'
            ],
            'E:\\path\\to': [
                'E:\\path\\to\\folder1',
                'E:\\path\\to\\folder2',
                'E:\\path\\to\\folder3'
            ]
        }
        bases: Dict[str, list] = {}
        bases = find_bases(paths, bases)
        self.assertEqual(bases, res)

    def test_2_diffroot(self):
        paths = [
            'E:\\path\\to\\folder1',
            'E:\\path\\to\\folder2',
            'E:\\path\\to\\folder3',
            'F:\\a\\path\\to',
            'F:\\a\\path\\to_another'
        ]
        res = {
            'E:': [
                'E:\\path'
            ],
            'E:\\path': [
                'E:\\path\\to'
            ],
            'E:\\path\\to': [
                'E:\\path\\to\\folder1',
                'E:\\path\\to\\folder2',
                'E:\\path\\to\\folder3'
            ],
            'F:': [
                'F:\\a'
            ],
            'F:\\a': [
                'F:\\a\\path'
            ],
            'F:\\a\\path': [
                'F:\\a\\path\\to',
                'F:\\a\\path\\to_another'
            ]
        }
        bases: Dict[str, list] = {}
        bases = find_bases(paths, bases)
        self.assertEqual(bases, res)

    def test_3_difflen(self):
        paths = [
            'E:\\path\\to\\folder1',
            'E:\\path\\to\\folder2',
            'E:\\path\\to\\folder3',
            'E:\\path\\to\\folder4\\subfolder',
            'E:\\path\\to\\folder5\\subfolder'
        ]
        res = {
            'E:': [
                'E:\\path'
            ],
            'E:\\path': [
                'E:\\path\\to'
            ],
            'E:\\path\\to': [
                'E:\\path\\to\\folder1',
                'E:\\path\\to\\folder2',
                'E:\\path\\to\\folder3',
                'E:\\path\\to\\folder4',
                'E:\\path\\to\\folder5'
            ],
            'E:\\path\\to\\folder4': [
                'E:\\path\\to\\folder4\\subfolder'
            ],
            'E:\\path\\to\\folder5': [
                'E:\\path\\to\\folder5\\subfolder'
            ]
        }
        bases: Dict[str, list] = {}
        bases = find_bases(paths, bases)
        self.assertEqual(bases, res)

    def test_4_combined(self):
        paths = [
            'E:\\path\\to\\folder1',
            'E:\\path\\to\\folder2',
            'E:\\path\\to\\folder3',
            'F:\\a\\path\\to\\folder1',
            'F:\\a\\path\\to_another\\folder1'
        ]
        res = {
            'E:': [
                'E:\\path'
            ],
            'E:\\path': [
                'E:\\path\\to'
            ],
            'E:\\path\\to': [
                'E:\\path\\to\\folder1',
                'E:\\path\\to\\folder2',
                'E:\\path\\to\\folder3'
            ],
            'F:': [
                'F:\\a'
            ],
            'F:\\a': [
                'F:\\a\\path'
            ],
            'F:\\a\\path': [
                'F:\\a\\path\\to',
                'F:\\a\\path\\to_another'
            ],
            'F:\\a\\path\\to': [
                'F:\\a\\path\\to\\folder1'
            ],
            'F:\\a\\path\\to_another': [
                'F:\\a\\path\\to_another\\folder1'
            ]
        }
        bases: Dict[str, list] = {}
        bases = find_bases(paths, bases)
        self.assertEqual(bases, res)


class TestFilterBasePaths(unittest.TestCase):

    def test_1_filter(self):
        bases = {
            'E:': [
                'E:\\path'
            ],
            'E:\\path': [
                'E:\\path\\to'
            ],
            'E:\\path\\to': [
                'E:\\path\\to\\folder1',
                'E:\\path\\to\\folder2',
                'E:\\path\\to\\folder3'
            ],
            'F:': [
                'F:\\a'
            ],
            'F:\\a': [
                'F:\\a\\path'
            ],
            'F:\\a\\path': [
                'F:\\a\\path\\to',
                'F:\\a\\path\\to_another'
            ],
            'F:\\a\\path\\to': [
                'F:\\a\\path\\to\\folder1'
            ],
            'F:\\a\\path\\to_another': [
                'F:\\a\\path\\to_another\\folder1'
            ]
        }
        res = {
            'E:\\path\\to': [
                'E:\\path\\to\\folder1',
                'E:\\path\\to\\folder2',
                'E:\\path\\to\\folder3'
            ],
            'F:\\a\\path': [
                'F:\\a\\path\\to',
                'F:\\a\\path\\to_another'
            ],
            'F:\\a\\path\\to': [
                'F:\\a\\path\\to\\folder1'
            ],
            'F:\\a\\path\\to_another': [
                'F:\\a\\path\\to_another\\folder1'
            ]
        }
        self.assertEqual(filter_bases(bases), res)


if __name__ == '__main__':
    unittest.main()
