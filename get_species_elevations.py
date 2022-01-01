import inat_api
import elev_api
import statistics as stats
import json

# Location information
loc = (37.6775, -113.061944)
names_base = "cedar_city_ut"
radius = 50

def get_stats(species_list, center, radius):
	species_stats = {}
	for species in species_list:
		x = inat_api.get_observations({
			"lat":center[0],"lng":center[1],"radius":radius,
			"taxon_name":species,"per_page":"200","captive":"false",
			"quality_grade":"research"
		})
		obs_list = inat_api.get_observations_results(x)
		# List for output
		current_species_stat = {}
		current_species_stat["elev_coord_list"] = []
		current_species_stat["avg_elev"] = 0
		current_species_stat["avg_coords"] = ()
		# Get information for each observation
		for obs in obs_list:
			coords = inat_api.get_observation_coords(obs)
			#print(coords)
			elev = elev_api.get_elevation(coords)
			observation_stat = {"coords": coords, "elev": elev}
			#print(coords)
			current_species_stat["elev_coord_list"].append(observation_stat)
		# Calculate statistics
		lat_list = []
		lng_list = []
		elev_list = []
		for elem in current_species_stat["elev_coord_list"]:
			coords = elem["coords"]
			elev = elem["elev"]
			elev_list.append(elev)
			lat_list.append(coords[0])
			lng_list.append(coords[1])
		avg_elev = avg_lat = avg_lng = med_elev = 0
		avg_coords = ()
		# Make sure we have enough data points, if so, calculate avgs and store them
		if(len(elev_list) > 0):
			avg_elev = stats.mean(elev_list)
			avg_lat = stats.mean(lat_list)
			avg_lng = stats.mean(lng_list)
			med_elev = stats.median(elev_list)
		avg_coords = (avg_lat, avg_lng)
		current_species_stat["avg_elev"] = avg_elev
		current_species_stat["avg_coords"] = avg_coords
		stdev_elev = 0
		# Calculate stdev and store it if we have enough data points
		if len(elev_list) > 1:
			stdev_elev = stats.stdev(elev_list)
		current_species_stat["stdev_elev"] = stdev_elev
		# Print some info
		print(f"{species} Avg elev:[{avg_elev}], Median: [{med_elev}], Stdev: [{stdev_elev}], n: [{len(elev_list)}]")
		# Save stats in the multiple species dictionary
		species_stats[species] = current_species_stat
	return species_stats

def main():
	species_lists = []
	locations = []
	names = []
	species_lists.append([
	"Larrea tridentata", "Prosopis", "Ferocactus", "Ambrosia dumosa", "Fouquieria splendens", "Yucca brevifolia", "Acacia greggii", "Bromus rubens", # Lower Sonoran
	"Juniperus osteosperma", "Pinus edulis", "Pinus monophylla", "Bouteloua gracilis", "Quercus turbinella", "Artemisia tridentata", "Cercocarpus ledifolius", "Juniperus monosperma", # Upper Sonoran
	"Pinus ponderosa", "Quercus gambelii", # Transition
	"Pseudotsuga", "Populus tremuloides", "Abies concolor", # Canadian
	"Picea engelmannii", "Abies lasiocarpa", "Picea pungens", "Pinus longaeva", "Juniperus communis", "Pinus flexilis", "Ribes cereum", # Hudsonian 
	"Phleum alpinum", "Geum rossii", "Phlox pulvinata", "Ribes montigenum" # Alpine-arctic
	])
	names.append(f"{names_base}_{radius}km")
	for i in range(len(species_lists)):
		cur_dict = get_stats(species_list=species_lists[0], center=loc, radius=radius)
		with open(f"{names[i]}.json","w+") as f:
			json.dump(cur_dict, f)
	print("Done!")


if __name__ == "__main__":
	main()
