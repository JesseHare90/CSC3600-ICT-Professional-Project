# -*- coding: utf-8 -*-
# =======================================================================================================
# 
# =======================================================================================================
# import sqlite3 module to create a relational database and table to store file metadata
import sqlite3
# os module needed for file operations
import os

# =======================================================================================================
# Tests whether a given string can represent an int
# @param s - string to test
# @return - True if string can represent an int, such as '12345', False if not, eg: '1Y234' etc
# =======================================================================================================
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# =======================================================================================================
# Extract data from the csv file (output of mdextract companion program)
# @param filepath - the path to the csv file
# @return - a list of lists, the first being each type of metadata attribute, then each subsequent element a list
#   of the metadata for each file
# =======================================================================================================
def get_csv_data(filepath):
    file = str(filepath)
    csv_data = open(file,"r")
    #use readlines() to build a list of the csv data, line by line
    csv_records = csv_data.readlines()
    #split each line of csv_records into a list, using ',' as a delimeter
    records = []
    for i in csv_records:
        record = i.split(',')
        records.append(record)
    #define a set to use to store each type of metadata attribute
    #initialise with first attribute, filepath (csv file format doesn't specify the key for the filepath)
    attr_set = ["filepath"]
    #now populate the attribute set with all types of metadata attributes found in records
    for i in records:
        temp = i
        for j in temp[1:]:
            atrrandval = j.split(':')
            field = atrrandval[0]
            if (field not in attr_set):
                attr_set.append(field)   
    #now we will convert each record into a dictionary (key:value pairs) for each metadata attribute
    rows = []
    check = "true"
    for i in records:
        temprecord = i
        tempdict = {}
        for j in temprecord:
            if (check == "true"):         
                tempdict["filepath"] = temprecord[0]
                check = "false"
            else:
                kv = j.split(":")
                tempdict[kv[0]] = kv[1]
        rows.append(tempdict)
        check = "true"

    rows.insert(0,list(attr_set))
    return rows
    
# =======================================================================================================
# create an SQLite3 database, and construct a schema based on the metadata extracted with the get_csv_data function
#   then create a table in the database, of which isthen queried using a SELECT * statement
#       This is the first function called by the GUI, which gives the initial display of file metadata
# @param data - list of file metadata, output of the get_csv_data() function
# @return - output of the "SELECT * FROM filerecords" query on the filerecords table
# =======================================================================================================
def display_all(data):
    rows = []
    fields = data[0]
    for index, x in enumerate(data):
        temp = data[index]
        if (index > 0):
            rows.append(temp)
    # remove the database if it exists - helps avoid problems caused by more than one function attempting to access at once
    if os.path.exists("filerecords.db"):
        os.remove("filerecords.db")
    connection = sqlite3.connect("filerecords.db")
    crsr = connection.cursor()
    field_str = "CREATE TABLE filerecords ( "
    for i in fields:
        field = i
        if field == "size":
            field_str = field_str+field+" INTEGER(50),"
        else:
           field_str = field_str+field+" VARCHAR(50)," 
    field_str = field_str[:-1]
    field_str = field_str+");" 
    crsr.execute(field_str)
    #create an insert statement for the sql database
    #get first part of the insert query
    attr_len = len(fields)-1       
    sql_insert = "INSERT INTO filerecords VALUES"
    #col_num = len(fields)
    values = "("
    for index, y in enumerate(fields):
        if index == attr_len:
            values = values+" ?)"
        else:
            values = values+" ?,"
    sql_insert = sql_insert+values
    # construct second portion of SQL INSERT query on the filerecords table  
    for i in rows:
        sql_insert_p2 = []
        temp = i
        for index, j in enumerate(fields):
            field = j
            if j in temp:
                if RepresentsInt(temp[j].strip()):
                    sql_insert_p2.append(int(temp[j].strip()))
                else:
                    sql_insert_p2.append(temp[j].strip())    
            else:
               sql_insert_p2.append("")      
        crsr.execute(sql_insert,sql_insert_p2)   
    connection.commit()    
    crsr.execute("SELECT * FROM filerecords")
    output = crsr.fetchall()
    output.insert(0,fields)
    connection.close()
    return output

