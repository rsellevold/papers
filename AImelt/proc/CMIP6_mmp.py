####################
# Calculates and writes the 1979--1998 mean ANN predicted melt
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
####################

import xarray as xr
import numpy as np
import os,sys

scratchdir = "/glade/scratch/raymonds/AImelt/CMIP6_output"

for mip in ["historical"]:
    for key in ["tas", "clt", "prsn", "radin", "zg"]:
        print("**********")
        print(key)
        print("**********")
        models = os.listdir("{}/{}/{}".format(scratchdir,mip,key))
        for model in models:
            print(model)
            ensembles = os.listdir("{}/{}/{}/{}".format(scratchdir,mip,key,model))
            for ens in ensembles:
                ds = xr.open_dataset("{}/{}/{}/{}/{}".format(scratchdir,mip,key,model,ens)).sortby("time")
                data = ds.melt_predicted.sel(time=slice("1979","1998")).mean()
                data.to_netcdf("{}/{}/{}/{}/mean.nc".format(scratchdir,mip,key,model))
                ds.close()
