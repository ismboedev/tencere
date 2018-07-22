#!/bin/python

import time
from streamlink import Streamlink
import yaml
from subprocess import Popen, PIPE
import urwid


# print into a logfile for debugging, or to have a live overvier whats
# happening
def printlog( str ):
    with open( 'tenc.log', mode='a' ) as log:
        now = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        log.write("[" + now + "]" + "\t " + str + "\n")
    return 0




# define channel class, that gets streamlink urls at init
class Channel:

    def __init__( self, data ):
        self.name = data[ 'ch_name' ]
        self.sources = data[ 'sources' ]
        # iterator to cycle through URLs. at first it is equal to the first
        # working url
        self.iterator = len( self.sources) - 1
        # list of URLs from streamlink
        self.URLs = []
        # fill with nosource file
        for i in range( 0, len(self.sources) ):
            self.URLs.append( 'nosource.mp4' )
        self.getURLs()

    def getURLs(self):
        streamlink = Streamlink()
        printlog("------ \t " + self.name + "\t ------" )
        self.iterator = len( self.sources) - 1
        for i in range( 0, len(self.sources) ):
            try:
                self.URLs[i] = streamlink.streams( self.sources[i] )['best'].url
                if ( i < self.iterator ):
                    self.iterator = i
                printlog( "source " + str(i) + "\t OK" )
            except:
                printlog( "source " + str(i) + "\t //" )
                #self.URLs.append( 'nosource.mp4' )
        return 0

    def url(self):
        return self.URLs[self.iterator]





# class mpv
class Mpv:

    load1 = str( "echo \'{ \"command\": [\"loadfile\", \"" )
    show1 = str( "echo \'{ \"command\": [\"show-text\", \"" )
    stop1 = str( "echo \'{ \"command\": [\"stop" )
    com2 = str( "\"] }\' | socat - /tmp/mpvsocket" )

    def __init__( self ):
        # start mpv player in background and give it some time to start
        # listening to /tmp/mpvsocket
        #try:
        #    call( 'pkill startplayer.sh && pkill mpv', shell=True, universal_newlines=True )
        #except:
        #    printlog( "no previous MPV to kill" )

        #Popen( './startplayer.sh', stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True )
        printlog( "init MPV player" )
        #time.sleep( 2 )

    def load( self, str ):
        x = "%s%s%s" % ( self.load1, str, self.com2 )
        Popen( x, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True )
        time.sleep( 1 )
        return 0

    def show( self, str ):
        x = "%s%s%s" % ( self.show1, str, self.com2 )
        Popen( x, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True )
        return 0

    def stop( self ):
        x = "%s%s" % ( self.stop1, self.com2 )
        Popen( x, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True )
        return 0







# def urwid menu and functions.
def menu( title, ch_list ):
    body = [urwid.Text( title, 'center'), urwid.Divider() ]
    for i in range( 0, len(ch_list) ):
        if ( i < 9 ):
            fil1 = "0"
            fil2 = "   "
        else:
            fil1 = ""
            fil2 = "  "
        button = urwid.Button( fil1 + str( i + 1 ) + fil2 + ch_list[i].name )
        urwid.connect_signal( button, 'click', ch_selected, i )
        body.append( urwid.AttrMap( button, None, focus_map='reversed' ) )
    return urwid.ListBox( urwid.SimpleFocusListWalker( body ) )




# introduce variables
curr_ch = 0
temp_ch = 0
pre_ch = 0






# this starts the selected channel
def ch_selected( button, sel ):
    global curr_ch
    global temp_ch
    global pre_ch
    pre_ch = curr_ch
    curr_ch = sel
    printlog( "Channel " + str(curr_ch) + " - " + ch_list[curr_ch].name + "  -  source: " + str( ch_list[curr_ch].iterator ) )
    mpv.load( ch_list[curr_ch].url() )
    mpv.show( str( curr_ch + 1 ) )


# this function is controlling everything
def inp( key ):
    global curr_ch
    global temp_ch
    global pre_ch
    # quit
    #if key in ( 'q', 'Q' ):
    #    printlog( "exiting tencere" )
    #    raise urwid.ExitMainLoop()

    if key in ( 'q', 'Q' ):
        mpv.stop()


    # ch up
    if key in ( 'w', 'W' ):
        pre_ch = curr_ch
        curr_ch = ( curr_ch + 1 + len( ch_list ) ) % len( ch_list )
        printlog( "Channel " + str(curr_ch) + " - " + ch_list[curr_ch].name + "  -  source: " + str( ch_list[curr_ch].iterator ) )
        mpv.load( ch_list[curr_ch].url() )
        mpv.show( str( curr_ch + 1 ) )

    # ch down
    if key in ( 's', 'S' ):
        pre_ch = curr_ch
        curr_ch = ( curr_ch - 1 + len( ch_list ) ) % len( ch_list )
        printlog( "Channel " + str(curr_ch) + " - " + ch_list[curr_ch].name + "  -  source: " + str( ch_list[curr_ch].iterator ) )
        mpv.load( ch_list[curr_ch].url() )
        mpv.show( str( curr_ch + 1 ) )

    # channels list
    if key in ( 'l', 'L' ):
        mpv.stop()

    # previous channel
    if key in ( 'p', 'P' ):
        temp_ch = curr_ch
        curr_ch = pre_ch
        pre_ch = temp_ch
        printlog( "Channel " + str(curr_ch) + " - " + ch_list[curr_ch].name + "  -  source: " + str( ch_list[curr_ch].iterator ) )
        mpv.load( ch_list[curr_ch].url() )
        mpv.show( str( curr_ch + 1 ) )

    # refresh URLs
    if key in ( 'g', 'G' ):
        mpv.stop()
        printlog( "Refreshing sources" )
        for i in range( 0, len(ch_list) ):
            ch_list[i].getURLs()
        printlog( "Channel " + str(curr_ch) + " - " + ch_list[curr_ch].name + "  -  source: " + str( ch_list[curr_ch].iterator ) )
        mpv.load( ch_list[curr_ch].url() )
        mpv.show( str( curr_ch + 1 ) )

    # exit mpv, show list
    if key in ( 'e', 'E' ):
        mpv.stop()

    # change source
    if key in ( 'c', 'C' ):
        ch_list[curr_ch].iterator = ( ch_list[curr_ch].iterator + 1 + \
                len( ch_list[curr_ch].sources ) ) % len( ch_list[curr_ch].sources )
        printlog( "Channel " + str(curr_ch) + " - " + ch_list[curr_ch].name + "  -  source: " + str( ch_list[curr_ch].iterator ) )
        mpv.load( ch_list[curr_ch].url() )
        mpv.show( str( curr_ch + 1 ) )

    time.sleep( 1 )

    


# read channels from tvsources.yaml
ch_list = []
with open("tvsources.yaml", 'r') as ts:
    for data in yaml.load_all( ts ):
        ch_list.append( Channel(data) )



# start MPV
mpv = Mpv()





# start mainloop with urwid
printlog("starting menu ...")
main = urwid.Padding( menu( u'channels', ch_list ), left=4, right=4 )

top = urwid.Overlay( main, urwid.SolidFill( u'\N{MEDIUM SHADE}' ),
    align='center', width=( 'relative', 70 ),
    valign='middle', height=( 'relative', 70 ),
    min_width=20, min_height=9 )

men = urwid.MainLoop( top, unhandled_input=inp, palette=[('reversed', 'standout, dark green, italics', '')])
men.run()
