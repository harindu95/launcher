from PyQt4.QtGui import *
from PyQt4.QtCore import *

import subprocess,os,mimetypes

class GenericWorker(QObject):

    start = pyqtSignal(str)

    def __init__(self, function, *args, **kwargs):
        super(GenericWorker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def connect_and_emit(self):
        self.start.connect(self.run)
        self.start.emit("")

    @pyqtSlot()
    def run(self,args=None):
        self.function(*self.args, **self.kwargs)
        
def get_mimetype_icon(mimetype):
    import gtk, gio
    iconName = gio.content_type_get_icon( mimetype )
    theme = gtk.icon_theme_get_default()
    icon = theme.choose_icon(iconName.get_names(), 48, 0)
    if not icon :
        return get_mimetype_icon('application/octet-stream')
    
    return icon.get_filename()

def query(w,txt):
    txt = txt.replace(' ','')
    try:
        w.wk.terminate = True
    except AttributeError:
        pass
    
    w.wk = GenericWorker(searchFiles, w,txt)
    w.wk.terminate = False
    w.wk.moveToThread(w.bg_thread2)
    w.wk.connect_and_emit()
    return True


def searchFiles(w,txt):
    print "file search:" , QThread.currentThreadId()
    findCMD = 'locate -l 30 ' + str(txt)
    out = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE, 
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out.wait() 
    # Check if the process has really terminated & force kill if not.
    filelist = []
    i = 0
    filelist = out.stdout.readlines()
    # i += 1
    # filelist.append(line.replace('\n',''))
    # if i == 30 or w.wk.terminate:
    #     break

    # pid = out.pid
    # out.terminate()
    # try:
    #     os.kill(pid, 0)
    #     out.kill()
    #     print "Forced kill"
    # except OSError, e:
    #     print "Terminated gracefully"
    # Save found files to list

    results = []
    for file in filelist:
        result = { "Name":file,"Comment":"","Path":file,"Type":"file"}
        mimetype = mimetypes.guess_type(file)[0]
        result['Icon'] = get_mimetype_icon(mimetype or 'document')
        results.append(result)

    QThread.currentThread().emit(SIGNAL('update'),results,"files")

def execute(file):
    import os
    # Popen(app['Exec'] + " &")
    # x-terminal-emulator -e "zsh -c \"apropos editor; exec zsh\""
    cmd = str('nohup xdg-open '+ file["Path"] + ' &')
    print cmd 
    os.system(cmd)



