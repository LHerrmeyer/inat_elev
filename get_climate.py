import noaa_api as na
import statistics

state = "Minnesota"
keyword = "minneapolis st"
dset = "GSOY"

state_id = na.get_state_id(state)
q_dict = {"locationid":state_id, "datasetid":dset,"enddate":"2001-01-01"}
station_list = na.get_stations(q_dict)
station_id = None
for elem in station_list["results"]:
	#print(elem)
	if keyword in elem["name"].lower():
		station_id = elem["id"]
		print(elem)

if station_id == None:
	print("Station not found")
	raise Exception("Station not found")

dat = na.get_dset_data(station_id,1981,2010,dset)
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
avg_prcp = statistics.mean(prcp_list)
avg_temp = statistics.mean(temp_list)
print(f"Avg precip:{avg_prcp}, avg temp: {avg_temp}")
