# -*- coding: utf-8 -*-

import argparse
import sys
import os.path

import nltk.data
from nltk.tokenize import sent_tokenize, blankline_tokenize, word_tokenize
from colorama import init, Style, Fore


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def parse_arguments():
    # Parse command line arguments
    parser = MyParser()
    parser.add_argument("file", type=str,
                        help="filename to proceed")
    parser.add_argument("-s", "--space", type=int, default=1,
                        help="space between occurrences of words <INT, default=1>")
    parser.add_argument("-w", "--word", type=int, default=4,
                        help="length of words to check <INT, default=4>")
    parser.add_argument("-v", "--verbose", action="store_true", help="print output to terminal")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    space = args.space
    if os.path.exists(args.file):
        filename = args.file
    else:
        print(f'No such file or directory: {args.file}')
        parser.print_help(sys.stderr)
        sys.exit(1)

    # open file and mark duplicates
    with open(filename, 'r', encoding='utf-8') as file:
        result = MarkDuplicates(file, space, filename, args.word, args.verbose)
    result.mark_duplicates()


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


class MarkDuplicates:

    def __init__(self, file, space, filename, length, verbose):
        self.filename = filename
        self.text = file.read()
        self.space = space
        self.word = length
        self.verbose = verbose

    def mark_duplicates(self):
        marked_text = ''
        verbose_mode_output = ''
        par_nr = 0
        html_start = "<span style='color:red; text-decoration:underline'>"
        html_stop = "</span>"
        marked_words = 0
        for paragraph in blankline_tokenize(self.text):
            par_nr += 1
            marked_paragraph = ''
            verbose_mode_paragraph = ''
            sentences = sent_tokenize(paragraph)
            for ind in range(len(sentences)):
                for word in word_tokenize(sentences[ind]):
                    if len(word) > self.word:
                        spaced_indices = get_indices(word, sentences, self.space)
                        if ind in spaced_indices:
                            marked_paragraph += f'{html_start} {word}{html_stop}'
                            if self.verbose:
                                verbose_mode_paragraph += f'{Fore.GREEN} {word}{Style.RESET_ALL}'
                            marked_words += 1
                        else:
                            if word not in ['.', ','] and len(marked_paragraph) > 0:
                                marked_paragraph += f' {word}'
                                if self.verbose:
                                    verbose_mode_paragraph += f' {word}'
                            else:
                                marked_paragraph += f'{word}'
                                if self.verbose:
                                    verbose_mode_paragraph += f'{word}'
                    else:
                        if word not in ['.', ','] and len(marked_paragraph) > 0:
                            marked_paragraph += f' {word}'
                            if self.verbose:
                                verbose_mode_paragraph += f' {word}'
                        else:
                            marked_paragraph += f'{word}'
                            if self.verbose:
                                verbose_mode_paragraph += f'{word}'
            marked_text += f'PARAGRAPH {par_nr} <br><br>{marked_paragraph}<br><br>'
            verbose_mode_output += f'PARAGRAPH {par_nr} \n\n{verbose_mode_paragraph}\n\n'
            if self.verbose:
                print(verbose_mode_output)

        with open(f"output_{os.path.splitext(self.filename)[0]}.html", 'w+', encoding='utf-8') as files:
            files.write(f'{marked_text}')
        print(55*'*')
        print(f'{Fore.GREEN}{marked_words}{Style.RESET_ALL} words was marked as duplicates')
        print(
            f'Your output file : {Fore.GREEN}output_{os.path.splitext(self.filename)[0]}.html{Style.RESET_ALL}')
        print(55*'*')


if __name__ == "__main__":
    init(autoreset=True)
    nltk.download('punkt', quiet=True)
    parse_arguments()
