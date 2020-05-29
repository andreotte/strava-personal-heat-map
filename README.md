# strava-personal-heat-map
Strava personal heatmap. Display Strava activities on a map using Python, Selenium, and Mapbox. This is a WIP.

#Things you need to get this running:
1. A Strava API Application, which will provide you with a Client ID and a Client Secret
2. A Mapbox public token
3. Python3 installed
4. GeckoDriver for Selenium installed

#To run the program all you need to do is run main.py. This will open FireFox and you will be prompted to log in to Strava.
Once logged in, hitting 'enter' will continue the script. When all the activities have been pulled and parsed from the API, 
a map will open with all your activities. 

#See demo.mp4 for a demonstration of the program running.

#Future goals:
- Put a front-end on it.
- Clean up main.py to stop using globals.
- Get the routes to snap to roads. This will be especially challenging if accomodating to activities on trails.
