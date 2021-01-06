###################
# Calculates and writes the ensemble 1979--1998 mean
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
##################

import xarray as xr
import numpy as np
import os,sys

for key in ["tas","zg","clt","radin","prsn"]:
    print(key)
    models = os.listdir("/glade/scratch/raymonds/AImelt/CMIP6/historical/{}".format(key))
    for model in models:
        print(model)
        ensembles = os.listdir("/glade/scratch/raymonds/AImelt/CMIP6/historical/{}/{}".format(key,model))
        nens = 0
        for ens in ensembles:
            ds = xr.open_dataset("/glade/scratch/raymonds/AImelt/CMIP6/historical/{}/{}/{}".format(key,model,ens))
            ds.coords["time"] = ds.time.dt.year
            ds = ds.sortby("time").sel(time=slice(1979,1998))
            if nens == 0:
                data = np.empty(shape=(len(ensembles),len(ds.lat),len(ds.lon)))
            data[nens,:,:] = ds[key].mean("time").values
            nens += 1
        data = np.nanmean(data, axis=0)
        data = xr.DataArray(data, name=key, dims=("lat","lon"), coords=[ds.lat, ds.lon])
        data.to_netcdf("/glade/scratch/raymonds/AImelt/CMIP6/historical/{}/{}/ens2dmean.nc".format(key,model))
