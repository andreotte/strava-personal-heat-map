#!python3
import time
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth     

urlBase = "https://www.strava.com/api/v3/"
headers = {'Authorization': 'Bearer 2c42930e9ab59b5452b510f0a68a8587e8347b3e'}

#returns parsed json as a dict
#params are ia dict or params
def request(request, params = None):
        url = urlBase + request
        response = requests.get(url, headers=headers, params=params)   # modify request headers 
        print(request, " - ResponseCode: ", response.status_code)
        return response.json()

def getAthlete():
        athlete = request("athlete")
        print(athlete["id"])        

def getActivityRoutes(page = 1, activityRoutes = []):
        timeStart = 0 #1970
        timeEnd = time.time() #Now

        params = {'after': timeStart, 'before': timeEnd, 'page': page}

        activityList = request("athlete/activities", params)

        # if page < 2: #for testing
        if len(activityList) > 0: #this is what we need. but we are commenting it out to keep it short.
                for activity in activityList:
                        if activity["map"]["summary_polyline"]:
                                activityRoutes.append(activity["map"]["summary_polyline"])
                
                return getActivityRoutes(page + 1, activityRoutes)
        else:
                print(len(activityRoutes), "routes found")
                return activityRoutes

# def writeAvtivityRouteToFile(activityRoute, routeNumber):
#         file = open("Activities.txt","a")
#         file.write(f'let route{routeNumber} = "{activityRoute}"')
#         file.write('\n')
#         file.close() 


def main():
        activityRoutes = getActivityRoutes()
        file = open("Activities.txt","a")
        file.write(f'let routes = [')
        file.write('\n')
        i = 1
        for activityRoute in activityRoutes:
                file.write(f'"{activityRoute}",\n')
                i += 1
        file.write('];')
        file.close() 

        
        # getAthlete()

if __name__ == '__main__':
    main()

 