# tencere

## Description

*tencere* is just a simple tool, that simulates the experience of a satellite
receiver or a cable subscription. It can be controlled with the TV remote over
hdmi-cec on compatible devices.  
It is primarily written to run on a raspberry pi 3.


## how it works

*tencere* consists of two scripts. The first one `tencereRemote.py` listens to
the hdmi-cec input and sends virtual keystrokes to a terminal window (here urxvt)
in wich the second script `tencereTV.py` with urwid gui is running.

`tencereTV.py` is taking care of the channels list, the mpv instance and the
changing of channels. The channels are imported from a file specified in
`tencereTV.py`, which is by default `tvsources.yaml` in the same path as the script.
`tvsouces.yaml` has to have the following form:

```
---
ch_name: "channel 1"
sources: 
        - "http://www.source.one.com"
        - "www.alternative.source.de"
---
ch_name: "channel 2"
sources:
        - "first.source.com.tr"
        - "http://www.more.than.two.sources.possible.uk"
        - "www.infact.infinite.sources.possible.to"
...
```

The sources are handled by streamlink, so that you can put the link to the
website which has the stream embedded into it, instead of the direct streaming-url.


## dependencies

- python 3
- [urwid](https://github.com/urwid/urwid) (for cli)
- [libcec](https://github.com/Pulse-Eight/libcec) (for hdmi-cec remote control)
- mpv
- [streamlink](https://github.com/streamlink/streamlink) (for getting the streaming url from websites with videos)
- [python-libxdo](https://github.com/rshk/python-libxdo) (and of course xdotool for that)
- [rxvt-unicode](http://software.schmorp.de/pkg/rxvt-unicode.html)


## raspberry-pi

*tencere* runs smoothly on a raspberry pi 3, if mpv is compiled with hardware acceleration.


## why?

I had to remove the satellite dish and was looking for a simple way to watch TV
over the internet. Kodi was an option, but was too slow for my taste and it has
too many features.

### name

The turkish word for *dish* as in *satellite dish* is *çanak* wich on it's own
means *bowl* in english. I just took another kitchen utensil: *pot*, wich in
turkish means *tencere*.