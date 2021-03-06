import requests
import json
import time
import numpy as np
import matplotlib.pyplot as plt

info = {}
fname = "mt_charleston_nv_50km.json"
with open(fname,"r") as f:
	info = json.load(f)

elev_lists = []
count = 1
species_nums = []
for species in info:
	# Put info to list
	data_points = info[species]["elev_coord_list"]
	elev_list = []
	for point in data_points:
		elev_list.append(point["elev"])
	# Calculate statistics
	start = end = 0
	if len(elev_list) < 3:
		continue
	if len(elev_list) > 1:
		start = np.percentile(elev_list, 10)
		end = np.percentile(elev_list, 90)
		mn = np.percentile(elev_list, 0)
		mx = np.percentile(elev_list, 100)
	print(f"{count}.{species} 10th:[{start}] 90th:[{end}] min:[{mn}] max:[{mx}] n:[{len(elev_list)}]")
	species_nums.append((count,species))
	elev_lists.append(elev_list)
	count += 1

fig1, ax1 = plt.subplots()
ax1.set_title(fname)
ax1.boxplot(elev_lists, showmeans=True, showfliers=False, whis = [10, 90])

# Add llabels
for species_num in species_nums:
	plt.plot([], [], ' ', label=f"{species_num[0]}. {species_num[1]}")

plt.legend(fontsize=6, loc="upper left")
out_fname = f"{fname.split('.')[0]}.png"
plt.savefig(out_fname)
plt.show()