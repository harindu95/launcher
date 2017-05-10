from PyQt4.QtGui import *
from PyQt4.QtCore import *
import functools
import os


def getLaunchers():
    apps = []
    for filename in os.listdir('/usr/share/applications'):
        try:
            if not '.desktop' in filename:
                continue
            with  open('/usr/share/applications/' + filename,'r') as file:
                text = file.readlines()
                try:
                    launcher=  extractData(text)
                    if(launcher):
                        apps.append(launcher)
                        
                except ValueError,e:
                    print e
        except IOError:
            pass
    for filename in os.listdir('/home/harindu/.local/share/applications'):
        if not '.desktop' in filename:
                continue

        try:
            with  open('/home/harindu/.local/share/applications/' + filename,'r') as file:
                text = file.readlines()
                try:
                    launcher=  extractData(text)
                    if(launcher):
                        apps.append(launcher)
                except ValueError,e:
                    print e
        except IOError:
            pass
    return apps

def extractData(txt):
    
    app = {"Exec":'','Icon':'','Comment':'','Name':"","Type":"applications" }
    for line in txt:
        if line.strip().startswith('#'):
            continue
        elif 'Name' in line and app['Name'] == "":
            app['Name'] = line[line.index('=')+1:].replace('\n','')
            
        elif 'Comment' in line and app['Comment']=='' :
            app['Comment'] = line[line.index('=')+1:].replace('\n','')
        elif 'Exec' in line and not app['Exec']:
            app['Exec'] = line[line.index('=')+1:].replace('\n','').replace('%u','')
        elif 'Icon' in line:
            app['Icon'] = icon_fullpath(line[line.index('=')+1:].replace('\n',''))

    if app['Exec'] == '':
        print app,txt
        return None

    return app

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

apps = []

def checkTerms(terms,txt):
    for term in terms:
        if not term in txt:
            return False
    return True

def query(w,txt):
    global apps
    # import re
    results = []
    if len(apps) == 0 :
        apps = getLaunchers()
        
    txt = str(txt).lower()
    terms = txt.split(" ")
    # pattern ='.*'+'.*'.join(terms)
    # pattern = re.compile(pattern)
    # widget =  QWidget()
    for app in apps:
        # "Exec":'','Icon':'','Comment':'' 
        info = app['Name'] + app['Exec'] + app['Comment']
        info = info.lower()
        if w.wk1.terminate:
            break
        if checkTerms(terms,info):
            if txt in app['Name'].lower():
                results.insert(0,app)
            else:
                results.append(app)

    return results

def execute(app):
    import os
    # Popen(app['Exec'] + " &")
    os.system('nohup ' + app["Exec"] + ' & ')
