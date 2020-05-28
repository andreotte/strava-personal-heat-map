#!python3
import getpass
import time
import json
import os
import requests
import webbrowser
from requests.auth import HTTPBasicAuth, HTTPDigestAuth  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options

apiBase = "https://www.strava.com/api/v3/"
# headers = {'Authorization': 'Bearer abc'} #the bearer comes from authorization post

#returns parsed json as a dict
#params are a dict of params
def request(urlBase, request, params = None):
        url = apiBase + request
        response = requests.get(url, headers=headers, params=params)   # modify request headers 
        print(request, " - ResponseCode: ", response.status_code)
        return response.json()

def parseAuthBearer(url):
        url2 = url.split('code=')
        bearer = url2[1].split('&scope')[0]

def authorizeStravaApp():
        clientID = #add strava ClientID here
        oauthUrl = (f"https://www.strava.com/oauth/authorize?client_id={clientID}&"
                        "response_type=code&"
                        "redirect_uri=http://localhost/exchange_token&"
                        "approval_prompt=force&"
                        "scope=read,activity:read_all")

        driver = webdriver.Firefox(executable_path=r'C:\\Program Files\\Geckodriver\\geckodriver.exe') #might need to change this path to geckodriver
        driver.get(oauthUrl)
        
        someVariable = getpass.getpass("Press Enter after You are done logging in") 
        print("You are logged in. Continuing script *beep bop boop*")
        
        driver.find_element_by_id("authorize").click()
        url2 = driver.current_url.split('code=')
        return url2[1].split('&scope')[0]

def getAthlete():
        athlete = request(apiBase, "athlete")
        print(athlete["id"])        

def getActivityRoutes(page = 1, activityRoutes = []):
        timeStart = 0 #1970
        timeEnd = time.time() #Now

        params = {'after': timeStart, 'before': timeEnd, 'page': page}

        activityList = request(apiBase, "athlete/activities", params)

        # if page < 2: #for testing
        if len(activityList) > 0: #comment this line out fortesting to keep it short.
                for activity in activityList:
                        if activity["map"]["summary_polyline"]:
                                activityRoutes.append(activity["map"]["summary_polyline"])
                
                return getActivityRoutes(page + 1, activityRoutes)
        else:
                print(len(activityRoutes), "routes found")
                return activityRoutes

def main():
        bearer = authorizeStravaApp()
        headers = {'Authorization': f'Bearer {bearer}'} #the bearer comes from authorization post
        # print(headers)
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

if __name__ == '__main__':
    main()

 