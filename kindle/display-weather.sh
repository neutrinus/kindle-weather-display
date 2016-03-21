#!/bin/sh

cd "$(dirname "$0")"

#clear the display to avoid shadows
eips -c
eips -c

# Check battery capacity
BATTERY=`grep -o "[0-9]*" /sys/devices/system/yoshi_battery/yoshi_battery0/battery_capacity`
CURRENT=`cat /sys/devices/system/yoshi_battery/yoshi_battery0/battery_current`

if [ $BATTERY -le 10 ] && [ $CURRENT -le 0 ]; then
	# Show battery drained image
    eips -g battery-drained.png
else
	# Stop services to turn off screensavers and gui
	/etc/init.d/framework stop
	/etc/init.d/powerd stop
	# Remove old file
	rm weather-display.png
	# Download updated weather picture
	if wget "http://Your-Website-Domain/weather-display.png"; then
		eips -g weather-display.png
	else
		eips -g weather-error.png
	fi
fi

