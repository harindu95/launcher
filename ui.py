#! /usr/bin/env python2
# -*- coding: utf-8 -*-
#
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import applications,terminal,web,file
from widgets import *

# from MyLayout import *
class GenericWorker(QObject):
    start = pyqtSignal(str)

    def __init__(self, function, *args, **kwargs):
        super(GenericWorker, self).__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs

    def connect_(self):
        self.start.connect(self.run)


    # @pyqtSlot
    def run(self, some_string_arg):
        self.function(*self.args, **self.kwargs)

def getResults(w,txt):
    
    print "\nplug:", QThread.currentThreadId()
    results = []
    txt = str(txt)
    if txt.strip() == "" :
        w.bg_thread.emit(SIGNAL('update'), results)
    else:
        results= applications.query(txt)
        results.append(terminal.query(txt))
        results.append(web.query(txt))
        w.bg_thread.emit(SIGNAL('update'), results,"plugins")


    
class LauncherWindow(QWidget):

    def __init__(self):
        super(QWidget,self).__init__()
        self.initUi()
        self.searchBox.textChanged.connect(self.textChanged)
        self.plugins = []
        self.files = []
        self.bg_thread = QThread()
        self.bg_thread2 = QThread()
        self.bg_thread.start()
        self.bg_thread2.start()
        self.bg_thread.connect(self.bg_thread, SIGNAL("update"), self.setResults )
        self.bg_thread2.connect(self.bg_thread2, SIGNAL("update"), self.setResults )
        self.connect(self.searchBox,SIGNAL('focusOut'),self.focusOutEvent)
        
    def setResults(self,results,Type=None):
        if Type == "plugins":
            self.plugins = results
        elif Type == "files":
            self.files = results
            
        self.updateUi()
        
    def initUi(self):
        self.center()
        self.searchBox = myLineEdit()
        self.searchBox.setStyleSheet("margin:3px;border:none;font-size:36px;font-style:normal;font-family:DejaVu Sans;font-weight: 200;")
        # self.setStyleSheet("*{ border:1px solid black; }")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.searchBox)
        self.items = [ResultWidget() for x in range(5)]
        self.visibleResults = 0
        self.selected = 0
        for label in self.items:
            label.hide()
            self.layout.addWidget(label)

        self.setLayout(self.layout)
        self.searchBox.setMinimumSize(QSize(630,50))
        self.setFocusPolicy(Qt.StrongFocus)
        
    def center(self):
        self.move(QApplication.desktop().screen().rect().center()- self.rect().center())

    def textChanged(self, text):
        print "gui :", QThread.currentThreadId()

        wk = GenericWorker(getResults, self,text)
        wk.connect_()
        wk.moveToThread(self.bg_thread)
        wk.start.emit(text)
        if str(text).startswith("file:") and str(text).endswith(" "):
            file.query(self,text[5:])

    def updateUi(self):

        results =  self.plugins + self.files

        l = len(results)
        print l
        self.selected = 0
        for i in range(5):
            if i < l :
                self.items[i].changeItem(results[i],i==self.selected)
                self.items[i].show()
            elif i>=l or l == 0:
                self.items[i].hide()

        if self.visibleResults > l:
            self.adjustSize()

        # print results,self.visibleResults, len(results)    
        self.visibleResults = min(5,l)

    def selectItem(self):
        for i in range(5):
            self.items[i].selectItem(i==self.selected)
            
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
            self.items[self.selected].execute()
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
w.bg_thread2.quit()
a.exit()

# chrome = applications.extractData(open('/usr/share/applications/google-chrome.desktop').readlines())
