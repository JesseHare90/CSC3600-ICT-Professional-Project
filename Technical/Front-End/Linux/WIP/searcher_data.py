# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 14:41:11 2019

@author: Jesse
"""

import sqlite3
import sys
import os
#this function extracts the data from the csv file

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False




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
    #initialise with first attribute, filepath
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
           
    #now we will construct a database with the data we have gathered from the csv file
    #create the table called 'filerecords' in memory (only persists for duration of program)
    rows.insert(0,list(attr_set))
    return rows
    

#print(get_csv_data(sys.argv[1]))
    

def display_all(data):
    rows = []
    fields = data[0]
    for index, x in enumerate(data):
        temp = data[index]
        if (index > 0):
            rows.append(temp)
        
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
    
    #sql_insertp3 = []
    #print(sql_insert)
    #print(attr_set)
    
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
        #print(sql_insert,sql_insert_p2)
    connection.commit()    
    crsr.execute("SELECT * FROM filerecords")
    output = crsr.fetchall()
    
    #testing output
    
    output.insert(0,fields)
    
    #connection.commit()
    connection.close()
    return output

def display_search(data, searchString, searchField, sortType):
    rows = []
    fields = data[0]
    print(type(searchString))
    for index, x in enumerate(data):
        temp = data[index]
        if (index > 0):
            rows.append(temp)
        
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
    
    #sql_insertp3 = []
    
    #print(attr_set)
    
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
    #searchStr ="SELECT * FROM filerecords "+"WHERE "+searchField+" LIKE %"+searchString+"%"    
    #print(searchStr)
    tempList = searchString.split(",")
    print(tempList)
    query_str = "SELECT * FROM filerecords WHERE "
    
    for i in tempList:
        if i == tempList[-1]:
            temp = "'"+"%"+i.strip()+"%"+"'"
            query_str = query_str+searchField+" LIKE "+temp
            #print(temp)
        else:
           temp = "'"+"%"+i.strip()+"%"+"'"
           #print(temp)
           query_str = query_str+searchField+" LIKE "+temp+" OR "
    query_str = query_str+" ORDER BY "+searchField+" "+sortType
    print(query_str)
    crsr.execute(query_str)
    """
    searchString = "("
    for i in tempList:
        if i == tempList[-1]:
            temp = "'"+i.strip()
            searchString = searchString+temp+"')"
        else:
            temp = "'"+i.strip()
            searchString = searchString+temp+"', "
            
    print("SELECT * FROM filerecords "+"WHERE "+searchField+" IN "+searchString)    
    crsr.execute("SELECT * FROM filerecords "+"WHERE "+searchField+" IN "+searchString)
    """
    output = crsr.fetchall()
    
    #testing output
   
    output.insert(0,fields)
    
    #connection.commit()
    connection.close()
    return output
   
    
def display_sorted(data,field,sortType):
    rows = []
    fields = data[0]
    for index, x in enumerate(data):
        temp = data[index]
        if (index > 0):
            rows.append(temp)
        
    if os.path.exists("filerecords.db"):
        os.remove("filerecords.db")
    connection = sqlite3.connect("filerecords.db")
    crsr = connection.cursor()
    field_str = "CREATE TABLE filerecords ( "
    for i in fields:
        
        #print("the field is",i)
        if i == "size":
            #print(i)
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
    #col_num = len(fields)
    values = "("
    for index, y in enumerate(fields):
        if index == attr_len:
            values = values+" ?)"
        else:
            values = values+" ?,"
    
    sql_insert = sql_insert+values
    
    #sql_insertp3 = []
    
    #print(attr_set)
    
    for i in rows:
        sql_insert_p2 = []
        temp = i
        for index, j in enumerate(fields):
            #field = j
            if j in temp:
                if RepresentsInt(temp[j].strip()):
                    #print(temp[j])
                    sql_insert_p2.append(int(temp[j].strip()))
                    #print(type(int(temp[j].strip())),int(temp[j].strip()))
                else:
                    sql_insert_p2.append(temp[j].strip())
                    #print(type(temp[j].strip()),temp[j].strip())
            else:
               sql_insert_p2.append("")
        #print(sql_insert,sql_insert_p2)       
        crsr.execute(sql_insert,sql_insert_p2)
    
    connection.commit()
    #print("SELECT * FROM filerecords "+"ORDER BY "+field+" "+sortType)    
    
    crsr.execute("SELECT * FROM filerecords "+"ORDER BY "+field+" "+sortType)
    data = crsr.execute("SELECT * FROM filerecords "+"ORDER BY "+field+" "+sortType)
    #for i in crsr:
        #print(i[1])
    #crsr.execute("SELECT * FROM filerecords ORDER BY size ASC")
    output = crsr.fetchall()
    
   
    output.insert(0,fields)
    
    #connection.commit()
    connection.close()
    return output

csv_data = get_csv_data('testdata.csv')
#print(csv_data)
#print(data)   
#testASC = display_sorted(csv_data, "size", "ASC")
#testDESC = display_sorted(csv_data, "size", "DESC")  
#testALL = display_all(csv_data)  
testSRCH = display_search(csv_data, "jesse,jess", "author", "DESC")  