import os
import cPickle as pickle
import os.path
import xdg.DesktopEntry

def getLaunchers():
    apps = []
    import codecs
    desktop = xdg.DesktopEntry.DesktopEntry()
    for filename in os.listdir('/usr/share/applications'):
        try:
            if not '.desktop' in filename:
                continue
            with  codecs.open('/usr/share/applications/' + filename,'r',"utf-8") as file:
                try:
                    desktop.parse('/usr/share/applications/' + filename)
                    launcher = { 'Name':desktop.getName(),
                                 'Exec':desktop.getExec().replace('%u','').replace('%U','').replace('%f',''),
                                 'Comment':desktop.getComment(),
                                 'Icon':desktop.getIcon() or '',
                                 'Terminal':desktop.getTerminal(),
                                 'Type':'applications'}
                    if(launcher):
                        apps.append(launcher)
                    if 'nautilus' in filename.lower():
                        print launcher
                except Exception,e:
                    print e
        except IOError:
            pass
    for filename in os.listdir('/home/harindu/.local/share/applications'):
        if not '.desktop' in filename:
                continue

        try:
            with  open('/home/harindu/.local/share/applications/' + filename,'r') as file:
                try:
                    desktop.parse('/home/harindu/.local/share/applications/' + filename)
                    launcher = { 'Name':desktop.getName(),
                                 'Exec':desktop.getExec(),
                                 'Comment':desktop.getComment(),
                                 'Icon':desktop.getIcon() or '',
                                 'Terminal':desktop.getTerminal(),
                                 'Type':'applications'}
                    if(launcher):
                        apps.append(launcher)
                except ValueError,e:
                    print e
        except IOError:
            pass

        
    return apps


apps = []

def checkTerms(terms,txt):
    for term in terms:
        if not term in txt:
            # print txt,terms
            return False
    return True

def terminalCommands():
    import subprocess
    apps = []
    CMD = "zsh -ci \'print -rl -- ${(ko)commands}\'"    
    out = subprocess.Popen(CMD,shell=True,stdin=subprocess.PIPE, 
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out.wait()
    commands = out.stdout.readlines()
    for cmd in commands:
        # print cmd
        cmd = cmd.replace('\n','')
        apps.append({"Exec":cmd,'Icon':'binary','Comment':'','Name':cmd,"Type":"applications" })


    return apps

pickle_name = "/home/harindu/projects/launcher/apps.dump"
refresh =False

def load_pickle():
    global apps
    if os.path.isfile(pickle_name) :
        changed = os.path.getmtime(pickle_name)
        import calendar,time
        current = calendar.timegm(time.gmtime())
        if current - changed < 86500 :
            apps = pickle.load(open(pickle_name,"rb"))

def query(w,txt):
    global apps,refresh
    import re
    results = []
    firsts = []
    dump_pickle = True
    if len(apps) == 0 :
        apps = pickle.load(open(pickle_name,"rb"))
        dump_pickle =False

    if (len (apps) == 0 and dump_pickle) or refresh:        
        apps =  getLaunchers() + terminalCommands()
        print "refresh applications"
        pickle.dump(apps,open(pickle_name,"wb"))
        refresh = False

    txt = txt.lower()
    terms = txt.split(" ")
    pattern = ".*"
    for index,term in enumerate(terms):
        pattern += "[^\s]*".join([c for c in term])
        pattern += ".*\s?"

        
    pattern += ".*"
    # pattern ='.*'+'.*'.join([c for c in txt])
    pattern = re.compile(pattern)
    # widget =  QWidget()
    # "Exec":'','Icon':'','Comment':'' 
    for app in apps:
        # "Exec":'','Icon':'','Comment':'' 
        info = " " + app['Name'] + ' ' + app['Comment']
        info = info.lower()
        # if w.wk1.terminate:
        # break

        if re.match(pattern,info):
            if txt in app['Name'].lower():
                firsts.append(app)
            else:
                results.append(app)
                # return [app for app in apps if re.match(pattern,app['Info'])]
    return firsts + results



def execute(app,shift=False):
    import os
    # Popen(app['Exec'] + " &")
    print app['Exec']
    if shift:
        cmd = str('nohup x-terminal-emulator -e \"zsh -ci \''+app['Exec'] + ' ; exec zsh \'\" &')
        os.system(cmd)
    elif app["Exec"].startswith('/'):
        os.system('nohup ' + app["Exec"] + ' &')
    else:
        # print cmd
        # p= subprocess.Popen(["/usr/bin/nohup","zsh","-ci",app["Exec"]," &"])
        # os.spawn*(cmd)
        os.execv("/usr/bin/zsh",["zsh","-ci",app["Exec"]])

if __name__ == "__main__":
    print terminalCommands()
