# mark-duplicates

Simple python script to mark duplicates in a text file. It is a tool for writers that was inspired by [Marta](https://github.com/martapotocka)


## Features

  - Examines indicated file (.txt files are allowed)
  - Marks words which are repeated in neighboring sentences
  - You can specify the length of words to check (eg. do not check words like but, with, me etc.)
  - You can specify the distance between sentences
  - the program creates an output .html file with marked words considered as duplicates


## Usage
```
USAGE
  mark_duplicates.py [-h] [-s SPACE] [-w WORD] [-v] file
  
POSITIONAL ARGUMENTS
  file                      filename to proceed <STR, .txt file>

OPTIONAL ARGUMENTS
  -h, --help                show this help message and exit
  -s SPACE, --space SPACE   set space between occurrences of words <INT, default=1>
  -w WORD, --word WORD      length of words to check <INT, default=4>
  -v, --verbose             print output into terminal

```

License
----

MIT


**Free Software!**