####################
# Downloads CMIP6 climate data
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
###################

import xarray as xr
import pandas as pd
import zarr
import gcsfs
import numpy as np
import sys
import os
from cdo import Cdo
pd.set_option('display.max_rows', 10)

scratchdir = "/glade/scratch/raymonds"

df = pd.read_csv('https://storage.googleapis.com/cmip6/cmip6-zarr-consolidated-stores.csv')
gcs = gcsfs.GCSFileSystem(token='anon')

varlist = ['zg','tas','psl','clt','rsds','rlds','prsn']
exps = ['historical','ssp126','ssp245','ssp370','ssp585']
mips = {'historical':'CMIP', 'ssp126':'ScenarioMIP', 'ssp245':'ScenarioMIP', 'ssp370':'ScenarioMIP', 'ssp585':'ScenarioMIP'}

for exper in exps:
	print(exper)
	for key in varlist:
		print(key)
		df_experkey = df.query("activity_id=='{}' & experiment_id=='{}' & table_id=='Amon' & variable_id=='{}'".format(mips[exper],exper,key))
		modelss = df_experkey.source_id.unique()
		modelss = modelss[modelss != 'NorCPM1']
		modelss = modelss[modelss != 'MCM-UA-1-0']
		for model in modelss:
			print(model)
			os.system("mkdir -p {}/AImelt/CMIP_6/{}/{}/{}".format(scratchdir,exper,key,model))
			dltab = df_experkey.query("source_id=='{}'".format(model))
			for ens in range(len(dltab.zstore.values)):
				zstore = dltab.zstore.values[ens]
				mapper = gcs.get_mapper(zstore)
				ds = xr.open_zarr(mapper, consolidated=True)
				ds.to_netcdf("/glade/scratch/raymonds/temp/cdoinput.nc")
				ds = Cdo().seasavg(input="/glade/scratch/raymonds/temp/cdoinput.nc", returnXDataset=True)
				ds = ds.sel(time=ds["time.season"]=="JJA")
				attrs = ds.attrs

				if key=='zg':
					plev = np.abs(ds.plev.values - 50000.0)
					p = np.argmin(plev)
					ds = ds[key]
					ds = ds[:,p,:,:]
					ds = ds.to_dataset()
					ds.attrs = attrs
					ds.encoding["unlimited_dims"] = "time"
				else:
					ds = ds[key]
					ds = ds.to_dataset()
					ds.attrs = attrs
					ds.encoding["unlimited_dims"] = "time"

				ds.to_netcdf("{}/AImelt/CMIP_6/{}/{}/{}/{}.nc".format(scratchdir,exper,key,model,attrs["variant_label"]))
				del(zstore, mapper, ds, attrs)
