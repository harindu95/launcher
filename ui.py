#! /usr/bin/env python2
# -*- coding: utf-8 -*-
#
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import applications,terminal,web,file,actions,firefox
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
    
    # print "\nplug:", QThread.currentThreadId()
    results = []
    print "plugin :" , QThread.currentThreadId()
    if txt.strip()=='' :
        QThread.currentThread().emit(SIGNAL('update'), results,"all")
    else:
        results += actions.query(txt)
        results += applications.query(w,txt)
        results += firefox.query(w,txt)
        results.append(terminal.query(txt))
        results.append(web.query(txt))
        # if txt.startswith('firefox:'):
        # results += firefox.query(txt[8:])
        # w.setResults(results,"plugins")
        QThread.currentThread().emit(SIGNAL('update'), results,"plugins")


    
class LauncherWindow(QWidget):

    def __init__(self):
        super(QWidget,self).__init__()
        self.initUi()
        self.searchBox.textChanged.connect(self.textChanged)
        self.plugins = []
        self.files = []
        self.bg_thread2 = QThread()
        self.bg_thread = QThread()
        self.bg_thread.start()
        self.bg_thread2.start()
        self.bg_thread.connect(self.bg_thread, SIGNAL("update"), self.setResults )
        self.connect(self.bg_thread2, SIGNAL("update"), self.setResults )
        # self.connect(QThread.currentThread(), SIGNAL("update"), self.setResults )
        self.connect(self.searchBox,SIGNAL('focusOut'),self.focusOutEvent)
        
    def setResults(self,results,Type=None):
        if Type == "plugins":
            self.plugins = results
        elif Type == "files":
            self.files = results
        elif Type == "all":
            self.files = results
            self.plugins =results
            
        self.selected = 0
        self.visibleStart = 0
        self.visibleEnd = 5
        self.updateUi()
        
    def initUi(self):
        self.center()
        self.searchBox = myLineEdit()
        self.searchBox.setStyleSheet("margin:3px;border:none;font-size:36px;font-style:normal;font-family:DejaVu Sans;font-weight: 200;")
        self.setObjectName("main")
        self.setStyleSheet("QWidget#main{border:1px solid #CCCCCC;}")
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
        self.visibleStart = 0
        self.visibleEnd = 5
        
    def center(self):
        self.move(QApplication.desktop().screen().rect().center()- self.rect().center())
        
    def textChanged(self, text):
        # print "gui :", QThread.currentThreadId()
        try:
            self.wk1.terminate = True
        except AttributeError:
            pass
        
        self.wk1 = GenericWorker(getResults, self,str(text).split(" "))
        self.wk1 = GenericWorker(getResults, self,str(text))
        self.wk1.terminate = False
        self.wk1.moveToThread(self.bg_thread)
        self.wk1.connect_()
        self.wk1.start.emit(text)
        # getResults(self,text)
        # if str(text).startswith("file:") and str(text).endswith(" "):
        file.query(self,text)
        
    def updateUi(self):
        results =  self.plugins + self.files
        print "gui:" , QThread.currentThreadId()
        l = len(results)
        # print l
        for i in range(5):
            if i < l  and self.visibleStart+i < l:
                self.items[i].changeItem(results[self.visibleStart+i],i==self.selected)
                self.items[i].show()
            elif i>=l or l == 0:
                self.items[i].hide()

        if (self.visibleEnd-self.visibleStart) > l:
            self.adjustSize()

        self.visibleEnd = min(5,l)
        # print results,self.visibleResults, len(results)

    def goDown(self):
        if len(self.files+self.plugins)> self.selected:
                if self.selected>=5:
                    self.visibleEnd += 1
                    self.visibleStart +=1
                    self.updateUi()
        else:
            self.selected -=1

        self.selectItem()

    def goUp(self):
        if self.selected<self.visibleStart:
            if len(self.files+self.plugins)> self.selected:
                self.visibleEnd -= 1
                self.visibleStart -=1
                self.updateUi()
            else:
                self.selected -=1

        self.selectItem()
        
    def selectItem(self):
        for i in range(5):
            self.items[i].selectItem(i==(self.selected-self.visibleStart))
            
    def keyPressEvent(self,event):
        # Escape key
        if event.key() == 0x01000000:
            self.close()
            # Up key
        if event.key() == 0x01000013 :
            self.selected = max ( 0, self.selected -1 )
            self.goUp()

            # Down key
        if event.key() == 0x01000015 :
            self.selected = min (len(self.plugins + self.files),self.selected+1)
            self.goDown()

        # enter key
        if event.key() == 0x01000004 :
            if event.matches(QKeySequence.InsertLineSeparator):
                self.items[self.selected- self.visibleStart].execute(shift=True)
            else:           
                self.items[self.selected - self.visibleStart].execute()

            self.close()

            
    def focusOutEvent(self,event):
        self.close()
        # pass

# Create an PyQT4 application object.
a = QApplication(sys.argv)
# Set window size.
w = LauncherWindow()
w.resize(650, 60)
w.show()
a.exec_()
w.bg_thread.quit()
w.bg_thread2.quit()
a.exit()

