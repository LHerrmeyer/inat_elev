import requests
import json

endpoint = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"

def get_state(state):
	ext = "/locations"

def get_station(query_dict):
	ext = "/stations"
	query_dict["limit"] = 1000
	res = requests.get(endpoint + ext, params=query_dict)
	return json.reads(res.content)
