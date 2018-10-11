#!/bin/sh

while true; do
	#mpv --idle=yes --input-ipc-server=/tmp/mpvsocket --volume=100 --osd-duration 10000 --osd-font-size=150 --osd-color='#00FF00' --osd-align-x=right --osd-align-y=center --loop-file=inf --no-input-default-bindings
	omxplayer --nohdmiclocksync --no-keys --timeout 30 --layer 1 --threshold 5 $(head /home/aile/tencere/currChUrl.txt)
	sleep 0.2s
done
