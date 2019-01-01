# -*- coding: utf-8 -*-
import argparse
import os
from unittest import TestCase
import unittest
from mark_duplicates import MarkDuplicates, check_arguments


class TestMarkDuplicates(TestCase):

    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.normal_test_file = 'test.txt'
        self.empty_file = 'empty_test.txt'

    def tearDown(self):
        for file in os.listdir(self.path):
            if file.startswith('output'):
                os.remove(f'{self.path}/{file}')

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
        test = MarkDuplicates(1, self.normal_test_file, 4, verbose=False)
        test.open_file()
        output = test.read_text()
        self.assertEqual(len(output), 2)

    def test_get_list_of_paragraphs_empty_file(self):
        test = MarkDuplicates(1, self.empty_file, 4, verbose=False)
        test.open_file()
        output = test.read_text()
        self.assertEqual(len(output), 0)

    def test_create_output_file(self):
        test = MarkDuplicates(1, self.normal_test_file, 4, verbose=False)
        test.run()
        assert os.path.exists(f'{self.path}/output_{self.normal_test_file[:-4]}.html')


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)  # reraise an error


class TestArgParse(TestCase):
    """Tests that the Parse class works correctly"""

    def setUp(self):
        self.parser = ErrorRaisingArgumentParser()
        self.parser.add_argument(
            "-f", "--file", type=str,
            help="filename to proceed")
        self.parser.add_argument(
            "-w", "--word",
            type=int,
            default=4)

    def test_unrecognized_argument(self):
        args = ["-x", "xxx"]
        with self.assertRaises(ValueError) as cm:
            self.parser.parse_args(args)
        self.assertIn('unrecognized', str(cm.exception))

    def test_word_length_less_than_1(self):
        args = ["-f", "test.txt", "-w", "-5"]
        with self.assertRaises(ValueError) as cm:
            check_arguments(self.parser, self.parser.parse_args(args))
        self.assertIn('Word length must be at least 3', str(cm.exception))

    def test_wrong_filename(self):
        args = ["-f", "ssxxxxx.txt"]
        with self.assertRaises(ValueError) as cm:
            check_arguments(self.parser, self.parser.parse_args(args))
        self.assertIn('No such file or directory', str(cm.exception))


if __name__ == '__main__':
    unittest.main()
