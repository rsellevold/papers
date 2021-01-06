import os, sys
sys.path.append("/glade/u/home/raymonds/pyCESM/lib")

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
from cartopy.util import add_cyclic_point
import matplotlib.colors as colors
import cmocean, rfunc, nclcmaps
import matplotlib.patches as patches
plt.style.use("publication")

def add_cyclic(data):
    attrs = data.attrs
    dims = data.dims
    name = data.name
    mp = data.map
    lat = data.lat
    data, lon = add_cyclic_point(data.values, coord=data.lon, axis=data.dims.index('lon'))
    data = xr.DataArray(data, name=name, dims=dims, attrs=attrs, coords=[mp, lat, lon])
    return data

# Load data
varlist = ["TREFHT", "Z500", "CLDTOT", "PSL", "RADIN", "PRECS"]
for key in varlist:
	f = xr.open_dataset("../models/saved/nn_10/{}/output.nc".format(key))
	vars()["maps_{}".format(key)] = f.featmaps

for key in varlist:
    vars()["maps_{}".format(key)] = add_cyclic(vars()["maps_{}".format(key)])


# Plot
fig = plt.figure(figsize=(7.3,5.5))

proj = ccrs.EquidistantConic(central_longitude=-45)
cmap = plt.get_cmap("RdBu_r")
clevs = np.array([-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
norm = colors.BoundaryNorm(clevs, cmap.N)

xmin = -135
xmax = 45
ymin = 40
ymax = 90
ext = [xmin,xmax,ymin,ymax]


# TREFHT maps (3,0)
ax11 = plt.subplot(5,3,1, projection=ccrs.PlateCarree(central_longitude=-45))
ax11.coastlines(resolution="50m", linewidth=0.5)
ax11.set_title(r"(a) T$_{2m}$", loc="left")
plot = ax11.contourf(maps_TREFHT.lon.data, maps_TREFHT.lat.data, maps_TREFHT[3,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax11.set_extent(ext, ccrs.PlateCarree())
ax11.outline_patch.set_edgecolor("tab:orange")

ax12 = plt.subplot(5,3,2, projection=ccrs.PlateCarree(central_longitude=-45))
ax12.coastlines(resolution="50m", linewidth=0.5)
plot = ax12.contourf(maps_TREFHT.lon.values, maps_TREFHT.lat.data, maps_TREFHT[0,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax12.set_extent(ext, ccrs.PlateCarree())
ax12.outline_patch.set_edgecolor("tab:green")

# Z500 maps (3,2,0)
ax21 = plt.subplot(5,3,4, projection=ccrs.PlateCarree(central_longitude=-45))
ax21.coastlines(resolution="50m", linewidth=0.5)
ax21.set_title(r"(b) Z$_{500}$", loc="left")
plot = ax21.contourf(maps_Z500.lon.data, maps_Z500.lat.data, maps_Z500[3,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax21.set_extent(ext, ccrs.PlateCarree())
ax21.outline_patch.set_edgecolor("tab:orange")

ax22 = plt.subplot(5,3,5, projection=ccrs.PlateCarree(central_longitude=-45))
ax22.coastlines(resolution="50m", linewidth=0.5)
plot = ax22.contourf(maps_Z500.lon.values, maps_Z500.lat.data, maps_Z500[2,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax22.set_extent(ext, ccrs.PlateCarree())
ax22.outline_patch.set_edgecolor("tab:green")

ax23 = plt.subplot(5,3,6, projection=ccrs.PlateCarree(central_longitude=-45))
ax23.coastlines(resolution="50m", linewidth=0.5)
plot = ax23.contourf(maps_Z500.lon.values, maps_Z500.lat.data, maps_Z500[0,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax23.set_extent(ext, ccrs.PlateCarree())
ax23.outline_patch.set_edgecolor("tab:red")

# CLDTOT maps (2,1,0)
ax31 = plt.subplot(5,3,7, projection=ccrs.PlateCarree(central_longitude=-45))
ax31.coastlines(resolution="50m", linewidth=0.5)
ax31.set_title("(c) CC", loc="left")
plot = ax31.contourf(maps_CLDTOT.lon.data, maps_CLDTOT.lat.data, maps_CLDTOT[2,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax31.set_extent(ext, ccrs.PlateCarree())
ax31.outline_patch.set_edgecolor("tab:orange")

ax32 = plt.subplot(5,3,8, projection=ccrs.PlateCarree(central_longitude=-45))
ax32.coastlines(resolution="50m", linewidth=0.5)
plot = ax32.contourf(maps_CLDTOT.lon.values, maps_CLDTOT.lat.data, maps_CLDTOT[1,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax32.set_extent(ext, ccrs.PlateCarree())
ax32.outline_patch.set_edgecolor("tab:green")

ax33 = plt.subplot(5,3,9, projection=ccrs.PlateCarree(central_longitude=-45))
ax33.coastlines(resolution="50m", linewidth=0.5)
plot = ax33.contourf(maps_CLDTOT.lon.values, maps_CLDTOT.lat.data, maps_CLDTOT[0,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax33.set_extent(ext, ccrs.PlateCarree())
ax33.outline_patch.set_edgecolor("tab:red")


# RADIN maps (2,3)
ax51 = plt.subplot(5,3,10, projection=ccrs.PlateCarree(central_longitude=-45))
ax51.coastlines(resolution="50m", linewidth=0.5)
ax51.set_title("(e) RAD$_{in}$", loc="left")
plot = ax51.contourf(maps_RADIN.lon.data, maps_RADIN.lat.data, maps_RADIN[2,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax51.set_extent(ext, ccrs.PlateCarree())
ax51.outline_patch.set_edgecolor("tab:orange")

ax52 = plt.subplot(5,3,11, projection=ccrs.PlateCarree(central_longitude=-45))
ax52.coastlines(resolution="50m", linewidth=0.5)
plot = ax52.contourf(maps_RADIN.lon.data, maps_RADIN.lat.data, maps_RADIN[3,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax52.set_extent(ext, ccrs.PlateCarree())
ax52.outline_patch.set_edgecolor("tab:green")

# PRECS maps (0)
ax6 = plt.subplot(5,3,13, projection=ccrs.PlateCarree(central_longitude=-45))
ax6.coastlines(resolution="50m", linewidth=0.5)
ax6.set_title("(f) SNOW", loc="left")
plot = ax6.contourf(maps_PRECS.lon.data, maps_PRECS.lat.data, maps_PRECS[0,:,:].values, clevs, cmap=cmap, transform=ccrs.PlateCarree())
ax6.set_extent(ext, ccrs.PlateCarree())
ax6.outline_patch.set_edgecolor("tab:orange")

plt.tight_layout()

fig.subplots_adjust(bottom=0.1)
cbar_ax = fig.add_axes([0.15, 0.075, 0.7, 0.02])
cb = fig.colorbar(plot, extend="neither", cax=cbar_ax, label="Normalized weights", orientation="horizontal", ticks=clevs)
cb.ax.set_xticklabels(clevs)


plt.savefig("/glade/work/raymonds/pyCESM/AImelt/meltmaps_cesm2.pdf")
