import os,sys
import yaml
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
plt.style.use("publication")

outdir = "/glade/scratch/raymonds/AImelt/NN_output"

varcolor = {}
varcolor["tas"] = "tab:blue"
varcolor["zg"] = "tab:orange"
varcolor["clt"] = "tab:green"
varcolor["radin"] = "tab:red"
varcolor["prsn"] = "tab:purple"

labeldict = {}
labeldict["tas"] = r"T$_{2m}$"
labeldict["zg"] = r"Z$_{500}$"
labeldict["clt"] = r"CC"
labeldict["radin"] = r"RAD$_{in}$"
labeldict["prsn"] = r"SNOW"

ensnumber = {}
ensnumber["CNRM-CM6-1"] = "r1i1p1f2"
ensnumber["CNRM-ESM2-1"] = "r1i1p1f2"
ensnumber["UKESM1-0-LL"] = "r1i1p1f2"
ensnumber["MRI-ESM2-0"] = "r1i1p1f1"
ensnumber["CESM2"] = "r02i1p1f1"

keydict = {}
keydict["CNRM-CM6-1"] = "CNRMCM6"
keydict["CNRM-ESM2-1"] = "CNRMESM2"
keydict["UKESM1-0-LL"] = "UKESM1"
keydict["MRI-ESM2-0"] = "MRIESM2"
keydict["CESM2"] = "CESM2"

fig = plt.figure(figsize=(7.3,8))

ax1 = plt.subplot(3,2,1)
ax2 = plt.subplot(3,2,2)
ax3 = plt.subplot(3,2,3)
ax4 = plt.subplot(3,2,4)
ax5 = plt.subplot(3,2,5)

CNRMCM6_historical_MAR = np.load("/glade/scratch/raymonds/MARPROC/CNRMCM6.histo.npy")
CNRMCM6_mean_melt = np.mean(CNRMCM6_historical_MAR[29:49])
CNRMCM6_historical_MAR = CNRMCM6_historical_MAR - CNRMCM6_mean_melt
CNRMCM6_ssp126_MAR = np.load("/glade/scratch/raymonds/MARPROC/CNRMCM6.ssp126.npy") - CNRMCM6_mean_melt
CNRMCM6_ssp585_MAR = np.load("/glade/scratch/raymonds/MARPROC/CNRMCM6.ssp585.npy") - CNRMCM6_mean_melt

CNRMCM6_MAR = np.append(CNRMCM6_historical_MAR,CNRMCM6_ssp585_MAR)

CNRMESM2_historical_MAR = np.load("/glade/scratch/raymonds/MARPROC/CNRMESM2.histo.npy")
CNRMESM2_mean_melt = np.mean(CNRMESM2_historical_MAR[29:49])
CNRMESM2_historical_MAR = CNRMESM2_historical_MAR - CNRMESM2_mean_melt
CNRMESM2_ssp585_MAR = np.load("/glade/scratch/raymonds/MARPROC/CNRMESM2.ssp585.npy") - CNRMESM2_mean_melt

CNRMESM2_MAR = np.append(CNRMESM2_historical_MAR,CNRMESM2_ssp585_MAR)

MRIESM2_historical_MAR = np.load("/glade/scratch/raymonds/MARPROC/MRIESM2.histo.npy")
MRIESM2_mean_melt = np.mean(MRIESM2_historical_MAR[29:49])
MRIESM2_historical_MAR = MRIESM2_historical_MAR - MRIESM2_mean_melt
MRIESM2_ssp585_MAR = np.load("/glade/scratch/raymonds/MARPROC/MRIESM2.ssp585.npy") - MRIESM2_mean_melt

MRIESM2_MAR = np.append(MRIESM2_historical_MAR,MRIESM2_ssp585_MAR)

UKESM1_historical_MAR = np.load("/glade/scratch/raymonds/MARPROC/UKESM1.histo.npy")
UKESM1_mean_melt = np.mean(UKESM1_historical_MAR[29:49])
UKESM1_historical_MAR = UKESM1_historical_MAR - UKESM1_mean_melt
UKESM1_ssp585_MAR = np.load("/glade/scratch/raymonds/MARPROC/UKESM1.ssp585.npy") - UKESM1_mean_melt

UKESM1_MAR = np.append(UKESM1_historical_MAR,UKESM1_ssp585_MAR)

CESM2_historical_MAR = np.load("/glade/scratch/raymonds/MARPROC/CESM2.histo.npy")
CESM2_mean_melt = np.mean(CESM2_historical_MAR[29:49])
CESM2_historical_MAR = CESM2_historical_MAR - CESM2_mean_melt
CESM2_ssp585_MAR = np.load("/glade/scratch/raymonds/MARPROC/CESM2.ssp585.npy") - CESM2_mean_melt

CESM2_MAR = np.append(CESM2_historical_MAR,CESM2_ssp585_MAR)

