#!/bin/sh

cd "$(dirname "$0")"

rm -f display.png && \
python2 weather-script.py && \
rsvg-convert --background-color=white -o weather-script-output.png weather-script-output.svg && \
pngcrush -c 0 -ow weather-script-output.png #&& \
#cp -f weather-script-output.png /path/to/web/server/directory/weather-script-output.png
