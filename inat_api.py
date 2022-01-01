import requests
import json
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

endpoint = "https://api.inaturalist.org/v1/"

def get_observations(req_dict):
	ext = "observations"
	url = endpoint + ext
	adapter = HTTPAdapter(max_retries=3)
	http = requests.Session()
	http.mount("https://", adapter)
	http.mount("http://", adapter)
	response = http.get(url, params=req_dict)
	return json.loads(response.content)

def get_observations_results(req_dict):
	print(req_dict["total_results"])
	return req_dict["results"]

def get_observation_coords(req_dict):
	coords = req_dict["geojson"]["coordinates"]
	return (coords[1], coords[0])

def get_observation_taxon(req_dict):
	return req_dict["taxon"]

def get_taxon_name(taxon):
	print(taxon)
	return taxon["taxon"]["name"]
