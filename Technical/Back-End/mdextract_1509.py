
#! /usr/bin/env python3

# import required os module to gain access to os.walk functionality
import os
# import required sys module for argument functionality
import sys
# import required argparse module for smart argument parsing functionality
import argparse
# import required CSV module for formating output
import csv

# Students
# Jesse Hare        - W0070949@umail.usq.edu.au
# James McKeown     - U1093772@umail.usq.edu.au
# Ryan Sharp        - U1090072@umail.usq.edu.au
# Richard Dobson    - U1011744@umail.usq.edu.au
# Vincent Robertski - U1046454@umail.usq.edu.au

# Backend program developed by James and Richard
# Frontend program developed by Jesse, Ryan and Vincent

# TODO: Input verification
# TODO: Command line argument number verification (EG: No more than 3 args)
# TODO: Data structure for storing metadata before output to CSV
# TODO: Hachoir-metadata class to scrape metadata from files found with os.walk
# TODO: CSV output function

module_name = "File metadata harvester and searcher"
team_name = "The USQ Learning Emporium"
__version__ = "0.0.1"

# ======================
# Function declarations
# ======================

# ----------------------------------------------------------------
# Traverses all directories and files recursively
# @param path - filename path passed in from command line argument
# @return N/A
# ----------------------------------------------------------------
def recursive(path):
    # set the directory to begin from
    #root = path
    #for root, dirs, files in os.walk(root):
    #    print('Found directory: %s' % root)
    #    for fname in files:
    #        print('\t%s' % fname)
    for root, dirs, files in os.walk(path):
        for index in files:
            print(os.path.join(root, index))


# ----------------------------------------------------------------
# Traverses all directories and files non-recursively
# @param path - filename path passed in from command line argument
# @return N/A
# ----------------------------------------------------------------
def non_recursive(path):
    # set the directory to begin from
    #root = path
    # required to keep dirs and files as there could be both inside a root directory instead of just in subfolders etc...
    #for root, dirs, files in os.walk(root):
        #print(root)
        #for dir in dirs:
            #print(os.path.join(root, dir))
    folders = []
    files = []

    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                folders.append(entry.path)
            elif entry.is_file():
                files.append(entry.path)
        for count in range(0, len(folders)):
            print(folders[count])
        for count in range(0, len(files)):
            print(files[count])

# ----------------------------------------------------------------
# Outputs metadata into CSV
# @param path -
# @param path -
# @param path -
# @return N/A
# ----------------------------------------------------------------
#def csv_output(csv_file, csv_columns, data):
#    try:
#        with open(csv_file, 'w') as csvfile:
#            writer = csv.DictWriter(csvfile, fielfnames=csv_columns)
#            writer.writeheader()
#            for data in dict_data:
#                writer.writerow(data)
#    except IOError as (errno, strerror):
#        print("I/O error({0}): {1}".format(errno, strerror))
#    return

#-------------------------------------------------------------------
# Validates file_path user input as valid string
# @param path - filename path passed in from command line argument 
# @return N/A 
# ------------------------------------------------------------------



# =============
# Control Flow
# =============

def main():
    # Initialise argument parsing functionality
    parser = argparse.ArgumentParser()
    # Add the recursive option
    parser.add_argument('-r', '--recursive', action='store_true', help="allows program to recursively traverse through folders")
    # Add the file path option
    parser.add_argument('file_path') # TODO: Add file path sanitisation/verification EG: No illegal characters
    # Parse any given arguments
    args = parser.parse_args()
    if not (os.path.isdir(args.file_path)):
        print("Invalid File Path")
        return
    if args.recursive:
        # if -r option is used call the recursive function
        recursive(args.file_path)
    if args.file_path:
        # if no -r option is used call the non_recursive function
        non_recursive(args.file_path)

# Main control flow of program is started here, first function called is main
if __name__ == '__main__':
    main()