"""
display_search takes information from the GUI to perform a SELECT query against specified values for a selected field
"""
# =======================================================================================================
# Perform a SELECT query against specified values for a selected field(metadata attr type/table column)
# @param data - output of get_csv_data() function (SELECT * statement)
# @param searchString - one or more comma separated values as a string, used in WHERE fieldname LIKE searchString
# @param searchField - the specified fieldname as a string
# @param sortType - ASC or DESC as a string, specifies an Ascending or Descending order sort by fieldname
# @return - results of query against the table
# =======================================================================================================
def display_search(data, searchString, searchField, sortType):
    # initialise empty list to store file records and a list of all the fields (metadata attribute types)
    rows = []
    fields = data[0]
    # populate rows[] with each file's data
    for index, x in enumerate(data):
        temp = data[index]
        if (index > 0):
            rows.append(temp)
    # remove the database if it already exists (avoids concurrency problems)    
    if os.path.exists("filerecords.db"):
        os.remove("filerecords.db")
    # create the database 'filerecords'
    connection = sqlite3.connect("filerecords.db")
    crsr = connection.cursor()
    # create the table 'filerecords' and it's schema
    field_str = "CREATE TABLE filerecords ( "
    for i in fields:
        field = i
        if field == "size":
            field_str = field_str+field+" INTEGER(50),"
        else:
           field_str = field_str+field+" VARCHAR(50),"
    field_str = field_str[:-1]
    field_str = field_str+");"    
    crsr.execute(field_str)
    #create an insert statement for the sql database
    #get first part of the insert query 
    attr_len = len(fields)-1        
    sql_insert = "INSERT INTO filerecords VALUES"
    values = "("
    for index, y in enumerate(fields):
        if index == attr_len:
            values = values+" ?)"
        else:
            values = values+" ?,"
    
    sql_insert = sql_insert+values
    # get second part of insert query, then execute
    for i in rows:
        sql_insert_p2 = []
        temp = i
        for index, j in enumerate(fields):
            field = j
            if j in temp:
                if RepresentsInt(temp[j].strip()):
                    sql_insert_p2.append(int(temp[j].strip()))
                else:
                    sql_insert_p2.append(temp[j].strip())    
            else:
               sql_insert_p2.append("")
        crsr.execute(sql_insert,sql_insert_p2) 
    connection.commit()
    # perform a search on the db for any records whose specified fieldname contains one or more specified strings
    tempList = searchString.split(",")
    print(tempList)
    query_str = "SELECT * FROM filerecords WHERE "
    for i in tempList:
        if i == tempList[-1]:
            temp = "'"+"%"+i.strip()+"%"+"'"
            query_str = query_str+searchField+" LIKE "+temp
        else:
           temp = "'"+"%"+i.strip()+"%"+"'"
           query_str = query_str+searchField+" LIKE "+temp+" OR "
    query_str = query_str+" ORDER BY "+searchField+" "+sortType
    print(query_str)
    crsr.execute(query_str)
    output = crsr.fetchall()
    output.insert(0,fields)
    connection.close()
    return output
   
# =======================================================================================================
# Sorts all file metadata according to a specified field, in Ascending or Descending order
# @param data - data collected from the csv file using get_csv_data function
# @param field - The field each file record will be sorted by
# @param sortType - ASC or DESC, the order of the sorting (ascending or descending)
# @return - all file metadata records sorting in ascending or descending order by a specified field
# ======================================================================================================= 
def display_sorted(data,field,sortType):
    # get all types(fields) of metadata that appear in csv file, and also each files data added to a list
    rows = []
    fields = data[0]
    for index, x in enumerate(data):
        temp = data[index]
        if (index > 0):
            rows.append(temp)
    # remove filerecords database from previous execution if it exists   
    if os.path.exists("filerecords.db"):
        os.remove("filerecords.db")
    # create table in db to store metadata for files 
    connection = sqlite3.connect("filerecords.db")
    crsr = connection.cursor()
    field_str = "CREATE TABLE filerecords ( "
    for i in fields:
        if i == "size":
            field_str = field_str+i+" INTEGER(50),"
        else:  
            field_str = field_str+i+" VARCHAR(50),"
    field_str = field_str[:-1]
    field_str = field_str+");"   
    crsr.execute(field_str)
    #create an insert statement for the sql database
    #get first part of the insert query
    attr_len = len(fields)-1       
    sql_insert = "INSERT INTO filerecords VALUES"
    values = "("
    for index, y in enumerate(fields):
        if index == attr_len:
            values = values+" ?)"
        else:
            values = values+" ?,"
    sql_insert = sql_insert+values
    # create second part of insert query
    for i in rows:
        sql_insert_p2 = []
        temp = i
        # test each attribute for whether it can be represented by an int, if so, insert as an integer
        for index, j in enumerate(fields):
            if j in temp:
                if RepresentsInt(temp[j].strip()):
                    sql_insert_p2.append(int(temp[j].strip()))
                else:
                    sql_insert_p2.append(temp[j].strip())
            else:
               sql_insert_p2.append("")       
        crsr.execute(sql_insert,sql_insert_p2)
    connection.commit()
    # now gather the odered results of the query on the table
    crsr.execute("SELECT * FROM filerecords "+"ORDER BY "+field+" "+sortType)
    output = crsr.fetchall()
    #insert at the beginning of the results the corresponding fields
    output.insert(0,fields)
    connection.close()
    return output

# =======================================================================================================
# Code Below is just for testing purposes
# =======================================================================================================
#csv_data = get_csv_data('testdata.csv')
#print(csv_data)
#print(data)   
#testASC = display_sorted(csv_data, "size", "ASC")
#testDESC = display_sorted(csv_data, "size", "DESC")  
#testALL = display_all(csv_data)  
#testSRCH = display_search(csv_data, "jesse,jess", "author", "DESC")  