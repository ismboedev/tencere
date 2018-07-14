#!/bin/python

import time
from streamlink import Streamlink
import yaml
import urwid


# print into a logfile for debugging, or to have a live overvier whats
# happening
def printlog( str ):
    with open( 'tenc.log', mode='a' ) as log:
        now = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        log.write("[" + now + "]" + "\t " + str + "\n")


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


# def urwid menu and functions.
def menu( title, ch_list ):
    body = [urwid.Text( title, 'center'), urwid.Divider() ]
    for i in range( 0, len(ch_list) ):
        if ( i < 10 ):
            fil1 = "0"
            fil2 = "   "
        else:
            fil1 = ""
            fil2 = "  "
        button = urwid.Button( fil1 + str(i) + fil2 + ch_list[i].name )
        urwid.connect_signal( button, 'click', ch_selected, i )
        body.append( urwid.AttrMap( button, None, focus_map='reversed' ) )
    return urwid.ListBox( urwid.SimpleFocusListWalker( body ) )


# this starts the selected channel
def ch_selected( button, sel ):
    if sel == 0:
        printlog( "selected first one" )


# this function is controlling everything
def inp( key ):
    if key in ('q', 'Q'):
        printlog( "exiting tencere" )
        raise urwid.ExitMainLoop()


# read channels from tvsources.yaml
ch_list = []
with open("tvsources.yaml", 'r') as ts:
    for data in yaml.load_all( ts ):
        ch_list.append( Channel(data) )



printlog("starting menu ...")
main = urwid.Padding( menu( u'channels', ch_list ), left=4, right=4 )

top = urwid.Overlay( main, urwid.SolidFill( u'\N{MEDIUM SHADE}' ),
    align='center', width=( 'relative', 70 ),
    valign='middle', height=( 'relative', 70 ),
    min_width=20, min_height=9 )

men = urwid.MainLoop( top, unhandled_input=inp, palette=[('reversed', 'standout, dark green, italics', '')])
men.run()
