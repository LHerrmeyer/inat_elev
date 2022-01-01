import noaa_api as na
import statistics

state = "Minnesota"
keyword = "minneapolis st"
dset = "GSOM"

state_id = na.get_state_id(state)
q_dict = {"locationid":state_id, "datasetid":"NORMAL_MLY"} # This is so we don't get too many results
station_list = na.get_stations(q_dict)
station_id = None
print(len(station_list["results"]))
for elem in station_list["results"]:
	#print(elem)
	if keyword in elem["name"].lower():
		station_id = elem["id"]

if station_id == None:
	print("Station not found")
	raise Exception("Station not found")

dat = na.get_dset_data(station_id,1991,2020,dset)
prcp_list = []
temp_list = []
# The sum method has limits are results will be wrong if months are skipped
# Averaging by months or by using the yearly data eliminates these problems
for elem in dat:
	if(elem["datatype"] == "PRCP"):
		#print(elem)
		prcp_list.append(elem["value"])
	elif(elem["datatype"] == "TAVG"):
		temp_list.append(elem["value"])
avg_prcp = statistics.mean(prcp_list) * 12
avg_temp = statistics.mean(temp_list)
print(f"Avg precip:{avg_prcp}, avg temp: {avg_temp}")
