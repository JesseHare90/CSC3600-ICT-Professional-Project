#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# =======================================================================================================
# USQ LEARNING EMPORIUM
# Team Members
# Jesse Hare
# James Mckeown
# Ryan Sharp
# Richard Dobson
# Vincent Robertski
# Script for Metadata Searcher GUI (frontend)
# Written By Jesse Hare, Ryan Sharp
# =======================================================================================================
# import required modules
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import subprocess
from pathlib import Path
#import searcher_data as searcher
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QGridLayout, QVBoxLayout, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import os

"""
THE FOLLOWING FUNCTIONS ARE MAINLY FOR VALIDATION OF CSV DATA, GATHERING OF CSV DATA AND CREATING OF THE SQLITE3 DATABASE USED TO STORE METADATA FOR USE BY THE GUI
"""
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
# Tests whether a filename (as part of a csv file record) is actually valid and exists
# @param filename - file (and path to) of file as string
# @ return - True if the filepath is valid, false if not
# =======================================================================================================    
def isValidPath(filename):
    if os.path.exists(filename):
        #print(filename)
        return True
    else:
        print("The filepath/file, "+"'"+filename+"' does not exist, or is an invalid path")
        return False
    
# =======================================================================================================
# Extract data from the csv file (output of mdextract companion program)
# @param filepath - the path to the csv file
# @return - a list of lists, the first being each type of metadata attribute, then each subsequent element a list
#   of the metadata for each file
# =======================================================================================================

def get_csv_data(filepath):
    csvFileName, fileExt = os.path.splitext(filepath)
    #print("Loading, please wait...")
    if fileExt != '.csv':
        print('ERROR: expected a csv file, '+fileExt+" files are not usable as input")
        raise SystemExit
    file = str(filepath)
    csv_data = open(file,"r")
    #use readlines() to build a list of the csv data, line by line
    csv_records = csv_data.readlines()
    #print("loading, please wait")
    #split each line of csv_records into a list, using ',' as a delimeter
    records = []
    for i in csv_records:
        record = i.split(',')
        records.append(record)
    #define a set to use to store each type of metadata attribute
    #initialise with first attribute, filepath (csv file format doesn't specify the key for the filepath)
    attr_set = ["Filepath"]
    #now populate the attribute set with all types of metadata attributes found in records
    #print(records)
    print("Loading, please wait..")
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
                #the first value for each line of csv should be a filepath on it's own, if a valid path, pair with the key 'filepath' for that record
                
                
                if isValidPath(temprecord[0]):
                    tempdict["Filepath"] = temprecord[0]
                    check = "false"
                else:
                    # if the formatting of the csv file incorrect: expects a filepath as the first attribute on each line, terminates program
                    print("ERROR: Incorrect formatting of csv file: Expected valid filepath where none was found")
                    raise SystemExit
                
            else:
                #split key values at ':'
                #print(j)
                kv = j.split(":")
                tempdict[kv[0]] = kv[1]
        rows.append(tempdict)
        check = "true"
    # insert before file records the list of all unique attribute types found in csv file
    rows.insert(0,list(attr_set))
    #print(rows)
    csv_data.close()
    #print("Loading complete!")
    return rows

# =======================================================================================================
# create an in-memory sqlite3 database that will be used to store file metadata records used for display by the GUI
# @param data - the csv data gathered by the get_csv_data(filepath) function above, from the output generated by mdextract
# @return - a connection to the created and populated database    
# =======================================================================================================
def create_connection(data):
    connection = sqlite3.connect(':memory:')
    rows = []
    tempFields = data[0]
    fields = []
    for i in tempFields:
        if '/' in i:
            tempField = i.replace("/","to")
            fields.append(tempField.replace(" ",""))
        else:
            fields.append(i.replace(" ",""))
        
    #print(fields)
    for index, x in enumerate(data):
        temp = data[index]
        if (index > 0):
            rows.append(temp)
    crsr = connection.cursor()
    field_str = "CREATE TABLE filerecords ( "
    for i in fields:
        field = i
        #size is a pretty universal attribute type, so we will make that field in the db store integers, as well as Imageheight and width
        if field in ["Size","Imageheight","Imagewidth"]:
            field_str = field_str+field+" INTEGER(50),"
        else:
           field_str = field_str+field+" VARCHAR(50)," 
    field_str = field_str[:-1]
    field_str = field_str+");" 
    #print(field_str)
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
               sql_insert_p2.append("NULL")      
        crsr.execute(sql_insert,sql_insert_p2)   
    connection.commit()
    #print("Loading complete!")
    return connection

