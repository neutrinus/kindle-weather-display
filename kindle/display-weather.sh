#!/bin/sh

cd "$(dirname "$0")"

rm -f display.png
eips -c
eips -c

if wget -q http://server/path/to/display.png; then
	eips -g display.png
else
	eips -g weather-image-error.png
fi
