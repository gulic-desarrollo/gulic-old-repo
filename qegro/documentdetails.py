# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'documentdetails.ui'
#
# Created: sáb nov 12 18:51:36 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.15
#
# WARNING! All changes made in this file will be lost!


from qt import *


class documentDetails(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("documentDetails")


        documentDetailsLayout = QVBoxLayout(self,11,6,"documentDetailsLayout")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        self.textLabel1.setTextFormat(QLabel.PlainText)
        documentDetailsLayout.addWidget(self.textLabel1)

        self.groupBox1 = QGroupBox(self,"groupBox1")
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(11)
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        self.textLabel2 = QLabel(self.groupBox1,"textLabel2")

        groupBox1Layout.addWidget(self.textLabel2,0,0)

        self.lineEdit1 = QLineEdit(self.groupBox1,"lineEdit1")

        groupBox1Layout.addWidget(self.lineEdit1,0,1)
        documentDetailsLayout.addWidget(self.groupBox1)

        self.groupBox2 = QGroupBox(self,"groupBox2")
        documentDetailsLayout.addWidget(self.groupBox2)

        self.languageChange()

        self.resize(QSize(561,555).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Document Details"))
        self.textLabel1.setText(self.__tr("Enter details about this document below."))
        self.groupBox1.setTitle(self.__tr("Author"))
        self.textLabel2.setText(self.__tr("Name:"))
        self.groupBox2.setTitle(self.__tr("Company"))


    def __tr(self,s,c = None):
        return qApp.translate("documentDetails",s,c)