#========================================================================================================
"""
THE FOLLOWING FUNCTIONS ARE FOR CONSTRUCTION OF THE GUI AND IT'S ELEMENTS AND ALL SIGNAL/EVENT HANDLERS
"""    
#========================================================================================================

# =======================================================================================================
# define mainwindow that will house all GUI widget
# initialise and set values for all widgets
# define member functions for the Ui_MainWindow class
# =======================================================================================================
class Ui_MainWindow(object):
    # =======================================================================================================
    # Creates the MainWIndow for the GUI, and all enclosed widgets (elements)
    # @param MainWindow - the main window widget
    # @return N/A
    # =======================================================================================================    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1092, 896)
        self.data = get_csv_data(sys.argv[1])
        #csvData = self.data
        self.csvFields = self.data[0]
        self.conn = create_connection(self.data)
        self.order = "ASC"
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 100, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setToolTip("Enter one or more values, separated by either AND or OR operators")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 70, 111, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(True)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.populateFirstTable(self.tableWidget)
        self.retranslateUi(MainWindow)
        self.populateFieldSelect(self.comboBox)
        self.populateFieldSelect2(self.comboBox_2)
        self.pushButton.clicked.connect(self.SortTable)
        self.pushButton.setToolTip('Click to sort file metadata')
        self.pushButton_2.setToolTip('Click to search file metadata')
        self.pushButton_2.clicked.connect(self.SearchTable)
        self.tableWidget.cellDoubleClicked.connect(self.cell_was_clicked)
        # qStr is needed to store queries between different functions
        self.qStr = "blank"
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.SortByHeader)
        self.lineEdit_2.returnPressed.connect(self.SearchTable)
        self.createDynamicSearch(self.tableWidget)
        #create a toolbar to house widgets to interact with the file metadata records
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        self.reset = QAction("RESET")
        self.reset.triggered.connect(self.resetTable)
        self.mainToolBar.addAction(self.reset)
        self.mainToolBar.addWidget(self.label)
        self.mainToolBar.addWidget(self.comboBox)
        self.mainToolBar.addWidget(self.pushButton)
        self.mainToolBar.addWidget(self.radioButton)
        self.mainToolBar.addWidget(self.radioButton_2)
        self.mainToolBar.addWidget(self.label_2)
        self.mainToolBar.addWidget(self.comboBox_2)
        self.mainToolBar.addWidget(self.label_3)
        self.mainToolBar.addWidget(self.lineEdit_2)
        self.mainToolBar.addWidget(self.pushButton_2)
        # create a grid layout to store the dynamic search and file metadata records table
        grid = QGridLayout()
        grid.setSpacing(0)
        self.tableWidget_2.setFixedHeight(60)
        grid.addWidget(self.tableWidget_2, 1, 0)
        grid.addWidget(self.tableWidget, 2, 0)
        self.centralwidget.setLayout(grid)
        self.tableWidget_2.move(10,125)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        print("Loading complete!")
        
        
    # =======================================================================================================
    # Sets text values for labels and widgets (buttons, radio etc)
    # @param MainWindow - The main window object
    # @return - N/A
    # =======================================================================================================    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "File Metadata Searcher - USQ Learning Emporium"))
        self.pushButton.setText(_translate("MainWindow", "SORT"))
        self.pushButton_2.setText(_translate("MainWindow", "SEARCH"))
        self.label.setText(_translate("MainWindow", "SORT BY"))
        self.radioButton.setText(_translate("MainWindow", "ASCENDING"))
        self.radioButton_2.setText(_translate("MainWindow", "DESCENDING"))
        self.label_2.setText(_translate("MainWindow", "SEARCH BY"))
        self.label_3.setText(_translate("MainWindow", "FOR"))
    
    # =======================================================================================================  
    # reset all inputs, and display original table created from csv file (display all)
    # @return - N/A
    # =======================================================================================================  
    def resetTable(self):
        csv_data = self.data
        test = self.display_all(self.conn)
        self.qStr = "blank"
        self.lineEdit_2.clear()
        #self.tableWidget_2.clearContents()
        self.createTable(test)
        
    # =======================================================================================================
    # This function is fired when table cells are double clicked, which in turn opens the file the record is for
    # @param row - the row of the cell doubleclicked
    # @param column - the column of the cell doubleclicked
    # @return - N/A
    # =======================================================================================================
    def cell_was_clicked(self, row, column):
        # get the contents of the cell that is doubleclicked using the row and column parameters
        cell_contents = self.tableWidget.item(row, column)
        cell_contents = cell_contents.text()
        # get the column that the clicked cell belongs to
        header = self.tableWidget.horizontalHeaderItem(column).text()
        
        # if the cell double clicked contains the filepath, open the file
        if header == "Filepath":
            subprocess.call(["xdg-open",str(self.tableWidget.item(row, column).text())])
            # the line above opens the file on linux systems, the one below, windows. (requires os module)
            # to enable running on windows swap the two
            #os.startfile((self.tableWidget.item(row, column)).text())
            
    # =======================================================================================================
    # create the tableWidget that will display the harvested metadata
    # @param tableData - A list containing: all metadata fields as a list (first element), 
    #                                       then the corresponding attributes for each file as a tuple 
    # @return N/A
    # =======================================================================================================
    def createTable(self, tableData):
    	# Iterate through the metadata list
        for i in tableData:
            data2 = {}
            # get all occuring metadata fields (types) that were harvested as list
            fields = self.csvFields
            # get number of columns required to display harvested data in the table
            num_cols = len(fields)
            # create a list of dictionaries, where each dictionary has one of the attrib type as the key, with the values
            #   for the key being each file's value for that attribute type
            for f_index, i in enumerate(fields):
                key = i
                col_vals = []
                for index, j in enumerate(tableData):
                    if index > 0:
                        col_temp = j[f_index]
                        if col_temp == 'NULL':
                            col_vals.append(str(""))
                        else:
                            col_vals.append(str(col_temp))
                data2[key] = col_vals    
            data1 = data2  
            # get the number of rows required by counting how many values occur for the key 'filepath' in the dictionary list
            num_records = len(data1['Filepath'])        
            # set the row and column counts of the table    
            self.tableWidget.setRowCount(num_records)
            self.tableWidget.setColumnCount(num_cols)
            # set the MainWindow attribute 'data' to the data gathered (list of dicts)
            self.data = data1
            # now we populate the headers (column heading) for the table with the keys from self.data
            horHeaders = []
            #for n, key in enumerate(sorted(data1.keys())):
            for n, key in enumerate(data1.keys()):
                horHeaders.append(key)
                
                # now we loop though and populate the cells of the table
                for m, item in enumerate(data1[key]):
                    newitem = QTableWidgetItem(item)
                    #ensure that filemetadata records are selectable, but not editable
                    newitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) 
                    self.tableWidget.setItem(m, n, newitem)
            #configure automatic resizing for the columns and rows, and set the column headers
            self.tableWidget.resizeRowsToContents()
            self.tableWidget.setHorizontalHeaderLabels(horHeaders)
            self.tableWidget.resizeColumnsToContents()
            
            
    # =======================================================================================================
    # create and display the inital table of metadata shown on startup, using the searcher.get_csv_data() function
    #   to extract the metadata information from the csv file, then uses the searcher.display_all() function to use
    #   the data to create an sql database that contains all file metadata as records, then invoke createtable() to
    #   create the final table for display
    # @param tableWidget - the widget object responsible for diplaying the table within the main window of the GUI
    # @return N/A
    # =======================================================================================================
    def populateFirstTable(self, tableWidget):
        csv_data = self.data
        test = self.display_all(self.conn)
        self.createTable(test)
        
    # =======================================================================================================
    # populate the FieldSelect Widget used to specify the table field, with every individual metadata type
    # @param comboBox - the drop down widget used to select a choice from a list of text values representing each field
    # @return - N/A
    # =======================================================================================================
    def populateFieldSelect(self,comboBox):
        csv_data = self.data
        test = self.display_all(self.conn)
        fieldVals = test[0]
        self.comboBox.addItems(fieldVals)
    
    # =======================================================================================================
    # Same idea as above, but for a different comboBox widget
    # @param comboBox_2 - the drop down widget used to select a choice from a list of text values representing each field
    # @return N/A
    # =======================================================================================================    
    def populateFieldSelect2(self,comboBox_2):
        csv_data = self.data
        test = self.display_all(self.conn)
        fieldVals = test[0]
        self.comboBox_2.addItems(fieldVals)
    
    # =======================================================================================================
    # Capture the user input for the search function (the values to be searched for)
    # @param lineEdit_2 - the widget that takes user input as a string
    # @return - contents of the lineEdit widget
    # =======================================================================================================    
    def getSearchString(self, lineEdit_2):
        searchString = self.lineEdit_2.text()
        return searchString
    
    # =======================================================================================================
    # Check whether the Ascending or Descending option has been selected (radio buttons for search/sorting)
    # @return - ASC or DESC, as a string, depending on which radio button is cheched
    # =======================================================================================================
    def checkSortType(self):
       ascChecked = self.radioButton.isChecked()
       #descChecked = self.radioButton_2.isChecked()
       if ascChecked:
           return "ASC"
       else:
           return "DESC"
    
    # =======================================================================================================
    # Get selected field from drop down list of fields for the sort function
    # @param comboBox - the widget that displays the drop down list of fields
    # @return - The selected field as a string
    # =======================================================================================================
    def getSortField(self,comboBox):
        sortField = self.comboBox.currentText()
        return sortField
    
    # =======================================================================================================
    # Same as above, but for the field list used with the search function
    # =======================================================================================================
    def getSearchField2(self,comboBox_2):
        sortField = self.comboBox_2.currentText()
        return sortField
    
    # =======================================================================================================
    # Function to display file metadata sorted by a specified field
    # @return - N/A
    # =======================================================================================================
    def SortTable(self):
        csv_data = self.data
        sortField = str(self.getSortField(self.comboBox))
        sortOrder = str(self.checkSortType())
        test = self.display_sorted(csv_data,sortField,sortOrder,self.conn)
        self.createTable(test)

    # =======================================================================================================
    # Function to display file metadata in a table where userspecified values match the specified field
    # Uses the SQLite query SELECT * FROM <tablename> WHERE <selectedfield> LIKE <user supplied comma spearated values>
    # @return - N/A
    # =======================================================================================================  
    def SearchTable(self):
        csv_data = self.data
        searchField = str(self.getSearchField2(self.comboBox_2))
        searchString = str(self.getSearchString(self.lineEdit_2))
        sortOrder = str(self.checkSortType())
        # check user input using the checkInput function
        # if valid, display results, otherwise, show an error dialog on screen with information for the user
        if self.checkInput(self.lineEdit_2) == True:
            test = self.display_search(csv_data,searchString.strip(),searchField.strip(),sortOrder,self.conn)
            self.createTable(test)   
        else:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText('Incorrect format/ Invalid Input for Search Function')
            error.setInformativeText('Please enter one or more values separated by either \'AND\' or \'OR\'')
            error.setWindowTitle("Search Input Error")
            error.exec_()
    #========================================================================================================
    # Function that enables sorting of data by clicking on column headers, sorting by the particular field alternating in order
    # @param column - the column of the Header Clicked
    # @return - N/A
    #========================================================================================================
    def SortByHeader(self, column):
        # get the value in the column header clicked (field name)
        colVal = self.tableWidget.horizontalHeaderItem(column).text()
        # Perform a sort against the field name, DESC or ASC alternating for each click (by default is ASCENDING)
        if self.order == "DESC":
            csv_data = self.data
            self.createTable(self.display_sorted(csv_data,colVal,"DESC",self.conn))
            self.order = "ASC" 
        else:
            csv_data = self.data
            self.createTable(self.display_sorted(csv_data,colVal,"ASC",self.conn))
            self.order = "DESC"
    
    #========================================================================================================
    # This Function will check as to whether the input is a valid string of search values, separated by the AND
    # or OR operators
    # @param lineEdit_2 - the widget from which the input is to be checked
    # @return - True if the user supplied string is valid, false if not
    #========================================================================================================            
    def checkInput(self, lineEdit_2):
          inputStr = self.lineEdit_2.text()
          inputVals = inputStr.split()
          # if the amount of values and operators is even, or there are none, return false
          if (((len(inputVals) % 2) == 0) | (len(inputVals) == 0)):
              return False
          # if only one value is supplied it is valid (even if that value is OR or AND)
          if len(inputVals) == 1:
              return True
          # otherwise, extract all values and operators from the string
          # for input containing more than one element, every second element must be either OR or AND
          #and the first, and every second afterward, must be a value
          else:
              vals = inputVals[::2]
              conds = inputVals[1::2]
              # now we just check if this is the case, if so, return true, otherwise return false
              for i in conds:
                  if (i.upper() != "OR" )&( i.upper() != "AND"):
                      return False
              for i in vals:
                  if (i.upper() == "OR" )|(i.upper() == "AND"):
                      return False
          return True
    


    #========================================================================================================
    # This function will generate an text input for each column header, that may be used to search against multiple values at once
    # @param tablewidget - the one-row table used to take user input for the dynamic search
    # @return N/A
    #========================================================================================================     
    def createDynamicSearch(self, tableWidget):
        numCols = tableWidget.columnCount()
        colHeaders = []
        for column in range(numCols):
            header = tableWidget.horizontalHeaderItem(column)
            colHeaders.append(header.text())    
        counter = 0
        for cell in range(numCols):
            counter = counter+1
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 125, 1071, 55))
        self.tableWidget_2.setObjectName("tableWidget_2")
        counter = 0
        self.tableWidget_2.setRowCount(1)
        self.tableWidget_2.setColumnCount(numCols)
        self.tableWidget_2.setHorizontalHeaderLabels(colHeaders)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.cellChanged.connect(self.cellEdited)
        counter = 0
        # initialise all dynamic search fields to empty strings
        for i in range(numCols):
            self.tableWidget_2.setItem(0, counter, QTableWidgetItem(""))
            counter = counter+1
    
    #========================================================================================================
    # This function is called on an edit to the cells used for the dynamic search
    # It fires whenever a cell's content is changed, and then performs a search depending on the value of the cells
    # @return - N/A
    #======================================================================================================== 
    def cellEdited(self):
        searchVals = []
        searchValStr = []
        numCols = self.tableWidget_2.columnCount()
        column = 0
        for i in range(numCols):
            cellVal = self.tableWidget_2.item(0,column)
            cellCol = self.tableWidget_2.horizontalHeaderItem(column)
            # some cell widgets will throw an attribute error because they are empty, so ignore
            try:
                cellText = cellVal.text()
            except AttributeError:
                searchValStr.append(cellCol.text()+" LIKE '%'")
                continue
            else:
                searchValStr.append(cellCol.text()+" LIKE '%"+cellText+"%'")
                searchVals.append(cellText)
            column = column+1
        #search vals holds the values to search from, search valstr holds the corresponding filed like val part of query
        connection = self.conn
        crsr = connection.cursor()
        searchStr = []
        # go through and collect any cell values that are present in the search, and add to a list
        for index, i in enumerate(searchVals):
            if i != "":     
                searchStr.append(searchValStr[index])
        # get sort field and type for use for query
        sortField = self.getSortField(self.comboBox)
        sortType = self.checkSortType()
        if len(searchStr) == 0:
            queryStr = "SELECT * FROM filerecords ORDER BY "+sortField+" "+sortType
            self.qStr = queryStr
            crsr.execute(queryStr)
            output = crsr.fetchall()
            data = self.data
            fields = self.csvFields
            output.insert(0,fields)
            self.createTable(output)
            crsr.close()
            return

        else:
            # if only one search field has been filled
            if len(searchStr) == 1:
                queryStr = "SELECT * FROM filerecords WHERE "+searchStr[0]+ " ORDER BY "+sortField+" "+sortType
                self.qStr = queryStr
                crsr.execute(queryStr)
                output = crsr.fetchall()
                data = self.data
                fields = self.csvFields
                output.insert(0,fields)
                self.createTable(output)
                crsr.close()
                return
            else:
                #if more than one search field has been filled
                queryStr = "SELECT * FROM filerecords WHERE "
                #build the query string to execute against the db
                for index, y in enumerate(searchStr):
                    
                    if y != searchStr[-1]:
                        queryStr = queryStr+searchStr[index]+" AND "
                    else:
                        queryStr = queryStr+searchStr[index]+" ORDER BY "+sortField+" "+sortType
                #execute the completed query against the db and update the displayed results
                self.qStr = queryStr
                crsr.execute(queryStr)
                output = crsr.fetchall()
                data = self.data
                fields = self.csvFields
                output.insert(0,fields)
                self.createTable(output)
                crsr.close()
                return
    # =======================================================================================================
    # Perform a SELECT query against specified values for a selected field(metadata attr type/table column)
    # @param data - output of get_csv_data() function (SELECT * statement)
    # @param searchString - one or more comma separated values as a string, used in WHERE fieldname LIKE searchString
    # @param searchField - the specified fieldname as a string
    # @param sortType - ASC or DESC as a string, specifies an Ascending or Descending order sort by fieldname
    # @param connection - the in-memory database
    # @return - results of query against the table
    # =======================================================================================================
    def display_search(self,data, searchString, searchField, sortType, connection):
        fields = self.csvFields
        crsr = connection.cursor()
        # perform a search on the db for any records whose specified fieldname contains one or more specified strings
        tempList = searchString.split(" ")
        #print(tempList)
        query_str = "SELECT * FROM filerecords WHERE "
        operators = ["AND","OR"]
        for index, i in enumerate(tempList):
            #if there is only one value supplied, just search for it alone
            if len(tempList) == 1:
               if i.strip() != 'NULL':
                   temp = "'"+"%"+i.strip()+"%"+"'"
                   query_str = query_str+searchField+" LIKE "+temp 
                   query_str = query_str+" ORDER BY "+searchField+" "+sortType
                   self.qStr = query_str
                   crsr.execute(query_str)
                   output = crsr.fetchall()
                   output.insert(0,fields)
                   return output
               else:
                  temp = i.strip()
                  query_str = query_str+searchField+" IS '"+temp+"'" 
                  query_str = query_str+" ORDER BY "+searchField+" "+sortType
                  self.qStr = query_str
                  crsr.execute(query_str)
                  output = crsr.fetchall()
                  output.insert(0,fields)
                  return output
            else:
               value = tempList[index]
               if value != tempList[-1]:
                   #if a value, not an operator
                   if value not in operators:
                       nextOp = tempList[index+1]
                       if value != 'NULL':
                           query_str = query_str+searchField+" LIKE '%"+value+"%' "+nextOp+" "
                       else:
                           query_str = query_str+searchField+" IS '"+value+"' "+nextOp+" "
               if value == tempList[-1]:
                   if value not in operators:
                       if value != 'NULL':
                           query_str = query_str+searchField+" LIKE '%"+value+"%'"
                       else:
                           query_str = query_str+searchField+" IS '"+value+"'"
        query_str = query_str+" ORDER BY "+searchField+" "+sortType
        self.qStr = query_str
        crsr.execute(query_str)
        output = crsr.fetchall()
        output.insert(0,fields)
        return output              


    # =======================================================================================================
    # Sorts all file metadata according to a specified field, in Ascending or Descending order
    # @param data - data collected from the csv file using get_csv_data function
    # @param field - The field each file record will be sorted by
    # @param sortType - ASC or DESC, the order of the sorting (ascending or descending)
    # @return - all file metadata records sorting in ascending or descending order by a specified field
    # ======================================================================================================= 
    def display_sorted(self,data,field,sortType, connection):
    
        fields = self.csvFields
        crsr = connection.cursor()
        # now gather the odered results of the query on the table
        if self.qStr != "blank":
            #execute from results of previous statement
            crsr.execute("SELECT * FROM ("+self.qStr+")"+"ORDER BY "+field+" "+sortType)
        else:
            crsr.execute("SELECT * FROM filerecords "+"ORDER BY "+field+" "+sortType)
        output = crsr.fetchall()
        #insert at the beginning of the results the corresponding fields
        output.insert(0,fields)
        return output
                        
    # =======================================================================================================
    # create an SQLite3 database, and construct a schema based on the metadata extracted with the get_csv_data function
    #   then create a table in the database, of which isthen queried using a SELECT * statement
    #       This is the first function called by the GUI, which gives the initial display of file metadata
    # @param data - list of file metadata, output of the get_csv_data() function
    # @param connection - the in-memory database
    # @return - output of the "SELECT * FROM filerecords" query on the filerecords table
    # =======================================================================================================
    def display_all(self,connection):
        fields = self.csvFields
        #print(type(fields))
        #fields = fields[0]
        crsr = connection.cursor()   
        crsr.execute("SELECT * FROM filerecords")
        output = crsr.fetchall()
        output.insert(0,fields)
        return output

    
        
# ===========================================================================================================
# The main routine which sets up and displays the GUI of the program
# ===========================================================================================================      
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Incorrect Number of arguments Supplied")
        print("Error: Mdsearch.py requires only one argument, a valid csv file (created by mdextract.py)")
        print("See documentation for further details")
        sys.exit()
    file = Path(sys.argv[1])
    if not file.is_file():
        print("Error: No such file'"+sys.argv[1]+"'")
        sys.exit()
    app = QtWidgets.QApplication(sys.argv)
    #set the theme of the program to a dark-mode style
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
sys.exit(app.exec_())

