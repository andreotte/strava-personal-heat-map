#!python3
import getpass
import time
import json
import os
import re
import requests
import webbrowser
from requests.auth import HTTPBasicAuth, HTTPDigestAuth  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options

apiBase = "https://www.strava.com/api/v3/"
clientID = #Custom Input - Strava Client ID
client_secret = #Custom Input - Strava Client Secret
headers = '' 

driver = webdriver.Firefox(executable_path=r'C:\\Program Files\\Geckodriver\\geckodriver.exe') #Custom Input - local path to Selenium geckodriver

#returns parsed json as a dictionary
#params are a dictionary of params
def request(urlBase, request, params = None):
        url = apiBase + request
        response = requests.get(url, headers=headers, params=params)
        # print("request endpoint: ", request, " - ResponseCode: ", response.status_code)
        return response.json()

def authorizeStravaApp():
        oauthUrl = (f"https://www.strava.com/oauth/authorize?client_id={clientID}&"
                        "response_type=code&"
                        "redirect_uri=http://localhost/exchange_token&"
                        "approval_prompt=force&"
                        "scope=read,activity:read_all")

        driver.get(oauthUrl)
        print("What's happening?")
        print("Use Selenium to make a GET request to www.strava.com/oauth/authorize")
        print("\n")
        
        print("Hitting 'enter' POSTs to www.strava.com/oauth/token with 'client_id', 'client_secret', and 'code' parameters that was returned from the previous GET request")
        print("\n")
        someVariable = getpass.getpass("Press 'enter' after you are done logging in.") 
        
        print("You are logged in. Continuing script *beep bop boop*")
        print("\n")
        driver.find_element_by_id("authorize").click()
        url2 = driver.current_url.split('code=')
        code = url2[1].split('&scope')[0]

        data = {f'client_id':clientID,    
                'client_secret':client_secret, 
                'code':code,
                'grant_type':'authorization_code'}

        access_token = requests.post(url = "https://www.strava.com/oauth/token", data = data).json()['access_token']
        global headers 
        headers = {'Authorization': f'Bearer {access_token}'}
        driver.get("file:///C:/Personal/Strava/StravaActivities/loader.html")

def getActivityRoutes(page = 1, activityRoutes = []):
        timeStart = 0 #1970
        timeEnd = time.time() #Now

        params = {'after': timeStart, 'before': timeEnd, 'page': page}

        activityList = request(apiBase, "athlete/activities", params)
        # print(activityList)
        # if page < 2: # uncomment this for testing to keep the request short
        if len(activityList) > 0: #comment this line out for testing to keep it short.
                for activity in activityList:
                        if activity["map"]["summary_polyline"]:
                                activityRoutes.append(activity["map"]["summary_polyline"])
                
                print(len(activityRoutes), "routes found")
                return getActivityRoutes(page + 1, activityRoutes)
        else:
                return activityRoutes
        # else: # uncomment this for testing to keep the request short
        #      return activityRoutes #for testing  
def main():
        authorizeStravaApp() 

        print("What is happening?")
        print("We are making a bunch of requests to https://www.strava.com/api/v3/athlete/activities, which returns routes with encoded polylines in batches of ~30. The route polyline strings are being written to a JS file to create an array. This array will be used to populate a map using Mapbox and leaflet.js. When all the polylines have been parsed, Selenium will open map.html.") 
        print("\n")
        activityRoutes = getActivityRoutes()

        file = open("activities.js","w")
        file.write(f'let routes = [')
        file.write('\n')
        i = 1
        for activityRoute in activityRoutes:
                activityRoute = activityRoute.replace("\\", "\\\\")
                file.write(f'"{activityRoute}",\n')
                i += 1
        file.write('];')
        file.close()

        driver.get("") #Custom Input - local path to StravaActivities/map.html
if __name__ == '__main__':
    main()

 