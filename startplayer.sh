#!/bin/sh

while true; do
	mpv --idle=yes --input-ipc-server=/tmp/mpvsocket --volume=100 --osd-duration 10000 --osd-font-size=150 --osd-color='#00FF00' --osd-align-x=right --osd-align-y=center --loop-file=inf --no-input-default-bindings
	sleep 1s
done
