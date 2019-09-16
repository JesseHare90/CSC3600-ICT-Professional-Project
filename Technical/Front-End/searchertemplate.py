# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searcher.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import searcher_data as searcher
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *




class Ui_MainWindow(object):
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
        self.label.setGeometry(QtCore.QRect(20, 30, 47, 13))
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 140, 1071, 731))
        self.tableWidget.setObjectName("tableWidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(210, 60, 82, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(True)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(210, 80, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 100, 21, 16))
        self.label_3.setObjectName("label_3")
        #self.radioButton_2.setChecked(True)
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
        #print(self.checkSortType())
        #print(self.getSortField(self.comboBox))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Sort"))
        self.pushButton_2.setText(_translate("MainWindow", "SEARCH"))
        self.label.setText(_translate("MainWindow", "SORT BY"))
        self.radioButton.setText(_translate("MainWindow", "ASCENDING"))
        self.radioButton_2.setText(_translate("MainWindow", "DESCENDING"))
        self.label_2.setText(_translate("MainWindow", "SEARCH IN"))
        self.label_3.setText(_translate("MainWindow", "FOR"))
    
    def cell_was_clicked(self, row, column):
        print("Row %d and Column %d was clicked" % (row, column))
        #item = self.itemAt(row, column)
        cell_contents = self.tableWidget.item(row, column)
        cell_contents = cell_contents.text()
        #print(cell_contents)
        header = self.tableWidget.horizontalHeaderItem(column).text()
        #print(header)
        if header == "filepath":
            os.startfile((self.tableWidget.item(row, column)).text())
        
    def populateFirstTable(self, tableWidget):
        
        csv_data = searcher.get_csv_data(sys.argv[1])
        #print(data)   
        test = searcher.display_all(csv_data)
        for i in test:
            print(i)
        data2 = {}
        fields = test[0]
        #print(fields)
        num_cols = len(fields)
        
        
        for f_index, i in enumerate(fields):
            key = i
            col_vals = []
            for index, j in enumerate(test):
                if index > 0:
                    col_temp = j[f_index]
                    col_vals.append(str(col_temp))
            data2[key] = col_vals
            
                
        num_records = len(data2)        
            
        tableWidget.setRowCount(num_records)
        tableWidget.setColumnCount(num_cols)
        data1 = data2
        
        self.data = data1

        
        
        horHeaders = []
        for n, key in enumerate(sorted(data1.keys())):
            horHeaders.append(key)
            #print(horHeaders)
            for m, item in enumerate(data1[key]):
                newitem = QTableWidgetItem(item)
                #print(newitem)
                newitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) 
                
                self.tableWidget.setItem(m, n, newitem)
                
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)
        #self.tableWidget.cellDoubleClicked.connect(self.cell_was_clicked)
        
    def populateFieldSelect(self,comboBox):
        csv_data = searcher.get_csv_data(sys.argv[1])
        test = searcher.display_all(csv_data)
        fieldVals = test[0]
        self.comboBox.addItems(fieldVals)
        
    def populateFieldSelect2(self,comboBox_2):
        csv_data = searcher.get_csv_data(sys.argv[1])
        test = searcher.display_all(csv_data)
        fieldVals = test[0]
        self.comboBox_2.addItems(fieldVals)
        
    def getSearchString(self, lineEdit_2):
        searchString = self.lineEdit_2.text()
        return searchString
    
    
    def checkSortType(self):
       ascChecked = self.radioButton.isChecked()
       #descChecked = self.radioButton_2.isChecked()
       if ascChecked:
           return "ASC"
       else:
           return "DESC"
    
    def getSortField(self,comboBox):
        sortField = self.comboBox.currentText()
        return sortField
    
    def getSearchField2(self,comboBox_2):
        sortField = self.comboBox_2.currentText()
        return sortField
    
    def SortTable(self):
        csv_data = searcher.get_csv_data(sys.argv[1])
        sortField = str(self.getSortField(self.comboBox))
        
        sortOrder = str(self.checkSortType())
        #print(sortField)
        #print(sortOrder)
        test = searcher.display_sorted(csv_data,sortField,sortOrder)
        data2 = {}
        fields = test[0]
        num_cols = len(fields)
        
        
        for f_index, i in enumerate(fields):
            key = i
            col_vals = []
            for index, j in enumerate(test):
                if index > 0:
                    col_temp = j[f_index]
                    col_vals.append(str(col_temp))
                    
            data2[key] = col_vals
            #print(col_vals)
            
                
        num_records = len(data2)        
            
        self.tableWidget.setRowCount(num_records)
        self.tableWidget.setColumnCount(num_cols)
        data1 = data2
        
        self.data = data1
        horHeaders = []
        for n, key in enumerate(sorted(data1.keys())):
            horHeaders.append(key)
            #print(horHeaders)
            for m, item in enumerate(data1[key]):
                newitem = QTableWidgetItem(item)
                #print(newitem)
                newitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) 
                
                self.tableWidget.setItem(m, n, newitem)
                
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)
       
    def SearchTable(self):
        csv_data = searcher.get_csv_data(sys.argv[1])
        searchField = str(self.getSearchField2(self.comboBox_2))
        searchString = str(self.getSearchString(self.lineEdit_2))
        sortOrder = str(self.checkSortType())
        #sortOrder = str(self.checkSortType())
        #print(sortField)
        #print(sortOrder)
        test = searcher.display_search(csv_data,searchString.strip(),searchField.strip(),sortOrder)
        print(test)
        data2 = {}
        fields = test[0]
        num_cols = len(fields)
        self.tableWidget.clear()
        
        for f_index, i in enumerate(fields):
            key = i
            col_vals = []
            for index, j in enumerate(test):
                if index > 0:
                    col_temp = j[f_index]
                    col_vals.append(str(col_temp))
                    
            data2[key] = col_vals
            
            
        data1 = data2        
        num_records = len(data1['filepath'])  
        #print(num_records)
            
        self.tableWidget.setRowCount(num_records)
        self.tableWidget.setColumnCount(num_cols)
        
        #self.data = ""
        self.data = data1
        #print(len(data1['filepath']))
        
        
        horHeaders = []
        for n, key in enumerate(sorted(data1.keys())):
            horHeaders.append(key)
            #print(horHeaders)
            for m, item in enumerate(data1[key]):
                newitem = QTableWidgetItem(item)
                #print(newitem)
                newitem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) 
                
                self.tableWidget.setItem(m, n, newitem)
                
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)
        #self.tableWidget.cellDoubleClicked.connect(self.cell_was_clicked)
       
       
if __name__ == "__main__":
    #import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

