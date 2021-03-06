import noaa_api as na


state_id = na.get_state_id("Minnesota")
q_dict = {"locationid":state_id, "datasetid":"GSOM","enddate":"2001-01-01"}
station_list = na.get_stations(q_dict)
station_id = ""
for elem in station_list["results"]:
	if "minneapolis st" in elem["name"].lower():
		station_id = elem["id"]

dat = na.get_gsom_data(station_id,1981,2010)
prcp_sum = 0
temp_sum = 0
for elem in dat:
	if(elem["datatype"] == "PRCP"):
		prcp_sum += elem["value"]
	elif(elem["datatype"] == "TAVG"):
		temp_sum += elem["value"]
avg_prcp = prcp_sum / 30
avg_temp = temp_sum / (12 * 30)
print(f"Avg precip:{avg_prcp}, avg temp: {avg_temp}")
