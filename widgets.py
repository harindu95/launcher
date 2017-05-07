from PyQt4.QtGui import *
from PyQt4.QtCore import *

class myLineEdit(QLineEdit):
    def __init__(self):
        super(QLineEdit,self).__init__()

    def focusOutEvent(self,event):
        self.emit(SIGNAL('focusOut'),event)


class ResultWidget(QWidget):
    
    def __init__(self, text=""):
        super(QWidget,self).__init__()
        self.initUi(text)

    def initUi(self, text):
        self.layout = QHBoxLayout()
        self.label1 = QLabel(text)
        self.label2 = QLabel(text)
        self.icon = QLabel()
        self.icon.setStyleSheet("margin:0;padding:0;width:64px;")
        self.layout.addWidget(self.icon)
        self.vbox = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.label2)
        self.vbox.setSpacing(0)
        self.widget.setMinimumSize(QSize(600,48))
        self.widget.setMaximumSize(QSize(600,48))
        self.layout.addWidget(self.widget,1)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.label1.setStyleSheet("font-weight:normal;font-style:normal;font-style:normal;font-family:DejaVu Sans;font-weight: 200;font-size:20px;")
        self.label2.setStyleSheet("font-weight:normal;font-style:normal;font-style:normal;font-family:DejaVu Sans;font-weight: 100;font-size:12px;")
        self.setStyleSheet("padding:3px;margin:0;background:#ffffff")
        self.connect(self,SIGNAL('mouseClicked'),self.execute)

    def mousePressEvent(self,event):
        self.execute()
        
    def changeItem(self,result,selected=False):
        self.result = result
        icon = result['Icon']
        text = result['Name']
        self.image = QPixmap(icon).scaled(QSize(48,48),transformMode=Qt.SmoothTransformation)
        self.icon.setPixmap(self.image)
        self.label1.setText(text)
        self.label2.setText(result['Comment'])
        self.setMinimumSize(QSize(630, 60))
        if selected:
            self.setStyleSheet("background-color:#eeeeee;")
        else:
            self.setStyleSheet("background-color:#ffffff")

    def selectItem(self,selected=True):
        if selected:
            self.setStyleSheet("background-color:#eeeeee;")
        else:
            self.setStyleSheet("background-color:#ffffff")

    def execute(self):
        if self.result['Type'] == "applications":
            import applications
            applications.execute(self.result)
            print "executing ", self.result

        elif self.result['Type'] == "terminal":
            import terminal
            terminal.execute(self.result)
        elif self.result['Type'] == "web":
            import web
            web.execute(self.result)
        elif self.result['Type'] == "file":
            import file
            file.execute(self.result)

