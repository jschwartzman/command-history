#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
# file: historyDlg7.sh (command-history project)
#
#           A utility program written in PyQt5 that examines
#           and searches your .bash_history file.
# author:   John Schwartzman, Forte Systems, Inc.
#
# last revision:	10/17/2018
##############################################################################
VERSION_NUMBER = '1.0.0'
RELEASE_DATE   = '10/17/2018'

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(743, 411)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonTrim = QtWidgets.QPushButton(Dialog)
        self.pushButtonTrim.setEnabled(False)
        self.pushButtonTrim.setObjectName("pushButtonTrim")
        self.gridLayout.addWidget(self.pushButtonTrim, 6, 4, 1, 1)
        self.pushButtonCopy = QtWidgets.QPushButton(Dialog)
        self.pushButtonCopy.setEnabled(False)
        self.pushButtonCopy.setObjectName("pushButtonCopy")
        self.gridLayout.addWidget(self.pushButtonCopy, 0, 4, 1, 1)
        self.pushButtonRestore = QtWidgets.QPushButton(Dialog)
        self.pushButtonRestore.setEnabled(False)
        self.pushButtonRestore.setObjectName("pushButtonRestore")
        self.gridLayout.addWidget(self.pushButtonRestore, 1, 4, 1, 1)
        self.pushButtonClose = QtWidgets.QPushButton(Dialog)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.gridLayout.addWidget(self.pushButtonClose, 3, 4, 1, 1)
        self.labelTrim = QtWidgets.QLabel(Dialog)
        self.labelTrim.setObjectName("labelTrim")
        self.gridLayout.addWidget(self.labelTrim, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 2)
        self.checkBoxAlphabetize = QtWidgets.QCheckBox(Dialog)
        self.checkBoxAlphabetize.setObjectName("checkBoxAlphabetize")
        self.gridLayout.addWidget(self.checkBoxAlphabetize, 2, 4, 1, 1)
        self.lineEditTrim = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(47)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditTrim.sizePolicy().hasHeightForWidth())
        self.lineEditTrim.setSizePolicy(sizePolicy)
        self.lineEditTrim.setObjectName("lineEditTrim")
        self.gridLayout.addWidget(self.lineEditTrim, 6, 1, 1, 2)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 0, 0, 5, 3)
        self.labelTrim.setBuddy(self.lineEditTrim)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # set tab order
        Dialog.setTabOrder(self.listWidget, self.pushButtonCopy)
        Dialog.setTabOrder(self.pushButtonCopy, self.pushButtonRestore)
        Dialog.setTabOrder(self.pushButtonRestore, self.checkBoxAlphabetize)
        Dialog.setTabOrder(self.checkBoxAlphabetize, self.lineEditTrim)
        Dialog.setTabOrder(self.lineEditTrim, self.pushButtonTrim)
        Dialog.setTabOrder(self.pushButtonTrim, self.pushButtonClose)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # hook up signals (widget outputs) and slots (class member methods)
        self.pushButtonClose.clicked.connect(self.close)
        self.pushButtonCopy.clicked.connect(self.copyText)
        self.pushButtonTrim.clicked.connect(self.trimList)
        self.lineEditTrim.textChanged.connect(self.trimTextChanged)
        self.lineEditTrim.returnPressed.connect(self.trimList)
        self.pushButtonRestore.clicked.connect(self.restoreHistory)
        self.listWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.listWidget.itemDoubleClicked.connect(self.copyItemText)
        self.checkBoxAlphabetize.stateChanged.connect(self.checkAndChangeSorting)
        
        # member variables
        self.historyFileName = ''
        self.unsortedList = []
        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Command History"))
        self.pushButtonTrim.setText(_translate("Dialog", "Trim &List"))
        self.pushButtonCopy.setText(_translate("Dialog", 
                                               "Copy\n&Selection\nto\nClipboard"))
        self.pushButtonRestore.setText(_translate("Dialog", "&Restore\nHistory"))
        self.pushButtonClose.setText(_translate("Dialog", "&Close"))
        self.labelTrim.setText(_translate("Dialog", "&Trim"))
        self.checkBoxAlphabetize.setText(_translate("Dialog", "&Alphabetized"))

    def clearListBox(self):         # remove all items from listWidget
        while self.listWidget.count() > 0:
            self.listWidget.takeItem(0)
            
    def close(self):
        sys.exit(0)

    def selectionChanged(self):     # listWidget selection has changed
        if self.listWidget.currentItem():
            self.pushButtonCopy.setEnabled(True)
        else:
            self.pushButtonCopy.setEnabled(False)

    def copyItemText(self, item):   # listWidget double-clicked
        self.lineEditTrim.setText(item.text())
    
    def copyText(self):             # copy to clipboard
        if self.listWidget.currentItem():
            clipboard = app.clipboard()
            clipboard.setText(self.listWidget.currentItem().text())
       
    def trimList(self):             # trim the history list
        strToMatch = self.lineEditTrim.text()
        if strToMatch != '':
            linesToRetain = []
            for line in self.unsortedList:
                if line.decode('utf-8').__contains__(strToMatch):
                    linesToRetain.append(line)
            self.clearListBox()
            self.unsortedList = []
            for line in linesToRetain:  # already in newest to oldest order
                self.unsortedList.append(line)
                self.listWidget.addItem(line)
            self.checkAndChangeSorting()
            self.pushButtonRestore.setEnabled(True)
            
    def trimTextChanged(self):
        if self.lineEditTrim.text():
            self.pushButtonTrim.setEnabled(True)
        else:
            self.pushButtonTrim.setEnabled(False)
                
    def restoreHistory(self):   # restore the entire history (less duplicates)
        self.clearListBox()
        self.populateListBox('')
        self.pushButtonRestore.setEnabled(False)
        
    def checkAndChangeSorting(self):    # sort the list or restore the unsorted list
        if self.checkBoxAlphabetize.checkState() == QtCore.Qt.Unchecked:
            self.listWidget.setSortingEnabled(False)
            self.clearListBox()
            for line in self.unsortedList:    # newest to oldest order
                self.listWidget.addItem(line)
        else:
            self.listWidget.setSortingEnabled(True)
            self.listWidget.sortItems()
        
    def populateListBox(self, text):    # first time and restore history
        fd = open(self.historyFileName, 'r')
        lines = fd.read().splitlines()
        #remove duplicates
        newLines = []
        self.unsortedList = []
        for line in lines:
            if line not in newLines:
                newLines.append(line)
        for line in reversed(newLines):     # newest to oldest order
            if line.__contains__(text):
                self.unsortedList.append(line)
                self.listWidget.addItem(line)
        fd.close()
        self.checkAndChangeSorting()
        
    def usage(self, progName):    # print usage information and get out
        sNameArray = progName.rsplit('/', 1)
        print('\n' + sNameArray[1] + ': a command history search utility')
        print('\t-h | --help\t\tdisplay this list')
        print('\t-v | --version\t\tdisplay version information')
        print('\t\'search term\'\t\tsearch for \'search term\' in the command history')
        print('\tno argument\t\tview/search the command history\n\n')
        sys.exit(0)
        
    def version(self, progName):    # print version information and get out
        sNameArray = progName.rsplit('/', 1)
        print('\n' + sNameArray[1] + ': a command history search utility')
        print('\tversion: ' + VERSION_NUMBER + 
              '\trelease date: ' + RELEASE_DATE + '\n\n')
        sys.exit(0)

if __name__ == "__main__":
    import sys, os
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.historyFileName = os.path.expandvars("$HOME/.bash_history")
    if len(sys.argv) > 1 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        ui.usage(sys.argv[0])
    if len(sys.argv) > 1 and (sys.argv[1] == '-v' or sys.argv[1] == '--version'):
        ui.version(sys.argv[0])
    text = ''
    if len(sys.argv) > 1:   # did the user provide an argument?
        text = sys.argv[1]
    if text != '':
        ui.pushButtonRestore.setEnabled(True)
    ui.populateListBox(text)
    Dialog.show()
    sys.exit(app.exec_())

