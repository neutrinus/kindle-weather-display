#!/usr/bin/python2
# coding=utf-8

# Kindle Weather Display
# Matthew Petroff (http://mpetroff.net/)
# September 2012

import json
import datetime
import codecs
try:
    # Python 3
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib2 import urlopen

#
# Geographic location
#

city = 'Aachen'

#
# Download and parse weather data
#

url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' + city + '&mode=json&units=metric&cnt=4'

# Fetch data (change lat and lon to desired location)
weather_json = urlopen(url).read()
data = json.loads(weather_json)

icon_mappings = {
    '01d': 'skc',      # Clear, sky is clear
    '02d': 'few',
    '03d': 'sct',
    '04d': 'ovc',
    '09d': 'ra',
    '10d': 'hi_shwrs', # Rain, light rain
    '11d': 'tsra',
    '13d': 'sn',
    '50d': 'fg',
}

highs = []
lows = []
icons = []
for day in data['list']:
    hi = int(round(float(day['temp']['max'])))
    lo = int(round(float(day['temp']['min'])))
    highs.append(hi)
    lows.append(lo)
    icons.append(icon_mappings[day['weather'][0]['icon']])

## Parse icons
#xml_icons = dom.getElementsByTagName('icon-link')
#icons = [None]*4
#for i in range(len(xml_icons)):
#    icons[i] = xml_icons[i].firstChild.nodeValue.split('/')[-1].split('.')[0].rstrip('0123456789')

# Parse dates
day_one = datetime.datetime.fromtimestamp(data['list'][0]['dt'])
today = datetime.datetime.now()

#print(day_one)
#print(highs)
#print(lows)
#print(icons)

#
# Preprocess SVG
#

# Open SVG to process
output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()

output = output.replace('UPDATE', "updated " + today.strftime("%H:%M"))
output = output.replace('DATE', day_one.strftime("%d.%m.%Y"))

# Insert icons and temperatures
output = output.replace('ICON_ONE',icons[0]).replace('ICON_TWO',icons[1]).replace('ICON_THREE',icons[2]).replace('ICON_FOUR',icons[3])
output = output.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
output = output.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))

# Insert days of week
one_day = datetime.timedelta(days=1)
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
output = output.replace('DAY_THREE',days_of_week[(day_one + 2*one_day).weekday()]).replace('DAY_FOUR',days_of_week[(day_one + 3*one_day).weekday()])

# Write output
codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)
