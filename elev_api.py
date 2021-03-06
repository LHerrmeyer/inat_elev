import requests
import json
import time
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def get_elevation_natmap(coords):
	endpoint = "https://nationalmap.gov/epqs/pqs.php"
	url = endpoint
	lat = coords[0]
	long = coords[1]
	param_dict = {"x": coords[1], "y": coords[0], "units": "Meters", "output": "json"}
	adapter = HTTPAdapter(max_retries=3)
	http = requests.Session()
	http.mount("https://", adapter)
	http.mount("http://", adapter)
	response = http.get(url, params=param_dict)
	resp_dict = json.loads(response.content)
	#print(resp_dict)
	return resp_dict["USGS_Elevation_Point_Query_Service"]["Elevation_Query"]["Elevation"]

def get_elevation(coords):
	return get_elevation_natmap(coords)
