#!/usr/bin/python2
# coding=utf-8

# Kindle Weather Display
# September 2012    Matthew Petroff (http://www.mpetroff.net/)
# April 2015        Alistair Bill
# February 2016     Marek Hobler 

import os 
import datetime
import codecs
import argparse

from pyowm import OWM

parser = argparse.ArgumentParser()
parser.add_argument('--owmkey', help='API key to http://openweathermap.org/', required=True)
parser.add_argument('--city', help='City', default='Wroclaw, PL')
args = parser.parse_args()

owm = OWM(language='en', API_key=args.owmkey, version='2.5')

icons = []
icons_parse = []
highs = []
lows = []
dates = []

forecast = owm.daily_forecast(args.city, limit=4).get_forecast()
for weather in forecast:
# Parse icons
    icons.append(weather.get_weather_code())
# Parse temperature highs
    highs.append(round(weather.get_temperature(unit='celsius')['max'], 1))
# Parse temperature lows
    lows.append(round(weather.get_temperature(unit='celsius')['min'], 1))
# Parse dates
    dates.append(weather.get_reference_time('iso')[:-12])


# Parse date
day_one = datetime.datetime.strptime(str(dates[0]), '%Y-%m-%d')

# Change icons from OWM format to the format the svg wants them in. This is
# really ugly code. I couldn't think of a better way to do it though, so for
# now it'll just stay like this. I'm sorry :'(

for item in icons:
    if item == 800:
        icons_parse.append('skc')
    elif item == 801:
        icons_parse.append('few')
    elif item == 802:
        icons_parse.append('sct')
    elif item == (803 or 771 or 762):
        icons_parse.append('bkn')
    
    elif item == (300 or 310 or 520):
        icons_parse.append('hi_shwrs')
    elif item == (301 or 302 or 311 or 312 or 313 or 314 or 321 or 521 or 522 or 531):
        icons_parse.append('shra')
    elif item == (200 or 210 or 221 or 230 or 231):
        icons_parse.append('scttsra')
    elif item == (201 or 202 or 211 or 212 or 232 or 960 or 961):
        icons_parse.append('tsra')
    
    elif item == 804:
        icons_parse.append('ovc')
    elif item == (500 or 501):
        icons_parse.append('ra')
    elif item == (502 or 503 or 504):
        icons_parse.append('hi_ra')
    elif item == (905 or 958 or 959):
        icons_parse.append('wind')
    elif item == 904:
        icons_parse.append('hot')
        
    elif item == 701:
        icons_parse.append('mist')
    elif item == 721:
        icons_parse.append('sctfg')
    elif item == 741:
        icons_parse.append('fg')
    elif item == 711:
        icons_parse.append('smoke')
    elif item == 761:
        icons_parse.append('du')
    elif item == (781 or 900):
        icons_parse.append('nsurtsra')
    
    elif item == 903:
        icons_parse.append('cold')
    elif item == (600 or 601):
        icons_parse.append('sn')
    elif item == 602:
        icons_parse.append('blizzard')
    elif item == (611 or 612):
        icons_parse.append('ip')
    
    elif item == (511 or 906):
        icons_parse.append('fzra')
    elif item == (620 or 621 or 622):
        icons_parse.append('mix')
    elif item == (615 or 616):
        icons_parse.append('rasn')
    else:
        icons_parse.append('sct')
        print ('Not recognised code')
        
print (icons_parse)

# Open SVG to process
output = codecs.open('weather-template.svg', 'r', encoding='utf-8').read()

# Insert icons and temperatures
output = output.replace('ICON_ONE',icons_parse[0]).replace('ICON_TWO',icons_parse[1]).replace('ICON_THREE',icons_parse[2]).replace('ICON_FOUR',icons_parse[3])
output = output.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
output = output.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))

# Insert days of week
one_day = datetime.timedelta(days=1)
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
output = output.replace('DAY_ONE',days_of_week[(day_one + 0*one_day).weekday()]).replace('DAY_TWO',days_of_week[(day_one + 1*one_day).weekday()]).replace('DAY_THREE',days_of_week[(day_one + 2*one_day).weekday()]).replace('DAY_FOUR',days_of_week[(day_one + 3*one_day).weekday()])

# Write output
codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)

os.system("rsvg-convert --background-color=white -o weather-script-output.png weather-script-output.svg")
os.system("pngcrush -c 0 -ow weather-script-output.png")

