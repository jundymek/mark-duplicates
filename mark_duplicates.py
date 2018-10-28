# -*- coding: utf-8 -*-
import getopt
import sys
import os.path
import nltk.data
from nltk.tokenize import sent_tokenize, blankline_tokenize, word_tokenize
from colorama import init, Style, Fore


def usage():
    print(f'Usage: {sys.argv[0]} [-s: <INT> -f <STR>]')
    print('Options:')
    print('     -h, --help           Show help.')
    print('     -s, --space          Set spacing between occurrences of words.')
    print('     -f, --file           Set filename to process.')


def main():
    space = 2
    file = 'test.txt'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:f:", ["help", "file"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        print(opt)
        if opt in ("-s", "--space"):
            try:
                space = int(arg)
            except ValueError:
                usage()
                sys.exit(2)
        elif opt in ("-f", "--file"):
            if os.path.exists(arg):
                file = arg
            else:
                sys.exit(f'No such file or directory: {arg}')
        else:
            usage()
            sys.exit(0)
    with open(file, 'r', encoding='utf-8') as file:
        text1 = MarkDuplicates(file, space)
    text1.mark_duplicates()


class MarkDuplicates:

    def __init__(self, file, space):
        self.text = file.read()
        self.space = space

    def mark_duplicates(self):
        marked_text = ''
        par_nr = 0
        for paragraph in blankline_tokenize(self.text):
            par_nr += 1
            marked_paragraph = ''
            sentences = sent_tokenize(paragraph)
            temp = {}
            for index, word in enumerate(word_tokenize(paragraph)):
                for i, s in enumerate(sentences):
                    if word in temp:
                        if (temp[word] - 2 > 0 and len(word) > 5) or word.lower() in sentences[i - 2].lower():
                            last = marked_paragraph.lower().rfind(word)
                            marked_paragraph = marked_paragraph.replace(marked_paragraph[last:last + len(word)],
                                                                        f'{Fore.GREEN}' +
                                                                        f'{marked_paragraph[last:last + len(word)]}' +
                                                                        f'{Style.RESET_ALL}', 1)
                            marked_paragraph += f' {Fore.GREEN}{word}{Style.RESET_ALL}'
                            break
                        else:
                            temp[word.lower()] = index
                            marked_paragraph += f' {word}'
                            break
                    else:
                        if len(word) > 5:
                            temp[word.lower()] = index
                        if word not in ['.', ','] and len(marked_paragraph) > 0:
                            marked_paragraph += f' {word}'
                        else:
                            marked_paragraph += f'{word}'
                        break
            print(f'PARAGRAPH {par_nr} \n\n{marked_paragraph}\n')
        return marked_text


if __name__ == "__main__":
    init(autoreset=True)
    nltk.download('punkt', quiet=True)
    main()
