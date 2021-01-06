import os, sys
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("publication")

plotdir = "/glade/work/raymonds/pyCESM/AImelt"
os.system("mkdir -p {}".format(plotdir))


# Load melt data and divide into

f = xr.open_dataset("/glade/scratch/raymonds/AImelt/ALL/lnd/rproc/timeseries/GrIS_integrated.annavg.nc")

labels_train = xr.open_dataset("/glade/scratch/raymonds/AImelt/ALL/lnd/rproc/timeseries/GrIS_integrated.annavg.nc")["MELT_ICE"].values - 569.6612932001112 + 486.7245000000001

areascale = 1e+12 / (1844610 * 1e+6)
areascale = areascale * (1693952 * 1e+6) / 1e+12

hist = (f.MELT_ICE[0:(2014-1850+1)*10].values - 569.6612932001112 + 486.7245000000001) * areascale
ssp = (f.MELT_ICE[(2014-1850+1)*10:].values - 569.6612932001112 + 486.7245000000001) * areascale

hist = np.reshape(hist, (10,2014-1850+1)).T
ssp = np.reshape(ssp, (19,2100-2015+1)).T

racmo = np.array([434.31, 475.67, 559.79, 421.81, 478.94, 400.10, 356.02, 445.69, 525.81, 421.13, 548.76, 425.32, 409.01, 510.24, 367.46, 394.61, 461.82, 489.82, 441.96, 417.98, 455.45, 398.05, 485.83, 526.28, 438.09, 357.86, 485.94, 508.06, 405.10, 563.25, 506.00, 473.00, 554.29, 529.34, 336.19, 542.40, 475.58, 587.64, 429.99, 502.10, 629.50, 528.32, 526.59, 530.56, 632.88, 671.61, 601.26, 651.54, 573.00, 686.36, 660.27, 553.19, 784.01, 655.29, 989.20, 490.56, 628.97, 625.26, 711.29, 541.14, 462.42])

racmo = racmo - np.mean(racmo[21:41])
avgmelt = np.mean(np.mean(hist, axis=1)[129:149])
#avgmelt = 0

ssp1 = ssp[:,0:3]
ssp2 = ssp[:,3:6]
ssp3 = ssp[:,6:16]
ssp5 = ssp[:,16:19]

hist = hist-avgmelt
ssp1 = ssp1-avgmelt
ssp2 = ssp2-avgmelt
ssp3 = ssp3-avgmelt
ssp5 = ssp5-avgmelt

fm = xr.open_dataset("/glade/scratch/raymonds/SSP_HIGH/histssp/lnd/rproc/timeseries/GrIS_integrated.annavg.nc")
melt = (fm.MELT_ICE.values - 569.6612932001112 + 486.7245000000001) * areascale - avgmelt

plt.figure(figsize=(7.3,5))
ax = plt.subplot(1,1,1)
ax.set_title(r"Melt anomalies calculated by CESM2 (Gt yr$^{-1}$)", loc="left", y=1.02)

ax.fill_between(np.arange(1850,2015,1), np.mean(hist, axis=1)-np.std(hist, axis=1), np.mean(hist, axis=1)+np.std(hist, axis=1), color="black", alpha=0.2)
ax.fill_between(np.arange(2015,2101,1), np.mean(ssp1, axis=1)-np.std(ssp1, axis=1), np.mean(ssp1, axis=1)+np.std(ssp1, axis=1), color="tab:blue", alpha=0.2)
ax.fill_between(np.arange(2015,2101,1), np.mean(ssp2, axis=1)-np.std(ssp2, axis=1), np.mean(ssp2, axis=1)+np.std(ssp2, axis=1), color="tab:orange", alpha=0.2)
ax.fill_between(np.arange(2015,2101,1), np.mean(ssp3, axis=1)-np.std(ssp3, axis=1), np.mean(ssp3, axis=1)+np.std(ssp3, axis=1), color="tab:green", alpha=0.2)
ax.fill_between(np.arange(2015,2101,1), np.mean(ssp5, axis=1)-np.std(ssp5, axis=1), np.mean(ssp5, axis=1)+np.std(ssp5, axis=1), color="tab:red", alpha=0.2)

ax.plot(np.arange(1850,2015,1), np.mean(hist, axis=1), color="black", label="Historical")
ax.plot(np.arange(2015,2101,1), np.mean(ssp1, axis=1), color="tab:blue", label="SSP1-2.6")
ax.plot(np.arange(2015,2101,1), np.mean(ssp2, axis=1), color="tab:orange", label="SSP2-4.5")
ax.plot(np.arange(2015,2101,1), np.mean(ssp3, axis=1), color="tab:green", label="SSP3-7.0")
ax.plot(np.arange(2015,2101,1), np.mean(ssp5, axis=1), color="tab:red", label="SSP5-8.5")
#ax.plot(np.arange(1950,2101,1), melt, color="tab:brown", label="Evaluation")
ax.plot(np.arange(1958,2019,1), racmo, color="tab:pink", label="RACMO2.3p2", linewidth=1)

#from scipy.stats import linregress
#slope, _, _, p, err = linregress(np.arange(2015,2101,1)[-20:], np.mean(ssp3, axis=1)[-20:])
#slope, _, _, p, err = linregress(np.arange(1850,2015,1)[140:], np.mean(hist, axis=1)[140:])
#print(slope, err, p)
#sys.exit()

#print(np.std(np.mean(ssp5, axis=1)[-20:]))
#sys.exit()

ax.legend(frameon=False)
ax.set_xlabel("Year")
ax.set_xticks(np.arange(1850,2101,20))

ax.set_xlim([1850,2100])
ax.minorticks_on()

ax.tick_params("both", length=6, width=0.6, which="major", bottom=True, top=True, left=True, right=True)
ax.tick_params("both", length=3, width=0.2, which="minor", bottom=True, top=True, left=True, right=True)

plt.savefig("{}/mp_cesm2.pdf".format(plotdir))
