# -*- coding: utf-8 -*-
import argparse
import os
from unittest import TestCase
import unittest
from mark_duplicates import MarkDuplicates

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'test.txt')
TESTDATA_EMPTY_FILE = os.path.join(os.path.dirname(__file__), 'empty_test.txt')


class TestMarkDuplicates(TestCase):

    def setUp(self):
        self.text = open(TESTDATA_FILENAME, encoding='utf-8')
        self.f = 'test.txt'
        self.empty_file = open(TESTDATA_EMPTY_FILE)

    def tearDown(self):
        self.text.close()

    def test_get_indices(self):
        sentences = ['My first sentence.', 'Next Sentences line 1.', 'My sentence.',
                     'My second next line sentence - line 2.', 'My second sentence.',
                     'My seconds next line sentence - line 2.']
        test = MarkDuplicates(1, 'test.txt', 4, verbose=False)
        x = test.get_indices('sentence', sentences, 1)
        self.assertEqual(x, [2, 3, 4, 5])

    def test_open_file(self):
        test = MarkDuplicates(1, 'test.txt', 4, verbose=False)
        output = test.open_file()
        expected = 'My first sentence. Next Sentences line 1.\nMy sentence. My second next line sentence - line 2.\nMy second sentence. My seconds next line sentence - line 2.\n\nDlaczego chiałbym być taki. Niedobry dlaczegol. dlaczego.'
        self.assertEqual(output, expected)

    def test_get_list_of_paragraphs_normal_file(self):
        test = MarkDuplicates(1, self.f, 4, verbose=False)
        test.open_file()
        output = test.read_text()
        print(output)
        self.assertEqual(len(output), 2)

    def test_get_list_of_paragraphs_empty_file(self):
        test = MarkDuplicates(1, 'empty_test.txt', 4, verbose=False)
        test.open_file()
        output = test.read_text()
        print(output)
        self.assertEqual(len(output), 0)


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)  # reraise an error


class TestArgParse(TestCase):
    """Tests that the Parse class works correctly"""

    def setUp(self):
        self.parser = ErrorRaisingArgumentParser()
        self.parser.add_argument(
            "file", type=str,
            help="filename to proceed")
        self.parser.add_argument(
            "-w", "--word",
            type=int,
            default=4, )

    def test_unrecognized_argument(self):
        args = ["-x", "xxx"]
        with self.assertRaises(ValueError) as cm:
            self.parser.parse_args(args)
        print('msg:', cm.exception)
        self.assertIn('unrecognized', str(cm.exception))

    # def test_wrong_filename(self):
    #     args = ["ssxxxxx"]
    #     with self.assertRaises(FileNotFoundError) as cm:
    #         self.parser.parse_args(args)
    #     print('msg:', cm.exception)
    #     self.assertIn('unrecognized', str(cm.exception))


if __name__ == '__main__':
    unittest.main()
