####################
# Calculates incoming radiation (shortwaveIN + longwaveIN) and writes to netcdf
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
####################

import xarray as xr
import os

mip = "ssp585"
os.system("mkdir -p /glade/scratch/raymonds/AImelt/CMIP_6/{}/radin".format(mip))
models = os.listdir("/glade/scratch/raymonds/AImelt/CMIP_6/{}/rlds".format(mip))

for model in models:
    print(model)
    ensembles_rlds = os.listdir("/glade/scratch/raymonds/AImelt/CMIP_6/{}/rlds/{}".format(mip,model))
    for ens in ensembles_rlds:
        ds_rlds = xr.open_dataset("/glade/scratch/raymonds/AImelt/CMIP_6/{}/rlds/{}/{}".format(mip,model,ens))
        try:
            ds_rsds = xr.open_dataset("/glade/scratch/raymonds/AImelt/CMIP_6/{}/rsds/{}/{}".format(mip,model,ens))
            fex = True #flag to see if file exists
        except FileNotFoundError:
            fex = False
        if fex:
            print(ens)
            data = ds_rlds["rlds"] + ds_rsds["rsds"]
            data = xr.DataArray(data.values, name="radin", dims=("time","lat","lon"), coords=[data.time, data.lat, data.lon])
            os.system("mkdir -p /glade/scratch/raymonds/AImelt/CMIP_6/{}/radin/{}".format(mip,model))
            data.to_netcdf("/glade/scratch/raymonds/AImelt/CMIP_6/{}/radin/{}/{}".format(mip,model,ens))
