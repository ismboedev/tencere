#!/bin/python

from subprocess import Popen, PIPE
from xdo import Xdo

# define function to send keys to a window in list
def sendkey( list, str ):
    for i in range( 0, len(list) ):
        xdo.send_keysequence_window( list[i], str.encode(), delay=10 )


# start xdo and search for window urxvt

xdo = Xdo()
# search return a list, of window ids of urxvt
urxvt = xdo.search_windows( winclass=str.encode( "urxvt" ) )


# execute cec-command and listen to remote input on TV
# send different keystrokes on each event.
with Popen('cec-client', stdout=PIPE, universal_newlines=True) as cec:
    
    for line in cec.stdout:
        
        # reboot of the system on red keypress on remote
        if 'key pressed: F2' in line and 'duration' in line:
            Popen( 'systemctl reboot', shell=True, universal_newlines=True )
            continue

        # channel up 
        if 'key pressed: channel up' in line and 'duration' in line:
            sendkey( urxvt, "w" )
            continue

        # channel down
        if 'key pressed: channel down' in line and 'duration' in line:
            sendkey( urxvt, "s" )
            continue

        # channels selection
        if 'key pressed: channels list' in line and 'duration' in line:
            sendkey( urxvt, "l" )
            continue

        # previous channel
        if 'key pressed: pre' in line and 'duration' in line:
            sendkey( urxvt, "p" )
            continue

        # guide key to regenerate streamlink urls
        if 'key pressed: electronic' in line and 'duration' in line:
            sendkey( urxvt, "g" )
            continue

        # press exit to stop the player
        if 'key pressed: exit' in line and 'duration' in line:
            sendkey( urxvt, "e" )
            continue

        # stop does nothing
        if 'key pressed: stop' in line and 'duration' in line:
            sendkey( urxvt, "t" )
            continue

        # green key cycles through the sources for that channel
        if 'key pressed: F3' in line and 'duration' in line:
            sendkey( urxvt, "c" )
            continue

        # when TV is powered off
        if 'power status changed from \'on'in line:
            sendkey( urxvt, "q" )
            continue
