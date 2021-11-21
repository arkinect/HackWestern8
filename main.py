from install_Packages import*
from math import*
import datetime as dt
import mapsdistance as md
import json

volume = int(input("Enter Average volume of patients in any given day: "))
hospital = input("Which london hospital are you calculating for? (university, victoria , st joseph): ") + " hospital"
tempDate = str(dt.date.today())
tempDate = tempDate[tempDate.find("-")+1:]
date = {"month":int(tempDate[:tempDate.find("-")]),"day":int(tempDate[tempDate.find("-")+1:]),"weekday":dt.date.today().weekday()}
holidays = {12:[30,25,26],1:[1],5:[24],7:[1],9:[6],10:[11]} # study citation
WesternEvents = 0
# function uses data from https://www.cihi.ca/sites/default/files/document/improving_health_system_efficiency_in_canada_description_methods_en.pdf
def checkPrecip(volume, hospital):
    tempVolume = volume
    precip = getPrecip()
    if precip >= 50:
        tempVolume -= tempVolume*0.032
    elif precip >= 10:
        tempVolume -= tempVolume*0.0265
    elif precip > 0:
        tempVolume -= tempVolume*0.0177
    return tempVolume

# function uses data from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3738307/
def checkTemp(volume, hospital):
    tempVolume = volume
    temperature = getTemp()
    if temperature >29:
        for i in range(ceil(temperature-29)):
            tempVolume += tempVolume*0.045
    elif 8.2 < temperature < 26.9:
        for i in range(27,temperature,-1):
            tempVolume += tempVolume*0.014
    return tempVolume

def checkHoliday(volume, hospital):
    tempVolume = volume
    for month in holidays:
        if date["month"] == month:
            if date["day"] in holidays[month]:
                tempVolume+=tempVolume*0.12
    return tempVolume

def checkWeekday(volume, hospital):  # eventually this would be expanded to incorporate uni calendars to account for exam periods, and events
    if date["weekday"]==0:  # monday
        social = 0
    elif date["weekday"]==1:  # tuesday
        social = 0
    elif date["weekday"]==2:  # wednesday
        social = 0
    elif date["weekday"]==3:  # thursday100
        social = 0.5
    elif date["weekday"]==4:  # friday
        social = 1
    elif date["weekday"]==5:  # saturday
        social = 1
    elif date["weekday"]==6:  # sunday
        social = 0.6
    return md.returnFinalUniCount(social, hospital)


def main(volume, hospital):
    volume = checkPrecip(volume, hospital)
    volume = checkTemp(volume, hospital)
    volume = checkHoliday(volume, hospital)
    volume += checkWeekday(volume, hospital)
    # json_formatted_str = json.dump("The estimated volume is " + str(int(volume)))
    # print("The estimated volume is",int(volume))
    # print(json_formatted_str)
    return volume

print(main(volume, hospital))
