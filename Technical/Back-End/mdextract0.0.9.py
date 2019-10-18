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
# import python magic module to provide filetype recognition functionality
import magic
# import re module to use regex
from PyPDF2 import PdfFileReader

from datetime import datetime

from pwd import getpwuid
# Students
# Jesse Hare        - W0070949@umail.usq.edu.au
# James McKeown     - U1093772@umail.usq.edu.au
# Ryan Sharp        - U1090072@umail.usq.edu.au
# Richard Dobson    - U1011744@umail.usq.edu.au
# Vincent Robertski - U1046454@umail.usq.edu.au

# Backend program developed by James, Vincent and Richard
# Frontend program developed by Jesse, Ryan

# ======================
# TODO list
# ======================

# TODO: Find out how to use > symbol in command line arguments
# TODO: Find better names for variables
# TODO: Find out how to discern file types pyhonically
# TODO: Rewrite populate function - please review and add your ideas
# TODO: Use strip() to take tab out of metadata output -

# ======================
# Variable declarations
# ======================

module_name = "File metadata harvester and searcher"
team_name = "The USQ Learning Emporium"
__version__ = "0.0.8"
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
        output_writer.writerows([metadata])


# ----------------------------------------------------------------
# Extracst file metadata using hachoir module, PyPDF2 moduel, or os module, depending on filetype
# @param path - filename path passed in from command line argument
# @return a dictionary of key:value pairs containing the file metadata
# ----------------------------------------------------------------
def populate(input_file):
    hachoir_compatibile_files = ['bzip2','cab','gzip','mar','tar','zip','aiff','mpeg','real_audio','sun_next_snd','matroska','ogg','real_media','riff','bmp','gif','ico','jpeg','pcx','png','psd','targa','tiff','wmf','xcf','ole2','pcf','torrent','ttf','exe','asf','flv','mov']
    if os.path.isdir(input_file):
        return 0    
    file_type = magic.from_file(input_file, mime=True)
    head, sep, file_ext = file_type.partition('/')
    # print(file_ext)    # used for testing
    if file_ext in hachoir_compatibile_files:
        scraper = "hachoir-metadata"
        process = subprocess.Popen([scraper, input_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        metadata = []
        for output in process.stdout:
            info = {}
            line = output.replace("- ", "").strip().split(":")
            info[line[0].strip()] = line[1].strip()
            metadata.append(info)
        return metadata
    elif file_ext == "pdf":
        fp = open(input_file, 'rb')
        pdf = PdfFileReader(fp)
        info = pdf.getDocumentInfo()
        # num_pages = pdf.getNumPages()
        # print(num_pages)
        return(info)
    elif file_ext == "x-python" or "plain":
        process = subprocess.Popen(["stat", input_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        metadata = []
        for output in process.stdout:
            info = {}
            line = output.replace("- ", "").strip().split(":")
            info[line[0].strip()] = line[1].strip()
            metadata.append(info)
        return metadata
    else:
        return 0

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
    # itr = 0
    for f in global_array:
        test_var.append(populate(f))

    # ------------------------
    # Phase 3 - Pushing output
    # ------------------------
    #super_global_array = zip(global_array,test_var)
    # Call the output function
    #csv_output(args.output_file, super_global_array)
    #print(len(global_array))
    #print(len(test_var))
    records = []
    
    for index, line in enumerate(test_var):
        fileStr = ""
        fileType = global_array[index].split(".")
        fileType = fileType[-1]
        #print("**************",fileType,"****************")
        fileStr = global_array[index]+","
        #print(global_array[index])
        #print(line)
        #if line is an int (not list of dicts, skip it)
        if isinstance(line,int):
            continue
        #else, we want to go through each dict in list, get keys and values, then append to fileStr, then finally records
        else:
            # we will come across some crappy data again, so we need to watch out
            #print(line)
            #print(len(line))
            if fileType != 'pdf':
                badKeys = ['Access','Modify','Change','Birth','Device','Size','Metadata','File','Audio','Common']
                fileStat = os.stat(global_array[index])
                accTime = datetime.fromtimestamp(fileStat.st_atime).strftime("%D %I:%M:%S")
                modTime = datetime.fromtimestamp(fileStat.st_mtime).strftime("%D %I:%M:%S")
                owner = getpwuid(os.stat(global_array[index]).st_uid).pw_name
                size = os.path.getsize(global_array[index])
                fType = fileType
                fileStr = fileStr+"Type:"+fType+",Size:"+str(size)+",Owner:"+owner+",Accessed:"+accTime+",Modified:"+modTime+","
                for item in line:
                    temp = item
                    #print(temp)
                    if isinstance(temp,dict):
                        for key in temp:
                            keys = temp.keys()
                            for tempKey in keys:
                                tk = tempKey.replace(" ","")
                                tV = temp[tempKey]
                                tV = tV.replace(" ","_")
                                tV = tV.replace("_pixels","")
                                if tk in badKeys:
                                    continue
                                if 'File' in tk:
                                    continue
                                else:    
                                    kvStr = tk.replace("/","per")+":"+tV+","
                                    print(tk+tV)
                                #print(kvStr)
                                fileStr = fileStr+kvStr
                fileStr = fileStr.rstrip(",")
                            #records.append(fileStr)
                #print(fileStr)
                records.append(fileStr)
            
            else:
                
                if fileType == 'pdf':
                    pdf = PdfFileReader(global_array[index])
                    info = pdf.getDocumentInfo()
                    numPages = pdf.getNumPages()
                    author = info.author
                    creator = info.creator
                    producer = info.producer
                    subject = info.subject
                    title = info.title
                    size = os.path.getsize(global_array[index])
                    fType = 'pdf'
                    fileStat = os.stat(global_array[index])
                    accTime = datetime.fromtimestamp(fileStat.st_atime).strftime("%D %I:%M:%S")
                    modTime = datetime.fromtimestamp(fileStat.st_mtime).strftime("%D %I:%M:%S")
                    owner = getpwuid(os.stat(global_array[index]).st_uid).pw_name
                    fileStr = fileStr+"Type:"+str(fType)+",Size:"+str(size)+",Owner:"+owner+",Accessed:"+accTime+",Modified:"+modTime+",Title:"+str(title)+",Author:"+str(author)+",Pages:"+str(numPages)+",Creator:"+str(creator)+",Producer:"+str(producer)+",Subject:"+str(subject)
                    #print(fileStr)
                    records.append(fileStr)
                                     
    #print("*",len(records),"*")
    #print("records",records)
    #for item in records:
        #print("*",'\n')
        #print(item)
        
    csv_output(args.output_file,records)
                        
        
# Main control flow of program is started here, first function called is main
if __name__ == '__main__':
    main()
    #format_output('/home/osboxes/Documents/ProfProj/FrontEnd/output2.csv')
