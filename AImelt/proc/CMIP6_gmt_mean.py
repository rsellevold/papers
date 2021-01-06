####################
# Calculate and write the ensemble-mean 1979--1998 global mean temperature
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
####################

import xarray as xr
import numpy as np
import os,sys

for mip in ["historical"]:
    models = os.listdir("/glade/scratch/raymonds/AImelt/CMIP6/{}/gmt".format(mip))
    for model in models:
        print(model)
        ensembles = os.listdir("/glade/scratch/raymonds/AImelt/CMIP6/{}/gmt/{}".format(mip,model))
        ensembles.remove("mean.nc")
        ens_mean = np.empty(shape=(len(ensembles)))
        for n,ens in enumerate(ensembles):
            ds = xr.open_dataset("/glade/scratch/raymonds/AImelt/CMIP6/{}/gmt/{}/{}".format(mip,model,ens))
            if model=="MPI-ESM1-2-HR":
                ds.coords["time"] = ds.time.dt.year
                data = ds.tas.sortby("time").sel(time=slice(1979,1998)).mean()
            else:
                data = ds.tas.sortby("time").sel(time=slice("1979","1998")).mean()
            ens_mean[n] = data
            ds.close()
        data = xr.DataArray(np.nanmean(ens_mean), name="tas")
        print(data.values)
        data.to_netcdf("/glade/scratch/raymonds/AImelt/CMIP6/{}/gmt/{}/mean.nc".format(mip,model))
