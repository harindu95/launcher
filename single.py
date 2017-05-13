#! /usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMessageBox, QApplication
from PyQt4.QtCore import QIODevice, QTimer, QCoreApplication
from PyQt4.QtNetwork import QLocalServer, QLocalSocket
import sys
from ui import *

class QSingleApplication(QApplication):
    def singleStart(self, mainWindow):
        self.mainWindow = mainWindow
        # Socket
        self.m_socket = QLocalSocket()
        self.m_socket.connected.connect(self.connectToExistingApp)
        self.m_socket.error.connect(self.startApplication)
        self.m_socket.connectToServer(self.applicationName(), QIODevice.WriteOnly)
    def connectToExistingApp(self):
        if len(sys.argv)>1 and sys.argv[1] is not None:
            self.m_socket.write(sys.argv[1])
            self.m_socket.bytesWritten.connect(self.quit)
        else:
            QMessageBox.warning(None, self.tr("Already running"), self.tr("The program is already running."))
            # Quit application in 250 ms
            QTimer.singleShot(250, self.quit)
            
    def startApplication(self):
        self.m_server = QLocalServer()
        if self.m_server.listen(self.applicationName()):
            self.m_server.newConnection.connect(self.getNewConnection)
            self.mainWindow.show()
        else:
            QMessageBox.critical(None, self.tr("Error"), self.tr("Error listening the socket."))
            print "error"
            self.quit()
            
    def getNewConnection(self):
        self.new_socket = self.m_server.nextPendingConnection()
        self.new_socket.readyRead.connect(self.readSocket)
        
    def readSocket(self):
        f = self.new_socket.readLine()
        self.mainWindow.getArgsFromOtherInstance(str(f))
        self.mainWindow.activateWindow()
        self.mainWindow.show()

if __name__ == '__main__':
    from PyQt4.QtGui import QMainWindow, QLabel
    class DallAgneseWindow(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)
            self.setWindowTitle("QSingleApplication Demo")
            labelText = "<b>dallagnese.fr recipe</b><br /><br />\
                        Allows you to start your program only once.<br />\
                        Parameters of later calls can be handled by this application."
            self.setCentralWidget(QLabel(labelText))
        def getArgsFromOtherInstance(self, args):
            QMessageBox.information(self, self.tr("Received args from another instance"),args)

    app = QSingleApplication(sys.argv)
    app.setApplicationName("Launcher")
    w = LauncherWindow()
    # w = DallAgneseWindow()
    app.singleStart(w)
    w.resize(650, 60)
    app.exec_()
    w.bg_thread.quit()
    w.bg_thread2.quit()
    app.m_socket.close()
    app.exit()

    
