import noaa_api as na


state_id = na.get_state_id("Minnesota")
q_dict = {"locationid":state_id, "datasetid":"GSOM","enddate":"2001-01-01"}
station_list = na.get_stations(q_dict)
station_id = ""
for elem in station_list["results"]:
	if "minneapolis st" in elem["name"].lower():
		station_id = elem["id"]

dat = na.get_gsom_data(station_id,1971,2020)
