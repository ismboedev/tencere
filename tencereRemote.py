#!/bin/python

from subprocess import Popen, PIPE
import time

# define function to send keys to a window in list
def sendkey( list, str ):
    for i in range( 0, len(list) ):
        Popen( 'xdotool key --window ' + list[i] + ' ' + str, shell=True,
                universal_newlines=True )


# search and return a list, of window ids of urxvt
urxvt = Popen( 'xdotool search --class urxvt', shell=True,
        universal_newlines=True, stdout=PIPE ).communicate()[0].splitlines()


# execute cec-command and listen to remote input on TV
# send different keystrokes on each event.
with Popen('cec-client', stdout=PIPE, universal_newlines=True) as cec:
    
    for line in cec.stdout:

        # search and return a list, of window ids of urxvt
        urxvt = []
        urxvt = Popen( 'xdotool search --class urxvt', shell=True,
                universal_newlines=True, stdout=PIPE ).communicate()[0].splitlines()

        
        # reboot of the system on red keypress on remote
        if 'key pressed: F2' in line and 'duration' in line:
            Popen( 'systemctl reboot', shell=True, universal_newlines=True )
            continue

        # restart tty1 on blue keypress on remote
        if 'key pressed: F5' in line and 'duration' in line:
            Popen( 'pkill -9 bspwm', shell=True, universal_newlines=True )
            continue

        # channel up 
        if 'key pressed: channel up' in line and 'duration' in line:
            sendkey( urxvt, "w" )
            time.sleep(0.5)
            continue

        # channel down
        if 'key pressed: channel down' in line and 'duration' in line:
            sendkey( urxvt, "s" )
            time.sleep(0.5)
            continue

        # channels selection
        if 'key pressed: channels list' in line and 'duration' in line:
            sendkey( urxvt, "l" )
            time.sleep(0.5)
            continue

        # previous channel
        if 'key pressed: pre' in line and 'duration' in line:
            sendkey( urxvt, "p" )
            time.sleep(0.5)
            continue

        # guide key to regenerate streamlink urls
        if 'key pressed: electronic' in line and 'duration' in line:
            sendkey( urxvt, "g" )
            time.sleep(0.5)
            continue

        # selecting a channel
        if 'key pressed: select' in line and 'duration' in line:
            sendkey( urxvt, "Return" )
            time.sleep(0.5)
            continue

        # going up in list
        if 'key pressed: up' in line and 'duration' in line:
            sendkey( urxvt, "Up" )
            time.sleep(0.5)
            continue

        # going down in list
        if 'key pressed: down' in line and 'duration' in line:
            sendkey( urxvt, "Down" )
            time.sleep(0.5)
            continue

        # press exit to stop the player
        if 'key pressed: exit' in line and 'duration' in line:
            sendkey( urxvt, "e" )
            time.sleep(0.5)
            continue

        # stop does nothing
        if 'key pressed: stop' in line and 'duration' in line:
            sendkey( urxvt, "t" )
            time.sleep(0.5)
            continue

        # green key cycles through the sources for that channel
        if 'key pressed: F3' in line and 'duration' in line:
            sendkey( urxvt, "c" )
            time.sleep(0.5)
            continue

        # when TV is powered off
        if 'power status changed from \'on'in line:
            sendkey( urxvt, "q" )
            time.sleep(0.5)
            continue
