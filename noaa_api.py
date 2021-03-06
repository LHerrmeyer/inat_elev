import requests
import json
import datetime
import statistics

endpoint = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"
h = {'token' : 'vFUYfwwlbfAuZDwrXnOSyNvMVpuEtOzR'}

def get_state_id(state):
	ext = "/locations"
	query_dict = {
		"locationcategoryid" : "ST",
		"limit" : "52"
	}
	res = requests.get(endpoint + ext, params=query_dict, headers=h)
	obj = json.loads(res.content)
	id = "0"
	for item in obj["results"]:
		if item["name"] == state:
			id = item["id"]
	return id

def get_stations(query_dict):
	ext = "/stations"
	query_dict["limit"] = "1000"
	res = requests.get(endpoint + ext, params=query_dict, headers=h)
	return json.loads(res.content)

def get_gsom_data_backend(station_id, start_date, end_date,dataset):
	ext = "/data"
	query_dict = {
		"stationid" : station_id,
		"datasetid": dataset,
		"startdate": start_date,
		"enddate": end_date,
		"limit": "1000",
		"units": "metric"
	}
	res = requests.get(endpoint + ext,params=query_dict, headers=h)
	try:
		obj = json.loads(res.content)
		meta = obj["metadata"]["resultset"]
		new_offset = meta["offset"] + meta["count"]
		limit = meta["limit"]
	except:
		print(res.content)
	return obj["results"]

def get_dset_data(station_id, start_year, end_year,dataset):
	data_list = []
	k = 1
	tmp_start = start_year
	tmp_end = start_year + k
	while(tmp_end < end_year + k):
		print(f"s {tmp_start} e {tmp_end}")
		out = get_gsom_data_backend(station_id, f"{tmp_start}-01-01",f"{tmp_end}-12-31",dataset)
		data_list += out
		tmp_start += k + 1
		tmp_end += k + 1
	return data_list

