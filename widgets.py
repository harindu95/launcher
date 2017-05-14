from PyQt4.QtGui import *
from PyQt4.QtCore import *

def icon_fullpath(icon):
    import gtk
    icon_theme = gtk.icon_theme_get_default()
    icon_info = icon_theme.lookup_icon(icon, 64, 64)
    if icon_info == None:
        if icon.startswith(r'/'):
                return icon
        return '/usr/share/icons/Numix/32/status/dialog-question.svg'
    # print icon_info.get_filename()
    return icon_info.get_filename()

class myLineEdit(QLineEdit):
    def __init__(self):
        super(QLineEdit,self).__init__()

    def focusOutEvent(self,event):
        self.emit(SIGNAL('focusOut'),event)


class ResultWidget(QWidget):
    
    def __init__(self,plugin_list, text=""):
        super(QWidget,self).__init__()
        self.initUi(text)
        self.plugin_list = plugin_list

    def initUi(self, text):
        self.layout = QHBoxLayout()
        self.lblName = QLabel(text)
        self.lblComment = QLabel(text)
        self.icon = QLabel()
        self.icon.setStyleSheet("margin:0;padding:0;width:64px;")
        self.layout.addWidget(self.icon)
        self.vbox = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.vbox.addWidget(self.lblName)
        self.vbox.addWidget(self.lblComment)
        self.vbox.setSpacing(0)
        self.widget.setMinimumSize(QSize(600,48))
        self.widget.setMaximumSize(QSize(600,48))
        self.layout.addWidget(self.widget,1)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.lblName.setStyleSheet("font-weight:normal;font-style:normal;font-style:normal;font-family:DejaVu Sans;font-weight: 200;font-size:20px;")
        self.lblComment.setStyleSheet("font-weight:normal;font-style:normal;font-style:normal;font-family:DejaVu Sans;font-weight: 100;font-size:12px;")
        self.setStyleSheet("padding:3px;margin:0;background:#ffffff")
        self.connect(self,SIGNAL('mouseClicked'),self.execute)

    def mousePressEvent(self,event):
        self.execute()
        
    def changeItem(self,result,selected=False):
        self.result = result
        icon = result['Icon']
        if not result['Icon'].startswith('//') :
            icon = icon_fullpath(result['Icon'])
            
        self.image = QPixmap(icon).scaled(QSize(48,48),transformMode=Qt.SmoothTransformation)
        self.icon.setPixmap(self.image)
        
        self.lblName.setText(result['Name'])
        self.lblComment.setText(result['Comment'])
        if selected:
            self.setStyleSheet("background-color:#eeeeee;")
        else:
            self.setStyleSheet("background-color:#ffffff")

        # self.adjustSize()

    def selectItem(self,selected=True):
        if selected:
            self.setStyleSheet("background-color:#eeeeee;")
        else:
            self.setStyleSheet("background-color:#ffffff")

    def execute(self,**kwargs):
        self.plugin_list[self.result['Type']].execute(self.result,kwarg)
        # if self.result['Type'] == "applications":
        #     import plugins.applications
        #     plugins.applications.execute(self.result)
        #     print "executing ", self.result

        # elif self.result['Type'] == "terminal":
        #     import plugins.terminal
        #     plugins.terminal.execute(self.result,**kwargs)
        # elif self.result['Type'] == "web":
        #     import plugins.web
        #     plugins.web.execute(self.result)
        # elif self.result['Type'] == "file":
        #     import plugins.file
        #     plugins.file.execute(self.result)

        # elif self.result['Type'] == "actions":
        #     import plugins.actions
        #     plugins.actions.execute(self.result)
        # elif self.result['Type'] == "firefox":
        #     import plugins.firefox
        #     plugins.firefox.execute(self.result)
