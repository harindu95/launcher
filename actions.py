import applications
def query(txt):
    actions = [ { 'Name': "Suspend" ,'Comment':'Suspend the machine' ,'cmd' : 'systemctl suspend -i' , 'Icon':applications.icon_fullpath('system-suspend'),"Type":"actions"},
                { 'Name': "Vlc Next" ,'Comment':'Play next track' ,'cmd':"dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next" , 'Icon' :'',"Type":"actions"},
                { 'Name': "Vlc Prev" ,'Comment':'Play previous track', 'cmd':"dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.previous" , 'Icon' :'',"Type":"actions"},
                { 'Name': "Vlc Play/Pause" ,'Comment':'Play/Pause the track', 'cmd':"dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause" ,'Icon':"","Type":"actions"}
                ,{ 'Name': "Shutdown" ,'Comment':'Power off the machine' ,'cmd' : 'systemctl poweroff' , 'Icon':applications.icon_fullpath('system-shutdown'),"Type":"actions"},
    ]

    txt = txt.lower().replace(' ','')
    results = []
    for action in actions:
        info = action['Name'] + action['Comment']
        info = info.lower().replace(' ','')
        
        if txt in info:
            results.append(action)

    return results

def execute(cmd):
    import os
    command = 'nohup ' + cmd['cmd'] + ' &'
    os.system(command)


