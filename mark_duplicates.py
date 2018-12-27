# -*- coding: utf-8 -*-

import argparse
import sys
import os.path

import nltk.data
from nltk.tokenize import sent_tokenize, blankline_tokenize, word_tokenize
from colorama import init, Style, Fore


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f'{Fore.RED}error: %s\n{Style.RESET_ALL}' % message)
        print(50 * '*')
        self.print_help()
        sys.exit(2)


def parse_arguments(parser):
    # Parse command line arguments

    parser.add_argument("-f", "--file", type=str,
                        help="filename to proceed")
    parser.add_argument("-s", "--space", type=int, default=1,
                        help="space between occurrences of words <INT, default=1>")
    parser.add_argument("-w", "--word", type=int, default=4,
                        help="length of words to check <INT, default=4>")
    parser.add_argument("-v", "--verbose", action="store_true", help="print output to terminal")
    arguments = parser.parse_args()
    return arguments


def check_arguments(parser, args):
    if args.file[-4:] != '.txt':
        parser.error(message='Not valid .txt file. Program accepts only .txt files.')
    if not os.path.exists(args.file):
        parser.error(message=f'No such file or directory: {args.file}')
    if args.word < 2:
        parser.error(message=f'Word length must be at least 1.')


class MarkDuplicates:

    def __init__(self, space, filename, length, verbose=False):
        self.filename = filename
        self.text = ''
        self.space = space
        self.word_length = length
        self.verbose = verbose
        self.verbose_mode_paragraph = ''
        self.marked_paragraph = ''
        self.paragraph_nr = 0
        self.marked_words = 0
        self.marked_text = ''
        self.verbose_mode_output = ''

    @staticmethod
    def get_indices(word, sentences, space):
        indices = []
        for i, elem in enumerate(sentences):
            for w in word_tokenize(elem):
                if w.lower() == word.lower():
                    indices.append(i)
        spaced_indices = []
        for i in range(1, len(indices)):
            if indices[i] - indices[i - 1] <= space:
                if indices[i - 1] not in spaced_indices:
                    spaced_indices.append(indices[i - 1])
                if indices[i] not in spaced_indices:
                    spaced_indices.append(indices[i])
        return spaced_indices

    def run(self):
        self.open_file()
        self.read_text()
        if len(self.marked_text) > 0:
            self.write_to_file()
        self.final_output_message()
        if self.verbose:
            print(self.verbose_mode_output)

    def open_file(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            self.text = file.read()
            return self.text

    def read_text(self):
        list_of_paragraphs = blankline_tokenize(self.text)
        self.read_paragraphs(list_of_paragraphs)
        return list_of_paragraphs

    def read_paragraphs(self, list_of_paragraphs):
        for paragraph in list_of_paragraphs:
            self.verbose_mode_paragraph = ''
            self.marked_paragraph = ''
            self.paragraph_nr += 1
            self.sentences = sent_tokenize(paragraph)
            self.read_sentences()
            self.marked_text += f'PARAGRAPH {self.paragraph_nr} <br><br>{self.marked_paragraph}<br><br>'
            self.verbose_mode_output += f'PARAGRAPH {self.paragraph_nr} \n\n{self.verbose_mode_paragraph}\n\n'

    def read_sentences(self):
        for ind in range(len(self.sentences)):
            self.sentence = self.sentences[ind]
            self.ind = ind
            self.read_single_sentence()

    def read_single_sentence(self):
        for word in word_tokenize(self.sentence):
            self.check_duplicates(word)

    def check_duplicates(self, word):
        if len(word) > self.word_length:
            spaced_indices = self.get_indices(word, self.sentences, self.space)
            if self.ind in spaced_indices:
                self.mark_duplicates_in_paragraph(word)
            else:
                self.add_normal_text_to_output(word)
        else:
            self.add_normal_text_to_output(word)

    def mark_duplicates_in_paragraph(self, word):
        html_start = "<span style='color:red; text-decoration:underline'>"
        html_stop = "</span>"
        self.marked_paragraph += f'{html_start} {word}{html_stop}'
        self.marked_words += 1
        if self.verbose:
            self.verbose_mode_paragraph += f'{Fore.GREEN} {word}{Style.RESET_ALL}'

    def add_normal_text_to_output(self, word):
        if word not in ['.', ','] and len(self.marked_paragraph) > 0:
            self.marked_paragraph += f' {word}'
            if self.verbose:
                self.verbose_mode_paragraph += f' {word}'
        else:
            self.marked_paragraph += f'{word}'
            if self.verbose:
                self.verbose_mode_paragraph += f'{word}'

    def write_to_file(self):
        with open(f"output_{os.path.splitext(self.filename)[0]}.html", 'w+', encoding='utf-8') as file:
            file.write(f'{self.marked_text}')

    def final_output_message(self):
        print(55 * '*')
        print(f'{Fore.GREEN}{self.marked_words}{Style.RESET_ALL} words was marked as duplicates')
        if len(self.marked_text) > 0:
            print(
                f'Your output file : {Fore.GREEN}output_{os.path.splitext(self.filename)[0]}.html{Style.RESET_ALL}')
            print(55 * '*')


if __name__ == "__main__":
    init(autoreset=True)
    nltk.download('punkt', quiet=True)
    my_parser = MyParser()
    args = parse_arguments(my_parser)
    check_arguments(my_parser, args)
    main = MarkDuplicates(args.space, args.file, args.word, args.verbose)
    main.run()
