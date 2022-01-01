import numpy as np
def get_climate_data(filename, coords):
	xll = 0 #lng, across the rows
	yll = 0 #lat, down the cols
	nd_val = 0
	cellsize = 0
	rows = 0 # Latitudes
	cols = 0 # Longitudes, there are more columns than rows as the US is wider than tall.
	with open(filename) as f:
		i = 0
		for line in f:
			line = line.split()
			left = line[0]
			right = line[1]
			i += 1
			if i > 7:
				break
			if left == "xllcorner":
				xll = float(right)
			elif left == "yllcorner":
				yll = float(right)
			elif left == "NODATA_VALUE":
				nd_val = float(right)
			elif left == "cellsize":
				cellsize = float(right)
			elif left == "nrows":
				rows = float(right)
			elif left == "ncols":
				cols = float(right)

	ascii_grid = np.loadtxt(filename,skiprows=6)
	lat = coords[0]
	lng = coords[1]
	lat_ul = yll + cellsize * (rows)
	#lat_a = (lat_ul - lat) / cellsize
	lat_a = rows - ((lat - yll) / cellsize)
	lng_a = (lng - xll) / cellsize
	return ascii_grid[round(lat_a)][round(lng_a)]
	#return (data, (xll, yll), cellsize)

def get_climate_data_unused(coords, dat):
	data = dat[0] # Actual raster data
	info = dat[1] # x and y lower left
	cellsize = dat[2]
	lat = coords[0]
	lng = coords[1]
	rows = len(data)
	cols = len(data[0])
	xll = info[0]
	yll = info[1]
	lat_a = rows - ((lat - yll) / cellsize)
	pass

def format_filename(dset, str):
	return f"docs/PRISM_{dset}_30yr_normal_4kmM2_{str}_asc.asc"

def get_biotemp(coords):
	monthly_temps = []
	for month in range(1, 13):
		tmin_fname = format_filename("tmin",f"{month:02d}")
		tmax_fname = format_filename("tmax",f"{month:02d}")
		tmin = get_climate_data(tmin_fname, coords)
		tmax = get_climate_data(tmax_fname, coords)
		tavg = (tmin + tmax) / 2
		if tavg < 0:
			tavg = 0
		monthly_temps.append(tavg)
	return sum(monthly_temps) / 12


def get_elev(coords):
	fname = "docs/PRISM_us_dem_4km_asc.asc"
	return get_climate_data(fname, coords)

def get_ann_precip(coords):
	fname = format_filename("ppt","annual")
	return get_climate_data(fname, coords)
