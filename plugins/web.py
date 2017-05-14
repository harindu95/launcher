
def query(txt):
    result = { "Name":"Web","Comment":"Start search in your browser","Command":txt,"Type":"web"}
    result['Icon'] = 'browser'
    return [result]

def execute(command,shift=False):
    import os
    # Popen(app['Exec'] + " &")
    # x-terminal-emulator -e "zsh -c \"apropos editor; exec zsh\""
    engine = "https://www.startpage.com/do/dsearch?query="
    cmd = str('nohup firefox -new-tab \'' +engine +command["Command"] + '\' &')
    print cmd 
    os.system(cmd)
