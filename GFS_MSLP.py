#Import all modules and components for project
from datetime import datetime, timedelta
import io
from metpy.units import units
from metpy.plots import ImagePlot, MapPanel, PanelContainer
from metpy.plots import ContourPlot
from siphon.catalog import TDSCatalog
import xarray as xr
import matplotlib.colors as cls
import matplotlib.pyplot as plt
from metpy.plots import FilledContourPlot
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import pandas as pd




#Connect to data source
data_url = ('http://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/'
'Global_0p25deg/catalog.xml?dataset=grib/NCEP/GFS/Global_0p25deg/Best')

best_gfs = TDSCatalog(data_url)
print(list(best_gfs.datasets))

best_ds = best_gfs.datasets[0]
ncss = best_ds.subset()





#Load the data from source
query = ncss.query()
query.lonlat_box(north=90, south=0, east=60, west=-20).time(datetime.utcnow() + timedelta(hours=84))
query.accept('netcdf4')
query.variables('Pressure_reduced_to_MSL_msl', 'Temperature_isobaric', 'u-component_of_wind_isobaric')
data = ncss.get_data_raw(query)

gfs = xr.open_dataset(io.BytesIO(data))

# Extract the model time from the data
model_time = gfs.time.data[0]





# Calculate geopotential height contours
contour = ContourPlot()
contour.data = gfs
contour.field = 'Pressure_reduced_to_MSL_msl'
#contour.level = 850 * units.hPa
contour.linecolor = 'white'
contour.linestyle = 'solid'
contour.linewidth = 1
contour.clabels = False
contour.contours = list(range(93100, 107300, 100))
contour.smooth_field = 6

# Calculate temperature contours
contourt = ContourPlot()
contourt.data = gfs
contourt.field = 'Temperature_isobaric'
contourt.level = 850 * units.hPa
contourt.linecolor = 'black'
contourt.linestyle = 'solid'
contourt.linewidth = 1
contourt.clabels = False
contourt.contours = list(range(183, 283, 1))

# Calculate filled temperature contours
filled_temp_contour = FilledContourPlot()
filled_temp_contour.data = gfs
filled_temp_contour.field = 'Pressure_reduced_to_MSL_msl'
#filled_temp_contour.level = 850 * units.hPa
filled_temp_contour.colormap = 'custom_temperature_colormap'
filled_temp_contour.colorbar = 'horizontal'
filled_temp_contour.contours = list(range(93100, 107300, 100))
filled_temp_contour.smooth_field = 6

temperature_colors = [
"#ff7fff",
"#ff6cff",
"#ff5fff",
"#ff51ff",
"#ff47ff",
"#ff3cff",
"#ff2bff",
"#ff19ff",
"#fb00fb",
"#f300f3",
"#ee00ee",
"#e400e4",
"#d900d9",
"#cb00cb",
"#bc00bc",
"#b200b1",
"#a800ac",
"#a100ab",
"#9b00af",
"#9300af",
"#8900af",
"#7e00af",
"#6f00af",
"#6000af",
"#5200af",
"#4400af",
"#3900af",
"#3000ae",
"#1f00ad",
"#1101ad",
"#0000af",
"#0000b2",
"#0000b5",
"#0000ba",
"#0000c1",
"#0000c8",
"#0000d2",
"#0000de",
"#0000eb",
"#0000f7",
"#0000ff",
"#0015ff",
"#0024ff",
"#0030ff",
"#003aff",
"#0041ff",
"#0046ff",
"#004cff",
"#0053ff",
"#005aff",
"#0062ff",
"#006bff",
"#0074ff",
"#007dff",
"#0086ff",
"#008fff",
"#0099ff",
"#00a3ff",
"#00adff",
"#00b7ff",
"#00c2ff",
"#00ccff",
"#00d7ff",
"#00e0ff",
"#42e8ff",
"#6cefff",
"#8ff5ff",
"#a4fbff",
"#afffff",
"#a7ffe6",
"#92ffc3",
"#6fff90",
"#44ff59",
"#00ff00",
"#00f600",
"#00ed00",
"#00e100",
"#00d500",
"#00c800",
"#00b600",
"#00a000",
"#008d00",
"#008100",
"#078000",
"#449100",
"#78af00",
"#b1d400",
"#e3f300",
"#ffff00",
"#fff900",
"#ffec00",
"#ffd800",
"#ffc300",
"#ffb200",
"#ffa600",
"#ff9c00",
"#ff9200",
"#ff8800",
"#ff7e00",
"#ff7400",
"#ff6a00",
"#ff5e00",
"#ff5100",
"#ff4400",
"#ff3900",
"#ff2e00",
"#ff2100",
"#ff1400",
"#ff0000",
"#f60000",
"#e80000",
"#d80000",
"#c70000",
"#b80000",
"#ac0000",
"#a10000",
"#950000",
"#8a0000",
"#7e0000",
"#6f0000",
"#630000",
"#560000",
"#4a0000",
"#430000",
"#40000e",
"#3d001d",
"#3c002a",
"#3f0039",
"#440045",
"#4d0051",
"#59005d",
"#660069",
"#740074",
"#820082",
"#900090",
"#a100a1",
"#af00af",
"#be00be",
"#cc00cc",
"#da00da",
"#e600e6",
"#f000f0",
"#ff00ff",
]
temperature_colormap = cls.ListedColormap(temperature_colors)

plt.register_cmap(cmap=temperature_colormap, name='custom_temperature_colormap')

filled_temp_contour.colormap = 'custom_temperature_colormap'





#Create panel and save the data as image
panel = MapPanel()
panel.plots = [contour, filled_temp_contour]
panel.area = (-4, 43, 51, 66)
panel.projection = ccrs.AlbersEqualArea()




# With the following line to use higher resolution borders
high_res_borders = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_0_boundary_lines_land',
    scale='10m',
    edgecolor='black',
    facecolor='none'
)

# Add land features with facecolor
land_feature = cfeature.NaturalEarthFeature(
    category='physical',
    name='land',
    scale='10m',
    edgecolor='face',
    facecolor='#C0C0C0'  # Choose the color you want for land fill
)

# Add land and ocean features with specified facecolors to the layers
panel.layers = [cfeature.COASTLINE.with_scale('10m'), high_res_borders]
panel.title = '10 hPa Temperatūra un ģeopotenciāle'

pc = PanelContainer()
pc.size = (20, 18)
pc.panels = [panel]

# Convert model_time to a Python datetime object
model_time_dt = pd.to_datetime(model_time)

# Format the model time as a string
model_time_str = model_time_dt.strftime('%Y-%m-%d %H:%M:%S UTC')

# Update the panel title to include the model time
title_text = 'Atmosfēras spiediens jūras līmenī (MSLP)                                                                                                                                                                                                                                               '
title_text2 = f'Laiks: {model_time_str}'
panel.title = f'{title_text} {title_text2}'

pc.save('02.01.2024.1857.png', bbox_inches="tight", pad_inches=0, dpi=600)
