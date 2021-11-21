def findClosestHospital(borough):
    import googlemaps
    import requests
    import json

    API_KEY = "AIzaSyB_2mjewoh1OYU0wyaOkIseKMTvnJFszgY"
    CITY = "%20London%20Ontario"
    googlemaps.Client(API_KEY)
    # boroughsText = open("boroughs.txt", "r", encoding="utf-8")
    hospitalsText = open("hospitals.txt", "r", encoding="utf-8")
    headers = {}
    payload = {}
    # boroughsHospitals = {}
    closestHospital = ['', 2**100]
    for hospital in hospitalsText:
        origin = borough.replace(" ", "%20") + CITY
        destination = hospital.replace(" ", "%20") + CITY
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&units=imperial&key={}".format(origin, destination, API_KEY)
        response = requests.request("GET", url, headers=headers, data=payload)
        timeToHospital = json.loads(response.text)["rows"][0]["elements"][0]["duration"]["value"]
        if timeToHospital < closestHospital[1]:
            closestHospital[1] = timeToHospital
            closestHospital[0] = hospital.strip("\n ")
    hospitalsText.close()
    return closestHospital[0].strip("\n ")
    # hospitalsText.seek(0)


def calcERTripsPerDay(multiplier):
    tripsPer100PA = 40.4
    tripsPerPersonPA = tripsPer100PA/100
    tripsPerPersonPerDay = tripsPerPersonPA/365
    return tripsPerPersonPerDay*multiplier  # model has a tendency to overestimate in our opinion. Needs to be tested

def returnFinalUniCount(socialActivityMultiplier, hospitalToRet):
    # open text files
    boroughsText = open("boroughs.txt", "r", encoding="utf-8")
    hospitalsText = open("hospitals.txt", "r", encoding= "utf-8")
    londonPopCSV = open("LondonPop.csv", "r", encoding= "utf-8")

    # define vars, and create empty lis
    percentOfStudentsWhoDontDrink = 0.2
    # socialActivityMultiplier = 1
    countYouthPerHospital = {}
    for hospital in hospitalsText:
        countYouthPerHospital[hospital.strip("\n ")] = 0

    # population data into complex dict
    boroughPops = {}
    for row in londonPopCSV:
        data = row.split(",")
        boroughPops[data[0]] = []
        for entries in data:
            boroughPops[data[0]].append(entries.strip("\n "))
    # remove some lines from CSV that shouldn't be processed
    boroughPops.pop("\ufeffDistrict")
    boroughPops.pop("")
    boroughPops.pop("Totals")

    # sum all uni aged residents to the appropriate hospital
    for borough in boroughsText:
        countYouthPerHospital[findClosestHospital(borough)] += int(boroughPops[borough.strip("\n ")][7])
    # adjust sum for students who don't drink
    # adjust sum for one day of active social events
    for i in countYouthPerHospital:
        countYouthPerHospital[i] *= (1-percentOfStudentsWhoDontDrink)
        countYouthPerHospital[i] *= calcERTripsPerDay(socialActivityMultiplier)
        countYouthPerHospital[i] = int(countYouthPerHospital[i])
    # print(countYouthPerHospital)
    boroughsText.close()
    hospitalsText.close()
    londonPopCSV.close()
    return (countYouthPerHospital[hospitalToRet])

# returnFinalUniCount()
