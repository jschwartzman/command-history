#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HistoryDlg5.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(616, 272)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonCopy = QtWidgets.QPushButton(Dialog)
        self.pushButtonCopy.setObjectName("pushButtonCopy")
        self.gridLayout.addWidget(self.pushButtonCopy, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(454, 20, 
                                           QtWidgets.QSizePolicy.Expanding, 
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.pushButtonRestore = QtWidgets.QPushButton(Dialog)
        self.pushButtonRestore.setObjectName("pushButtonRestore")
        self.gridLayout.addWidget(self.pushButtonRestore, 1, 3, 1, 1)
        self.pushButtonClose = QtWidgets.QPushButton(Dialog)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.gridLayout.addWidget(self.pushButtonClose, 2, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 24, 
                                            QtWidgets.QSizePolicy.Minimum, 
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)
        self.labelTrim = QtWidgets.QLabel(Dialog)
        self.labelTrim.setObjectName("labelTrim")
        self.gridLayout.addWidget(self.labelTrim, 4, 0, 1, 1)
        self.pushButtonTrim = QtWidgets.QPushButton(Dialog)
        self.pushButtonTrim.setObjectName("pushButtonTrim")
        self.gridLayout.addWidget(self.pushButtonTrim, 4, 3, 1, 1)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 0, 0, 4, 3)
        self.lineEditTrim = QtWidgets.QLineEdit(Dialog)
        self.lineEditTrim.setObjectName("lineEditTrim")
        self.gridLayout.addWidget(self.lineEditTrim, 4, 1, 1, 2)
        self.labelTrim.setBuddy(self.lineEditTrim)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # set tab order
        Dialog.setTabOrder(self.listWidget, self.pushButtonCopy)
        Dialog.setTabOrder(self.pushButtonCopy, self.pushButtonRestore)
        Dialog.setTabOrder(self.pushButtonRestore, self.pushButtonClose)
        Dialog.setTabOrder(self.pushButtonClose, self.lineEditTrim)
        Dialog.setTabOrder(self.lineEditTrim, self.pushButtonTrim)
        
        # hook up signals (widget outputs) and slots (class member methods)
        self.pushButtonClose.clicked.connect(self.close)
        self.pushButtonCopy.clicked.connect(self.copyText)
        self.pushButtonTrim.clicked.connect(self.trimList)
        self.lineEditTrim.returnPressed.connect(self.trimList)
        self.pushButtonRestore.clicked.connect(self.restoreHistory)
        self.listWidget.itemDoubleClicked.connect(self.copyItemText)

        # member variables
        self.historyFileName = ''

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Command History"))
        self.pushButtonCopy.setText(_translate("Dialog", 
                                               "Copy\n&Selection\nto\nClipboard"))
        self.pushButtonRestore.setText(_translate("Dialog", "&Restore\nHistory"))
        self.pushButtonClose.setText(_translate("Dialog", "&Close"))
        self.labelTrim.setText(_translate("Dialog", "Trim"))
        self.pushButtonTrim.setText(_translate("Dialog", "&Trim List"))
        
    def clearListBox(self):         # remove all items from listWidget
        while self.listWidget.count() > 0:
            self.listWidget.takeItem(0)
            
    def close(self):                # terminate the program
        sys.exit(0)

    def copyItemText(self, item):   # listWidget double-clicked
        self.lineEditTrim.setText(item.text())
    
    def copyText(self):             # copy to clipboard
        if self.listWidget.currentItem():
            clipboard = app.clipboard()
            clipboard.setText(self.listWidget.currentItem().text())
       
    def trimList(self):             # trim the history list
        strToMatch = self.lineEditTrim.text()
        if strToMatch != '':
            linesToRetain = self.listWidget.findItems(strToMatch, 
                                                      QtCore.Qt.MatchContains |                                                                                                                              
                                                      QtCore.Qt.CaseSensitive | 
                                                      QtCore.Qt.MatchRecursive)
            self.clearListBox()
            for line in linesToRetain:
                self.listWidget.addItem(line)
                
    def restoreHistory(self):   # restore the entire history (less duplicates)
        self.clearListBox()
        self.populateListBox('')
        
    def populateListBox(self, text):    # first time and restore history
        fd = open(self.historyFileName, 'r')
        lines = fd.read().splitlines()
        #remove duplicates
        newLines = []
        for line in lines:
            if line not in newLines:
                newLines.append(line)
        for line in newLines:
            if line.__contains__(text):
                self.listWidget.addItem(line)
        fd.close()

if __name__ == "__main__":
    import sys, os
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.historyFileName = os.path.expandvars("$HOME/.bash_history")
    text = ''
    if len(sys.argv) > 1:   # did the user provide an argument?
        text = sys.argv[1]
    ui.populateListBox(text)
    Dialog.show()
    sys.exit(app.exec_())

