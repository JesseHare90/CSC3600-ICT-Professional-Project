#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# =======================================================================================================
# USQ LEARNING EMPORIUM
# Team Members
# Jesse Hare
# James Mackeown
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
import searcher_data as searcher
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(90, 30, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 30, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 100, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 100, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setToolTip("Enter one or more comma separated values")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 70, 111, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(25, 33, 67, 13))
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 140, 1071, 731))
        self.tableWidget.setObjectName("tableWidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(210, 60, 102, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(True)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(210, 80, 102, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 100, 31, 16))
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
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
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
        if header == "filepath":
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
            fields = tableData[0]
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
                        col_vals.append(str(col_temp))
                data2[key] = col_vals    
            data1 = data2  
            # get the number of rows required by counting how many values occur for the key 'filepath' in the dictionary list
            num_records = len(data1['filepath'])        
            # set the row and column counts of the table    
            self.tableWidget.setRowCount(num_records)
            self.tableWidget.setColumnCount(num_cols)
            # set the MainWindow attribute 'data' to the data gathered (list of dicts)
            self.data = data1
            # now we populate the headers (column heading) for the table with the keys from self.data
            horHeaders = []
            for n, key in enumerate(sorted(data1.keys())):
                horHeaders.append(key)
                # now we loop though and populate the cells of the table
                for m, item in enumerate(data1[key]):
                    newitem = QTableWidgetItem(item)
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
        csv_data = searcher.get_csv_data(sys.argv[1])
        test = searcher.display_all(csv_data)
        self.createTable(test)
        
    # =======================================================================================================
    # populate the FieldSelect Widget used to specify the table field, with every individual metadata type
    # @param comboBox - the drop down widget used to select a choice from a list of text values representing each field
    # @return - N/A
    # =======================================================================================================
    def populateFieldSelect(self,comboBox):
        csv_data = searcher.get_csv_data(sys.argv[1])
        test = searcher.display_all(csv_data)
        fieldVals = test[0]
        self.comboBox.addItems(fieldVals)
    
    # =======================================================================================================
    # Same idea as above, but for a different comboBox widget
    # @param comboBox_2 - the drop down widget used to select a choice from a list of text values representing each field
    # @return N/A
    # =======================================================================================================    
    def populateFieldSelect2(self,comboBox_2):
        csv_data = searcher.get_csv_data(sys.argv[1])
        test = searcher.display_all(csv_data)
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
        csv_data = searcher.get_csv_data(sys.argv[1])
        sortField = str(self.getSortField(self.comboBox))
        sortOrder = str(self.checkSortType())
        test = searcher.display_sorted(csv_data,sortField,sortOrder)
        self.createTable(test)

    # =======================================================================================================
    # Function to display file metadata in a table where userspecified values match the specified field
    # Uses the SQLite query SELECT * FROM <tablename> WHERE <selectedfield> LIKE <user supplied comma spearated values>
    # @return - N/A
    # =======================================================================================================  
    def SearchTable(self):
        csv_data = searcher.get_csv_data(sys.argv[1])
        searchField = str(self.getSearchField2(self.comboBox_2))
        searchString = str(self.getSearchString(self.lineEdit_2))
        sortOrder = str(self.checkSortType())
        
        test = searcher.display_search(csv_data,searchString.strip(),searchField.strip(),sortOrder)
        self.createTable(test)

# ===========================================================================================================
# The main routine which sets up and displays the GUI of the program
# ===========================================================================================================      
if __name__ == "__main__":
    #import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

