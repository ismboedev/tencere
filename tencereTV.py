#!/bin/python

import yaml
from streamlink import Streamlink
import time


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

    


# read channels from tvsources.yaml
ch_list = []

with open("tvsources.yaml", 'r') as ts:
    for data in yaml.load_all( ts ):
        ch_list.append( Channel(data) )

print(ch_list)

for i in range(0, len(ch_list) ):
    #ch_list[i].getURLs
    print( ch_list[i].URLs )
