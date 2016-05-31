# Weatherstation on Kindle4
This is just bunch of scripts that generate PNG image with weather forecast and display them on kindle. Because kindle doesn't have python, you need separate machine to generate the images, then serve them via HTTP.

You will need API key for weather service (http://openweathermap.org/) - it's free, just need to register.

## Got r00t?
Great "tutorial" to root your kindle and activate ssh:

http://wiki.mobileread.com/wiki/Kindle4NTHacking

## Installation
```
scp -r ./kindle/* root@10.252.1.52:~/
ssh root@kindle
mntroot rw
./init-weather.sh
```

## Generate new image

```
python ./server/weather-script.py --owmkey XXX
```


## Influenced by
This is the code to generate a status information / weather forecast image to be displayed on a Kindle.
Read more [in the blog post](http://fnordig.de/2015/05/14/using-a-kindle-for-status-information/)

Original: <http://www.mpetroff.net/archives/2012/09/14/kindle-weather-display/>
