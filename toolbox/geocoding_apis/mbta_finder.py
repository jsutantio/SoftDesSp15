"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?address={}"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"
MBTA_url = "http://realtime.mbta.com/developer/api/v2/stopsbylocation?api_key={}&lat={}&lon={}&format=json"


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data

def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    """
    
    place_name_formatted = place_name.replace(" ","+")
    # add the queried location to the url
    GMAPSurl = GMAPS_BASE_URL.format(place_name_formatted)
    response_data = get_json(GMAPSurl)
    if response_data == {u'status': u'ZERO_RESULTS', u'results': []}:
        print "Location brings up zero results."
    else:
        # look through the data for the long and lat
        latitude = response_data["results"][0]["geometry"]["location"]["lat"]
        longitude = response_data["results"][0]["geometry"]["location"]["lng"]
        
    return latitude, longitude

def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.
    """
    
    # add the API key, long and lat to the url
    MBTA_url_formatted = MBTA_url.format(MBTA_DEMO_API_KEY, latitude, longitude)
    response_data = get_json(MBTA_url_formatted)
    
    # check to see if the location is valid
    if response_data == {u'stop': []}:
        print "Location is not valid. Try typing the city or street name."
    else:
        # look through the data for the closest station (name and distance)
        station_name = response_data["stop"][0]["stop_name"]
        print "STATION NAME: ", station_name.encode("latin-1")
        distance = response_data["stop"][0]["distance"]
        print "DISTANCE(mi): ", distance.encode("latin-1")


if __name__ == '__main__':
    
    place_name = "70 Line St Somerville"
    (latitude,longitude) = get_lat_long(place_name)
    get_nearest_station(latitude,longitude)