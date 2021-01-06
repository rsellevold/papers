####################
# Runs climate simulation output through the ANN models
# and predicts the annual melt rate.
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
####################


import sys, os
import xarray as xr
import tensorflow as tf
import pandas as pd
import numpy as np
import cdo
cdo = cdo.Cdo()

def model_weights(model):
	wgtsnn, biasnn = model.layers[1].get_weights()
	wgtsout, biasout = model.layers[2].get_weights()

	wgts_reshaped = np.empty(shape=(wgtsnn.shape[1], 192, 288))
	maxes = []
	for k in range(wgtsnn.shape[1]):
		wgts_reshaped[k,:,:] = np.reshape(wgtsnn[:,k], (192, 288))
		locmax = np.max(np.abs(np.array([np.max(wgts_reshaped[k,:,:]),np.min(wgts_reshaped[k,:,:])])))
		maxes.append(locmax)
		wgts_reshaped[k,:,:] = wgts_reshaped[k,:,:] / locmax

	return wgts_reshaped, maxes, wgtsout, biasnn, biasout

def meltmap(data, years, wgtsnn, maxes, biasnn, wgtsout, biasout):
	nmaps = 4
	melt_maps = np.empty(shape=(nmaps, years))
	for m in range(nmaps):
		wgtedmap = data * wgtsnn[m,:,:] * maxes[m]
		melt_maps[m,:] = np.sum(wgtedmap, axis=(1,2)) + biasnn[m]
		for t in range(melt_maps.shape[1]):
			if melt_maps[m,t] <= 0:
				melt_maps[m,t] = 0
	melt_maps = (melt_maps * wgtsout + biasout)
	return melt_maps
			


scratchdir = "/glade/scratch/raymonds/AImelt/CMIP6"
mip = "ssp585"

keydict = {"TREFHT": "tas", "Z500": "zg", "CLDTOT": "clt", "PSL": "psl", "PRECS": "prsn", "RADIN": "radin"}
subtract = {"TREFHT": 180.0, "Z500": 4250.0, "CLDTOT": 0.0, "PSL": 920.0, "PRECS": 0.0, "RADIN": 0.0}
divide = {"TREFHT": 160.0, "Z500": 2000.0, "CLDTOT": 1.0, "PSL": 140.0, "PRECS": 7000.0, "RADIN": 1000.0}
scale = {"TREFHT": 1.0, "Z500": 1.0, "CLDTOT": 100.0, "PSL": 100.0, "PRECS": 3.1709791983764586e-08, "RADIN": 1.0}

# Loop through the variables
for key in ["PSL", "RADIN", "PRECS", "CLDTOT", "Z500", "TREFHT"]:
    print("---------------")
    print(key)
    print("---------------")
    model = tf.keras.models.load_model("../models/saved/nn_4/{}/model.tf".format(key))
    wgts_reshaped, maxes, wgtsout, biasnn, biasout = model_weights(model)
    climate_models = os.listdir("{}/{}/{}".format(scratchdir, mip, keydict[key]))
    mean2d = xr.open_dataset("/glade/scratch/raymonds/AImelt/CMIP6/historical/{}/CESM2/ens2dmean.nc".format(keydict[key]))[keydict[key]]
    for cm in climate_models:
        print("*****")
        print(cm)
        ensembles = os.listdir("{}/{}/{}/{}".format(scratchdir, mip, keydict[key], cm))
        if mip=="historical":
            ensembles.remove("ens2dmean.nc")
        try:
            mean2dens = xr.open_dataset("/glade/scratch/raymonds/AImelt/CMIP6/historical/{}/{}/ens2dmean.nc".format(keydict[key],cm))
            meanisthere = True
        except FileNotFoundError:
            meanisthere = False
        for ens in ensembles:
            if meanisthere:
                fname = "/glade/scratch/raymonds/AImelt/CMIP6/{}/{}/{}/{}".format(mip,keydict[key],cm,ens)
                ds = xr.open_dataset(fname)
                ds[keydict[key]].values = ds[keydict[key]].values - mean2dens[keydict[key]].values
                ds = cdo.remapbil("../data/cesm2_grid.txt", input=ds, returnXDataset=True)
                ds = ds.sortby("time")
                data = ds[keydict[key]].values + mean2d.values
                data = ((data/scale[key]) - subtract[key])/divide[key]

                pred = model.predict(data)[:,0]
                print(np.mean(pred[-20:]),np.std(pred[-20:]))
                os.system("mkdir -p /glade/scratch/raymonds/AImelt/CMIP6_output/{}/{}/{}".format(mip, keydict[key], cm))
                pred_attrs = {"long_name": "Predicted melt from neural network", "unit": "Gt/yr"}
                pred = xr.DataArray(pred, name="melt_predicted", dims=("time"), coords=[ds.time], attrs=pred_attrs)
                pred.to_netcdf("/glade/scratch/raymonds/AImelt/CMIP6_output/{}/{}/{}/{}_output.nc".format(mip, keydict[key], cm, ens[:-3]))

                melt_maps = meltmap(data, len(ds.time.values), wgts_reshaped, maxes, biasnn, wgtsout, biasout)
                melt_maps_attrs = {"long_name": "Melt contribution per map", "units": "Gt/yr"}
                melt_maps = xr.DataArray(melt_maps, name="melt_per_map", dims=("map","time"), coords=[np.arange(0,4,1), ds.time])
                melt_maps.to_netcdf("/glade/scratch/raymonds/AImelt/CMIP6_output/{}/{}/{}/{}_output.nc".format(mip, keydict[key], cm, ens[:-3]), mode="a")
                ds.close()
        mean2dens.close()
