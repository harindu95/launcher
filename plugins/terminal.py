
def query(txt):
    result = { "Name":"Terminal","Comment":"Open in Terminal","Command":txt,"Type":"terminal"}
    result['Icon'] = 'terminal'
    return result

def execute(command,shift=False):
    import os
    # Popen(app['Exec'] + " &")
    # x-terminal-emulator -e "zsh -c \"apropos editor; exec zsh\""
    if shift:
        cmd = str('nohup x-terminal-emulator -e \"zsh -ci \''+command["Command"] + ' ; exec zsh \'\" &')
    else:
        cmd = str('nohup zsh -ci \''+command["Command"] + ' ; exec zsh \' &')

    print cmd 
    os.system(cmd)

