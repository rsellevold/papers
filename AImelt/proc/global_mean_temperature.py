###################
# Calculate the global mean temperature for each scenario
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
##################


import os,sys
import yaml
import xarray as xr
import numpy as np

scratchdir = "/glade/scratch/raymonds/AImelt/CMIP6"


for s,scenario in enumerate(["historical", "ssp126", "ssp245", "ssp370", "ssp585"]):
    print(scenario)
    vars()["temp_"+scenario] = np.array([])
    vars()["w"+scenario] = []
    cms = os.listdir("{}/{}/gmt".format(scratchdir,scenario))
    if "CIESM" in cms: cms.remove("CIESM")
    for cm in cms:
        if scenario=="historical":
            fnames = os.popen("ls {}/{}/gmt/{}/*".format(scratchdir,scenario,cm)).read().split("\n")[1:-1]
        else:
            fnames = os.popen("ls {}/{}/gmt/{}/*".format(scratchdir,scenario,cm)).read().split("\n")[:-1]
        data_mean = xr.open_dataset("{}/historical/gmt/{}/mean.nc".format(scratchdir,cm)).tas.values
        for fname in fnames:
            ds = xr.open_dataset(fname)
            ds.coords["time"] = ds.time.dt.year
            if scenario=="historical":
                ds = ds.sel(time=slice(1850,2014)).sortby("time")
            else:
                try:
                    ds = ds.sel(time=slice(2015,2100)).sortby("time")
                except KeyError:
                    pass
            data = ds.tas.values - data_mean
            if scenario=="historical" and len(data)==165 and not(np.isnan(data).any()):
                vars()["temp_"+scenario] = np.append(vars()["temp_"+scenario], data)
                vars()["w"+scenario].append(cm)
            elif scenario!="historical" and len(data)==86 and not(np.isnan(data).any()):
                vars()["temp_"+scenario] = np.append(vars()["temp_"+scenario], data)
                vars()["w"+scenario].append(cm)
            ds.close()

    if scenario=="historical":
        vars()["temp_"+scenario] = np.reshape(vars()["temp_"+scenario], (int(len(vars()["temp_"+scenario])/165),165))
    else:
        vars()["temp_"+scenario] = np.reshape(vars()["temp_"+scenario], (int(len(vars()["temp_"+scenario])/86),86))


for scenario in ["historical","ssp126","ssp245","ssp370","ssp585"]:
        print("**********")
        print(scenario)
        cms = list(dict.fromkeys(vars()["w"+scenario]))
        for i in range(len(cms)):
            print(cms[i])
            idxs = np.copy(vars()["w"+scenario])
            idxs[idxs!=cms[i]] = 0
            idxs[idxs==cms[i]] = 1
            idxs = idxs.astype(np.bool)
            cm_melt = vars()["temp_"+scenario][idxs,:]
            np.save("../data/temp.{}.{}.npy".format(cms[i],scenario), cm_melt)


for scenario in ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]:
    print(scenario)
    cms = list(dict.fromkeys(vars()["w"+scenario]))
    if scenario=="historical":
        vars()["ensmean_"+scenario] = np.zeros(shape=(len(cms),165))
    else:
        vars()["ensmean_"+scenario] = np.zeros(shape=(len(cms),86))
    for i in range(len(vars()["w"+scenario])):
        cmidx = cms.index(vars()["w"+scenario][i])
        vars()["ensmean_"+scenario][cmidx,:] += vars()["temp_"+scenario][i,:]
    for n,cm in enumerate(cms):
        cnt = vars()["w"+scenario].count(cm)
        vars()["ensmean_"+scenario][n,:] = vars()["ensmean_"+scenario][n,:] / cnt
    np.save("glbmean_"+scenario+".npy", vars()["ensmean_"+scenario])
