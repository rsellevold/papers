###################
# This script generates melt projections for each scenario
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
####################


import os,sys
import yaml
import xarray as xr
import numpy as np

scratchdir = "/glade/scratch/raymonds/AImelt/CMIP6_output"

melt_historical = np.array([])
melt_ssp126 = np.array([])
melt_ssp245 = np.array([])
melt_ssp370 = np.array([])
melt_ssp585 = np.array([])
cmdict = {}

for s,scenario in enumerate(["historical", "ssp126", "ssp245", "ssp370", "ssp585"]):
    print(scenario)
    vars()["w"+scenario] = []
    for key in ["tas","prsn"]:
        print(key)
        cms = os.listdir("{}/{}/{}".format(scratchdir,scenario,key))
        if "CIESM" in cms: cms.remove("CIESM")
        for cm in cms:
            try:
                cmdict[cm]
            except KeyError:
                cmdict[cm] = {}
            fnames = os.popen("ls {}/{}/{}/{}/*".format(scratchdir,scenario,key,cm)).read().split("\n")[:-1]
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
                data = ds.melt_predicted.values
                if scenario=="historical" and len(data)==165 and not(np.isnan(data).any()):
                    vars()["melt_"+scenario] = np.append(vars()["melt_"+scenario], data)
                    vars()["w"+scenario].append(cm)
                    try:
                        cmdict[cm][scenario].append(fname.replace(f"{scratchdir}/{scenario}/{key}/{cm}/",""))
                    except KeyError:
                        cmdict[cm][scenario] = []
                        cmdict[cm][scenario].append(fname.replace(f"{scratchdir}/{scenario}/{key}/{cm}/",""))
                elif scenario!="historical" and len(data)==86 and not(np.isnan(data).any()):
                    vars()["melt_"+scenario] = np.append(vars()["melt_"+scenario], data)
                    vars()["w"+scenario].append(cm)
                    try:
                        cmdict[cm][scenario].append(fname.replace(f"{scratchdir}/{scenario}/{key}/{cm}/",""))
                    except KeyError:
                        cmdict[cm][scenario] = []
                        cmdict[cm][scenario].append(fname.replace(f"{scratchdir}/{scenario}/{key}/{cm}/",""))

    if scenario=="historical":
        vars()["melt_"+scenario] = np.reshape(vars()["melt_"+scenario], (int(len(vars()["melt_"+scenario])/165),165))
    else:
        vars()["melt_"+scenario] = np.reshape(vars()["melt_"+scenario], (int(len(vars()["melt_"+scenario])/86),86))

a = np.zeros(5)
b = np.zeros(5)
for key,item in cmdict.items():
    for s,scenario in enumerate(["ssp585"]):#enumerate(["historical","ssp126","ssp245","ssp370","ssp585"]):
        try:
            print(key, scenario, len(list(dict.fromkeys(cmdict[key][scenario]))))
            a[s] += len(list(dict.fromkeys(cmdict[key][scenario])))
            b[s] += len(cmdict[key][scenario])
        except KeyError:
            None
print(a)
print(b)
sys.exit()

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
        cm_melt = vars()["melt_"+scenario][idxs,:]
        np.save("../data/{}.{}.npy".format(cms[i],scenario), cm_melt)


for scenario in ["historical","ssp126","ssp245","ssp370","ssp585"]:
    print("**********")
    print(scenario)
    cms = list(dict.fromkeys(vars()["w"+scenario]))
    cms.sort()
    if scenario=="historical":
        vars()["ensmean_"+scenario] = np.zeros(shape=(len(cms),165))
        cmdict = dict.fromkeys(vars()["w"+scenario])
    else:
        vars()["ensmean_"+scenario] = np.zeros(shape=(len(cms),86))
    for i in range(len(vars()["w"+scenario])):
        cmidx = cms.index(vars()["w"+scenario][i])
        vars()["ensmean_"+scenario][cmidx,:] += vars()["melt_"+scenario][i,:]
    for n,cm in enumerate(cms):
        cnt = vars()["w"+scenario].count(cm)
        vars()["ensmean_"+scenario][n,:] = vars()["ensmean_"+scenario][n,:] / cnt
        print(cm,cnt)
    np.save("proj_"+scenario+".npy", vars()["ensmean_"+scenario])
