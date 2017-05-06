#! /usr/bin/env python2
# -*- coding: utf-8 -*-
#
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import applications,terminal,web
from widgets import *

# from MyLayout import *
class GenericWorker(QObject):
    def __init__(self, function, *args, **kwargs):
        super(GenericWorker, self).__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start.connect(self.run)

    start = pyqtSignal(str)

    # @pyqtSlot
    def run(self, some_string_arg):
        self.function(*self.args, **self.kwargs)

def getResults(w,txt):
    results = {}
    if str(txt).strip() == "" :
        w.bg_thread.emit(SIGNAL('update'), results)
    else:
        results= applications.query(txt)
        results.append(terminal.query(txt))
        results.append(web.query(txt))

        w.bg_thread.emit(SIGNAL('update'), results)


    
class LauncherWindow(QWidget):

    def __init__(self):
        super(QWidget,self).__init__()
        self.initUi()
        self.searchBox.textChanged.connect(self.textChanged)
        self.bg_thread = QThread()
        self.bg_thread.start()
        self.bg_thread.connect(self.bg_thread, SIGNAL("update"), self.updateUi )
        self.connect(self.searchBox,SIGNAL('focusOut'),self.focusOutEvent)
        
    
    def initUi(self):
        self.center()
        self.searchBox = myLineEdit()
        self.searchBox.setStyleSheet("margin:3px;border:none;font-size:36px;font-style:normal;font-family:DejaVu Sans;font-weight: 200;")
        # self.setStyleSheet("*{ border:1px solid black; }")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.searchBox)
        self.results = [ResultWidget() for x in range(5)]
        self.visibleResults = 0
        self.selected = 0
        for label in self.results:
            label.hide()
            self.layout.addWidget(label)

        self.setLayout(self.layout)
        self.searchBox.setMinimumSize(QSize(630,50))
        self.setFocusPolicy(Qt.StrongFocus)
        
    def center(self):
        self.move(QApplication.desktop().screen().rect().center()- self.rect().center())

    def textChanged(self, text):
        wk = GenericWorker(getResults, self,text)
        wk.moveToThread(self.bg_thread)
        wk.start.emit(text)

    def updateUi(self,results):

        l = len(results)

       

        self.selected = 0
        for i in range(5):
            if i < l :
                self.results[i].changeItem(results[i],i==self.selected)
                self.results[i].show()
            elif i>=l or l == 0:
                self.results[i].hide()

        if self.visibleResults > l:
            self.adjustSize()

        # print results,self.visibleResults, len(results)    
        self.visibleResults = min(5,l)

    def selectItem(self):
        for i in range(5):
            self.results[i].selectItem(i==self.selected)
            
    def keyPressEvent(self,event):
        # Escape key
        if event.key() == 0x01000000:
            self.close()
            # Up key
        if event.key() == 0x01000013 :
            self.selected = max ( 0, self.selected -1 )
            self.selectItem()

            # Down key
        if event.key() == 0x01000015 :
            self.selected = min(self.visibleResults-1,self.selected +1)
            self.selectItem()

        # enter key
        if event.key() == 0x01000004 :
            self.results[self.selected].execute()
            self.close()

    def focusOutEvent(self,event):
        self.close()
        # pass

        
# Create an PyQT4 application object.
a = QApplication(sys.argv)
w = LauncherWindow()
# Set window size.
w.resize(650, 60)
w.show()
# w.setWindowState( Qt.WindowFullScreen)
# w.size(QSize(400,400))
a.exec_()
w.bg_thread.quit()
a.exit()

# chrome = applications.extractData(open('/usr/share/applications/google-chrome.desktop').readlines())
