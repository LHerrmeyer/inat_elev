import noaa_api as na
import statistics

state = "Minnesota"
keyword = "minneapolis anoka"
dset = "NORMAL_MLY"

state_id = na.get_state_id(state)
print(state_id)
state_id = "ZIP:55014"
q_dict = {"locationid":state_id, "datasetid":dset}
station_list = na.get_stations(q_dict)
station_id = None
try:
	print(len(station_list["results"]))
	for elem in station_list["results"]:
		if keyword in elem["name"].lower():
			station_id = elem["id"]
except KeyError:
	print(station_list)

if station_id == None:
	print("Station not found")
	print("Falling back")
	station_id = 'GHCND:US1MNAA0098'
	#raise Exception("Station not found")

start_date = '2020-04-27'
end_date = '2020-11-10'
dat = na.get_dset_data_backend(station_id,start_date,end_date,dset)
prcp_list = []
temp_list = []
# The sum method has limits are results will be wrong if months are skipped
# Averaging by months or by using the yearly data eliminates these problems
for elem in dat:
	if(elem["datatype"] == "MLY-PRCP-NORMAL"):
		print(elem)
		prcp_list.append(elem["value"])
	elif(elem["datatype"] == "MLY-TAVG-NORMAL"):
		temp_list.append(elem["value"])
avg_prcp = statistics.mean(prcp_list) * 12
avg_temp = statistics.mean(temp_list)
print(f"Avg precip:{avg_prcp}, avg temp: {avg_temp}")