for n,cm in enumerate(["CNRM-CM6-1","CNRM-ESM2-1","UKESM1-0-LL","MRI-ESM2-0","CESM2"]):
    for var in ["tas","zg","clt","radin","prsn"]:
        vars()[f"{var}_{keydict[cm]}"] = np.array([])
        for scenario in ["historical","ssp585"]:
            if scenario=="historical":
                tt = np.arange(1850,2015,1)
            else:
                tt = np.arange(2015,2101,1)
            data = np.load(f"{outdir}/{scenario}/{var}/{cm}/{ensnumber[cm]}.npy")
            if scenario=="historical":
                data_mean = np.mean(data[129:149])
            data = data - data_mean
            vars()[f"{var}_{keydict[cm]}"] = np.append(vars()[f"{var}_{keydict[cm]}"],data)
            if cm=="CNRM-CM6-1" and scenario=="historical":
                vars()[f"ax{n+1}"].plot(tt, data, color=varcolor[var], linewidth=1, label=labeldict[var])
            else:
                vars()[f"ax{n+1}"].plot(tt, data, color=varcolor[var], linewidth=1)

r_tas = 0
r_zg = 0
r_clt = 0
r_radin = 0
r_prsn = 0
RMSE_tas = 0
RMSE_zg = 0
RMSE_clt = 0
RMSE_radin = 0
RMSE_prsn = 0
for cm in ["CNRM-CM6-1","CNRM-ESM2-1","UKESM1-0-LL","MRI-ESM2-0","CESM2"]:
    for key in ["tas","zg","clt","radin","prsn"]:
        runaveMAR = vars()[f"{keydict[cm]}_MAR"] - np.convolve(np.append(vars()[f"{keydict[cm]}_MAR"],np.flip(vars()[f"{keydict[cm]}_MAR"][-19:])), np.ones((20,))/20, mode="valid")
        runaveANN = vars()[f"{key}_{keydict[cm]}"][100:] - np.convolve(np.append(vars()[f"{key}_{keydict[cm]}"][100:],np.flip(vars()[f"{key}_{keydict[cm]}"][-19:])), np.ones((20,))/20, mode="valid")
        vars()[f"r_{key}"] += np.corrcoef(runaveMAR,runaveANN)[0,1]
        vars()[f"RMSE_{key}"] += np.sqrt(np.mean((vars()[f"{keydict[cm]}_MAR"]-vars()[f"{key}_{keydict[cm]}"][100:])**2))
print(RMSE_tas/5)
print(RMSE_zg/5)
print(RMSE_clt/5)
print(RMSE_radin/5)
print(RMSE_prsn/5)

ax1.set_title("(a) CNRM-CM6-1", loc="left", y=1.02)
ax1.plot(np.arange(1950,2015,1), CNRMCM6_historical_MAR, color="black", linewidth=1, label="MAR")
ax1.plot(np.arange(2015,2101,1), CNRMCM6_ssp585_MAR, color="black", linewidth=1)
ax1.legend(frameon=False)

ax2.set_title("(b) CNRM-ESM2-1", loc="left", y=1.02)
ax2.plot(np.arange(1950,2015,1), CNRMESM2_historical_MAR, color="black", linewidth=1)
ax2.plot(np.arange(2015,2101,1), CNRMESM2_ssp585_MAR, color="black", linewidth=1)

ax3.set_title("(c) UKESM1-0-LL", loc="left", y=1.02)
ax3.plot(np.arange(1950,2015,1), UKESM1_historical_MAR, color="black", linewidth=1)
ax3.plot(np.arange(2015,2101,1), UKESM1_ssp585_MAR, color="black", linewidth=1)

ax4.set_title("(d) MRI-ESM2-0", loc="left", y=1.02)
ax4.plot(np.arange(1950,2015,1), MRIESM2_historical_MAR, color="black", linewidth=1)
ax4.plot(np.arange(2015,2101,1), MRIESM2_ssp585_MAR, color="black", linewidth=1)

ax5.set_title("(e) CESM2", loc="left", y=1.02)
ax5.plot(np.arange(1950,2015,1), CESM2_historical_MAR, color="black", linewidth=1)
ax5.plot(np.arange(2015,2101,1), CESM2_ssp585_MAR, color="black", linewidth=1)

for axes in range(5):
    vars()[f"ax{axes+1}"].set_xlim([1950,2100])
    vars()[f"ax{axes+1}"].set_ylim([-500,3500])
    vars()[f"ax{axes+1}"].minorticks_on()
    vars()[f"ax{axes+1}"].tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
    vars()[f"ax{axes+1}"].tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)

plt.tight_layout()
plt.savefig("/glade/work/raymonds/pyCESM/AImelt/two/meltvar_mar.pdf", dpi=500)

sys.exit()
