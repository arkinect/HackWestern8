from weatherapi import WeatherPoint
# lat/lon for london ontario
latitude = 42.984270
longitude = -81.247530
key = "65313c4a8b1143c5bbb181802212011" #google API Key

point = WeatherPoint(latitude, longitude)

point.set_key(key)

point.get_current_weather()

def getTemp():
    return point.temp_c

def getPrecip():
    return point.precip_mm

