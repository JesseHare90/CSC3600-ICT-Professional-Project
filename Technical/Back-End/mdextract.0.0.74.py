#! /usr/bin/env python3

# import required os module to gain access to os.walk functionality
import os
# import required sys module for argument functionality
import sys
# import required subprocess module for program capture within console
import subprocess
# import required argparse module for smart argument parsing functionality
import argparse
# import required CSV module for formating output
import csv

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument



# Students
# Jesse Hare        - W0070949@umail.usq.edu.au
# James McKeown     - U1093772@umail.usq.edu.au
# Ryan Sharp        - U1090072@umail.usq.edu.au
# Richard Dobson    - U1011744@umail.usq.edu.au
# Vincent Robertski - U1046454@umail.usq.edu.au

# Backend program developed by James and Richard
# Frontend program developed by Jesse, Ryan

# ======================
# TODO list
# ======================

# TODO: Find out how to use > symbol in command line arguments
# TODO: Data structure for storing metadata before output to CSV
# TODO: Use Pyexiftool wrapper to scrape metadata
# TODO: CSV output function

# ======================
# Variable declarations
# ======================

module_name = "File metadata harvester and searcher"
team_name = "The USQ Learning Emporium"
__version__ = "0.0.5"
global_array = []

# ======================
# Function declarations
# ======================

# ----------------------------------------------------------------
# Traverses all directories and files recursively
# @param path - filename path passed in from command line argument
# @return array of paths
# ----------------------------------------------------------------
def recursive(path):
    for root, dirs, files in os.walk(path):
        for index in files:
            global_array.append(os.path.join(root, index))
    return global_array

# ----------------------------------------------------------------
# Traverses all directories and files non-recursively
# @param path - filename path passed in from command line argument
# @return array of paths
# ----------------------------------------------------------------
def non_recursive(path):
    folders = []
    files = []

    for entry in os.scandir(path):
        if entry.is_dir():
            folders.append(entry.path)
        elif entry.is_file():
            files.append(entry.path)
    for count in range(0, len(folders)):
        global_array.append(folders[count])
    for count in range(0, len(files)):
        global_array.append(files[count])

# ----------------------------------------------------------------
# Outputs metadata into CSV
# @param output_csv - filename of the csv
# @param global_array - array with stored metadata
# @return N/A
# ----------------------------------------------------------------
def csv_output(output_csv, global_array):
    # Open/create the CSV file with writeable attributes
    with open(output_csv, mode='w') as output:
        # Create a writer object and set csv delimiter
        output_writer = csv.writer(output, delimiter='\n', quoting=csv.QUOTE_MINIMAL)
        metadata = global_array
        # Use writerow method function to add rows to csv file
        #for count in range(0, len(metadata)):
        output_writer.writerows([metadata])

# ----------------------------------------------------------------
# Populates array with metadata
# @param path - filename path passed in from command line argument
# @return N/A
# ----------------------------------------------------------------
def populate(input_file):
    if "pdf" in input_file:
        fp = open(input_file, 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        parser.set_document(doc)
        doc.set_parser(parser)
        if len(doc.info) > 0:
            info = doc.info[0]
            return(info)
    elif "py" in input_file:
        process = subprocess.Popen(["stat", input_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        metadata = []
        for output in process.stdout:
            info = {}
            line = output.replace("- ", "").strip().split(":")
            info[line[0].strip()] = line[1].strip()
            metadata.append(info)
        return metadata
    elif "txt" in input_file:
        process = subprocess.Popen(["stat", input_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        metadata = []
        for output in process.stdout:
            info = {}
            line = output.replace("- ", "").strip().split(":")
            info[line[0].strip()] = line[1].strip()
            metadata.append(info)
        return metadata
    else:
        scraper = "hachoir-metadata"
        process = subprocess.Popen([scraper, input_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        metadata = []
        for output in process.stdout:
            info = {}
            line = output.replace("- ", "").strip().split(":")
            info[line[0].strip()] = line[1].strip()
            metadata.append(info)
        return metadata

# =============
# Control Flow                                           
# =============

def main():
    # -------------------------------
    # Phase 1 - Information Gathering
    # -------------------------------

    # Initialise argument parsing functionality
    parser = argparse.ArgumentParser(description='File metadata harvester and searcher')
    # Add the recursive option
    parser.add_argument('-r', '--recursive', action='store_true', help='allows program to recursively traverse through folders')
    # Add the file path option
    parser.add_argument('file_path', help='Input file path to be indexed')
    # Add the output file path token ">"
    parser.add_argument('-o', action='store_true', help='Token to signify output to subsequent csv file') # TODO: Need to figure out how to use > ... causes errors
    # Add the output csv file name
    parser.add_argument('output_file', help='Output CSV file')
    # Parse any given arguments
    args = parser.parse_args()
    # Checks if the supplied argument is a valid file path
    if not (os.path.isdir(args.file_path)):
        print("Invalid File Path")
        return
    if args.recursive:
        # if -r option is used call the recursive function
        recursive(args.file_path)
    if args.file_path and not args.recursive:
        # if no -r option is used call the non_recursive function
        non_recursive(args.file_path)

    # ---------------------------
    # Phase 2 - Metadata Scraping
    # ---------------------------
    test_var = []
    itr = 0
    for f in global_array:
        test_var.append(populate(f))

    # ------------------------
    # Phase 3 - Pushing output
    # ------------------------
    super_global_array = zip(global_array,test_var)
    # Call the output function
    csv_output(args.output_file, super_global_array)

# Main control flow of program is started here, first function called is main
if __name__ == '__main__':
    main()
