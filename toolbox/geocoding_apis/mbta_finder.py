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


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    # print "response text: ", response_text
    response_data = json.loads(response_text)
    return response_data

def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    
    place_name_formatted = place_name.replace(" ","+")
    print place_name_formatted
    GMAPSurl = GMAPS_BASE_URL.format(place_name_formatted)
    response_data = get_json(GMAPSurl)
    (latitude, longitude) = response_data["results"][0]["geometry"]["location"]
    
    return latitude, longitude


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    
    MBTA_url = "http://realtime.mbta.com/developer/api/v2/stopsbylocation?api_key={}&lat={}&lon={}&format=json"
    MBTA_url_formatted = MBTA_url.format(MBTA_DEMO_API_KEY, latitude, longitude)
    # print "MBTAurl: ", MBTA_url_formatted
    response_data = get_json(MBTA_url_formatted)
    # station_name = response_data["stop"]

    station_name = response_data["stop"][0]["stop_name"]
    print "STATION NAME: ", station_name.encode("latin-1")
    distance = response_data["stop"][0]["distance"]
    print "DISTANCE(mi): ", distance.encode("latin-1")


if __name__ == '__main__':
    
    place_name = "Boston Public Library"
    (latitude,longitude) = get_lat_long(place_name)
    # get_nearest_station(42.349449,-71.077883)