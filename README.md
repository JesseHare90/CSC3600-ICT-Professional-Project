# CSC3600 ICT Professional Project

**Supervisor:** A/Prof Stijn Dekeyser

**Contact:** stijn.dekeyser@usq.edu.au

**Language:** Python3

**Platform:** Linux, Windows, MacOS

**Synopsis:** The aim of the project is two-fold

1. develop a CLI script that takes a directory path as input, and returns a CSV-formatted text having one like per file in the directory, and listing all metadata attributes and values extracted from that file.
2. develop a GUI that reads the above CSV file and displays a spreadsheet-like grid, where rows can be sorted and filtered on attribute values, files can be searched for on multiple criteria, and double-clicking a file-row opens it.

## Group

**Jesse Hare**        - W0070949@umail.usq.edu.au\
**James McKeown**     - U1093772@umail.usq.edu.au\
**Ryan Sharp**        - U1090072@umail.usq.edu.au\
**Richard Dobson**    - U1011744@umail.usq.edu.au\
**Vincent Robertski** - U1046454@umail.usq.edu.au\

## Installation

**NOTE**: Python 3.6 or higher is required.

```bash
# clone the repo
$ git clone https://github.com/JesseHare90/CSC3600-ICT-Professional-Project

# change the working directory to project
$ cd CSC3600-ICT-Professional-Project

# install python3 and python3-pip if they are not installed

# install the requirements
$ python3 -m pip install -r requirements.txt
```
## Usage

```bash
$ python3 mdextract.py --help
usage: mdextract.py [-h] [-r] [-o] file_path output_file

File metadata harvester and searcher

positional arguments:
  file_path        Input file path to be indexed
  output_file      Output CSV file

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  allows program to recursively traverse through folders
  -o               Token to signify output to subsequent csv file


```

For example to search the folder "test" recursively and output to out.csv:
```
python3 mdextracy.py -r /Users/U1093772/Desktop/test -o out.csv
```

For non-recursive use we remove the -r optional argument:
```
python3 mdextracy.py /Users/U1093772/Desktop/test -o out.csv
```
