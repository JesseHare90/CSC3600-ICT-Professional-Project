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
python3 mdextract.py -r /Users/U1093772/Desktop/test -o out.csv
```

For non-recursive use we remove the -r optional argument:
```
python3 mdextract.py /Users/U1093772/Desktop/test -o out.csv
