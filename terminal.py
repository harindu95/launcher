import applications

def query(txt):
    result = { "Name":"Terminal","Comment":"Open in Terminal","Command":txt,"Type":"terminal"}
    result['Icon'] = applications.icon_fullpath('terminal')
    return result

def execute(command):
    import os
    # Popen(app['Exec'] + " &")
    # x-terminal-emulator -e "zsh -c \"apropos editor; exec zsh\""
    cmd = str('nohup zsh -ci \''+command["Command"] + ' ; exec zsh \' &')
    print cmd 
    os.system(cmd)

