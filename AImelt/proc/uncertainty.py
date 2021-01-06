####################
# Calculates the uncertainties related to: variable, ensemble, model, and scenario
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
####################


import sys
import numpy as np
import yaml
plt.style.use("publication")

outdir = "/glade/scratch/raymonds/AImelt/NN_output"

# Calculate variable spread
def variables():
    with open("modellist.yml","r") as f:
        dicti = yaml.safe_load(f)

    nsimssp = 0
    nsim = 0
    stdall = np.zeros(shape=(165))
    stdallssp = np.zeros(shape=(86))
    for scenario in ["historical","ssp126","ssp245","ssp370","ssp585"]:
        cms = dicti[scenario]
        for cm,ens in cms.items():
            if not(len(ens)==0):
                for en in ens:
                    data = np.array([])
                    n = 0
                    for var in ["tas","prsn"]:
                        try:
                            data = np.append(data, np.load(f"{outdir}/{scenario}/{var}/{cm}/{en}.npy"))
                            n+=1
                        except FileNotFoundError:
                            pass
                    data = np.reshape(data, (n,int(len(data)/n)))
                    std = np.std(data, axis=0)
                    if scenario=="historical":
                        nsim += 1
                        stdall += std
                    else:
                        nsimssp += 1
                        stdallssp += std

    stdall = stdall / nsim
    stdallssp = stdallssp/ nsimssp
    stdall = np.append(stdall,stdallssp)
    return stdall

# Calculate ensemble/climate spread
def ensembles():
    with open("modellist.yml","r") as f:
        dicti = yaml.safe_load(f)

    nsim = 0
    nsimssp = 0
    stdall = np.zeros(shape=(165))
    stdallssp = np.zeros(shape=(86))
    for scenario in ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]:
        cms = dicti[scenario]
        for cm, ens in cms.items():
            if not(len(ens)==0):
                dataens = np.array([])
                nens = 0
                for en in ens:
                    data = np.array([])
                    nvar = 0
                    for var in ["tas","prsn"]:
                        try:
                            data = np.append(data, np.load(f"{outdir}/{scenario}/{var}/{cm}/{en}.npy"))
                            nvar += 1
                        except FileNotFoundError:
                            pass
                    nens += 1
                    data = np.reshape(data, (nvar,int(len(data)/nvar)))
                    dataens = np.append(dataens,np.mean(data, axis=0))
                dataens = np.reshape(dataens, (nens,int(len(dataens)/nens)))                 
                std = np.std(dataens,axis=0)
                if scenario=="historical":
                    nsim += 1
                    stdall += std
                else:
                    nsimssp += 1
                    stdallssp += std

    stdall = stdall/nsim
    stdallssp = stdallssp / nsimssp
    stdall = np.append(stdall,stdallssp)
    return stdall

def models():
    with open("modellist.yml","r") as f:
        dicti = yaml.safe_load(f)

    nsim = 0
    nsimssp=0
    stdall = np.zeros(shape=(165))
    stdallssp = np.zeros(shape=(86))
    for scenario in ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]:
        cms = dicti[scenario]
        modeldata = np.array([])
        nmod = 0
        for cm, ens in cms.items():
            if not(len(ens)==0):
                dataens = np.array([])
                nens = 0
                for en in ens:
                    data = np.array([])
                    nvar = 0
                    for var in ["tas","prsn"]:
                        try:
                            data = np.append(data, np.load(f"{outdir}/{scenario}/{var}/{cm}/{en}.npy"))
                            nvar += 1
                        except FileNotFoundError:
                            pass
                    nens += 1
                    data = np.reshape(data, (nvar,int(len(data)/nvar)))
                    dataens = np.append(dataens,np.mean(data, axis=0))
                nmod += 1
                dataens = np.reshape(dataens, (nens,int(len(dataens)/nens)))
                ensmean = np.mean(dataens, axis=0)
                modeldata = np.append(modeldata, ensmean)
        datacalc = np.reshape(modeldata, (nmod,int(len(modeldata)/nmod)))
        std = np.std(datacalc,axis=0)
        if scenario=="historical":
            nsim += 1
            stdall +=std
        else:
            nsimssp += 1
            if scenario=="ssp126":
                stdallssp += std*(31/123)
            elif scenario=="ssp245":
                stdallssp += std*(32/123)
            elif scenario=="ssp370":
                stdallssp += std*(28/123)
            elif scenario=="ssp585":
                stdallssp += std*(32/123)
            #stdallssp += std
    stdall = stdall/nsim
    stdallssp = stdallssp #/ nsimssp
    stdall = np.append(stdall,stdallssp)
    print(stdall[-1])
    sys.exit()
    return stdall


def scenario():
    
    with open("modellist.yml","r") as f:
        dicti = yaml.safe_load(f)

    scens = np.array([])
    for scenario in ["ssp126", "ssp245", "ssp370", "ssp585"]:
        cms = dicti[scenario]
        modeldata = np.array([])
        nmod = 0
        for cm, ens in cms.items():
            if not(len(ens)==0):
                dataens = np.array([])
                nens = 0
                for en in ens:
                    data = np.array([])
                    nvar = 0
                    for var in ["tas","prsn"]:
                        try:
                            data = np.append(data, np.load(f"{outdir}/{scenario}/{var}/{cm}/{en}.npy"))
                            nvar += 1
                        except FileNotFoundError:
                            pass
                    nens += 1
                    data = np.reshape(data, (nvar,int(len(data)/nvar)))
                    dataens = np.append(dataens,np.mean(data, axis=0))
                nmod += 1
                dataens = np.reshape(dataens, (nens,int(len(dataens)/nens)))
                ensmean = np.mean(dataens, axis=0)
                modeldata = np.append(modeldata, ensmean)
        datacalc = np.reshape(modeldata, (nmod,int(len(modeldata)/nmod)))
        modmean = np.mean(datacalc,axis=0)
        scens = np.append(scens,modmean)
    scens = np.reshape(scens, (4,86))
    stdall = np.std(scens, axis=0)
    return stdall


varunc = variables()
ensunc = ensembles()
modunc = models()
scenunc = scenario()

np.save("varunc.npy",varunc)
np.save("ensunc.npy",ensunc)
np.save("modunc.npy",modunc)
np.save("scenunc.npy",scenunc)
