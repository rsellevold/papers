####################
# Calculate and write the global mean temperature
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
###################

import xarray as xr
import numpy as np
from cdo import Cdo
import os,sys
cdo = Cdo()

for mip in ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]:
    os.system("mkdir -p /glade/scratch/raymonds/AImelt/CMIP6/{}/gmt".format(mip))
    models = os.listdir("/glade/scratch/raymonds/AImelt/CMIP6/{}/tas".format(mip))
    for model in models:
        print(model)
        ensembles = os.listdir("/glade/scratch/raymonds/AImelt/CMIP6/{}/tas/{}".format(mip,model))
        for ens in ensembles:
            ds = xr.open_dataset("/glade/scratch/raymonds/AImelt/CMIP6/{}/tas/{}/{}".format(mip,model,ens))
            area = cdo.gridarea(input=ds, returnXDataset=True)
            data = np.sum(ds.tas.values * area.cell_area.values, axis=(1,2)) / np.sum(area.cell_area.values)
            print(np.mean(data-273.15))
            data = xr.DataArray(data, name="tas", dims=("time"), coords=[ds.time])
            os.system("mkdir -p /glade/scratch/raymonds/AImelt/CMIP6/{}/gmt/{}".format(mip,model))
            data.to_netcdf("/glade/scratch/raymonds/AImelt/CMIP6/{}/gmt/{}/{}".format(mip,model,ens))
            ds.close()
            area.close()
