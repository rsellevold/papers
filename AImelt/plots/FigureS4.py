import os,sys
import yaml
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
plt.style.use("publication")

# Load data
CNRMCM6_histo_NN = np.load("../data/MARcomp.CNRM-CM6-1.historical.npy")
CNRMCM6_mean_melt = np.mean(CNRMCM6_histo_NN[:,129:149], axis=1)
CNRMCM6_histo_NN = CNRMCM6_histo_NN - CNRMCM6_mean_melt[...,np.newaxis]
CNRMCM6_ssp126_NN = np.load("../data/MARcomp.CNRM-CM6-1.ssp126.npy") - CNRMCM6_mean_melt[...,np.newaxis]
CNRMCM6_ssp585_NN = np.load("../data/MARcomp.CNRM-CM6-1.ssp585.npy") - CNRMCM6_mean_melt[...,np.newaxis]

CNRMESM2_histo_NN = np.load("../data/MARcomp.CNRM-ESM2-1.historical.npy")
CNRMESM2_mean_melt = np.mean(CNRMESM2_histo_NN[:,129:149])
CNRMESM2_histo_NN = CNRMESM2_histo_NN - CNRMESM2_mean_melt[...,np.newaxis]
CNRMESM2_ssp585_NN = np.load("../data/MARcomp.CNRM-ESM2-1.ssp585.npy") - CNRMESM2_mean_melt[...,np.newaxis]

UKMO_histo_NN = np.load("../data/MARcomp.UKESM1-0-LL.historical.npy")
UKMO_mean_melt = np.mean(UKMO_histo_NN[:,129:149])
UKMO_histo_NN = UKMO_histo_NN - UKMO_mean_melt[...,np.newaxis]
UKMO_ssp585_NN = np.load("../data/MARcomp.UKESM1-0-LL.ssp585.npy") - UKMO_mean_melt[...,np.newaxis]

MRIESM2_histo_NN = np.load("../data/MARcomp.MRI-ESM2-0.historical.npy")
MRIESM2_mean_melt = np.mean(MRIESM2_histo_NN[:,129:149])
MRIESM2_histo_NN = MRIESM2_histo_NN - MRIESM2_mean_melt[...,np.newaxis]
MRIESM2_ssp585_NN = np.load("../data/MARcomp.MRI-ESM2-0.ssp585.npy") - MRIESM2_mean_melt[...,np.newaxis]

CESM2_histo_NN = np.load("../data/MARcomp.CESM2.historical.npy")
CESM2_mean_melt = np.mean(CESM2_histo_NN[:,129:149])
CESM2_histo_NN = CESM2_histo_NN - CESM2_mean_melt[...,np.newaxis]
CESM2_ssp585_NN = np.load("../data/MARcomp.CESM2.ssp585.npy") - CESM2_mean_melt[...,np.newaxis]


# Load MAR data
CNRMCM6_histo_MAR = np.load("/glade/scratch/raymonds/MARPROC/CNRMCM6.histo.npy")
CNRMCM6_mean_melt = np.mean(CNRMCM6_histo_MAR[29:49])
CNRMCM6_histo_MAR = CNRMCM6_histo_MAR - CNRMCM6_mean_melt
CNRMCM6_ssp126_MAR = np.load("/glade/scratch/raymonds/MARPROC/CNRMCM6.ssp126.npy") - CNRMCM6_mean_melt
CNRMCM6_ssp585_MAR = np.load("/glade/scratch/raymonds/MARPROC/CNRMCM6.ssp585.npy") - CNRMCM6_mean_melt

CNRMESM2_histo_MAR = np.load("/glade/scratch/raymonds/MARPROC/CNRMESM2.histo.npy")
CNRMESM2_mean_melt = np.mean(CNRMESM2_histo_MAR[29:49])
CNRMESM2_histo_MAR = CNRMESM2_histo_MAR - CNRMESM2_mean_melt
CNRMESM2_ssp585_MAR = np.load("/glade/scratch/raymonds/MARPROC/CNRMESM2.ssp585.npy") - CNRMESM2_mean_melt

MRIESM2_histo_MAR = np.load("/glade/scratch/raymonds/MARPROC/MRIESM2.histo.npy")
MRIESM2_mean_melt = np.mean(MRIESM2_histo_MAR[29:49])
MRIESM2_histo_MAR = MRIESM2_histo_MAR - MRIESM2_mean_melt
MRIESM2_ssp585_MAR = np.load("/glade/scratch/raymonds/MARPROC/MRIESM2.ssp585.npy") - MRIESM2_mean_melt

UKMO_histo_MAR = np.load("/glade/scratch/raymonds/MARPROC/UKESM1.histo.npy")
UKMO_mean_melt = np.mean(UKMO_histo_MAR[29:49])
UKMO_histo_MAR = UKMO_histo_MAR - UKMO_mean_melt
UKMO_ssp585_MAR = np.load("/glade/scratch/raymonds/MARPROC/UKESM1.ssp585.npy") - UKMO_mean_melt

CESM2_histo_MAR = np.load("/glade/scratch/raymonds/MARPROC/CESM2.histo.npy")
CESM2_mean_melt = np.mean(CESM2_histo_MAR[29:49])
CESM2_histo_MAR = CESM2_histo_MAR - CESM2_mean_melt
CESM2_ssp585_MAR = np.load("/glade/scratch/raymonds/MARPROC/CESM2.ssp585.npy") - CESM2_mean_melt


a = np.empty(shape=(5,165))
a[0,:] = np.mean(CNRMCM6_histo_NN,axis=0)
a[1,:] = np.mean(CNRMESM2_histo_NN,axis=0)
a[2,:] = np.mean(MRIESM2_histo_NN,axis=0)
a[3,:] = np.mean(UKMO_histo_NN,axis=0)
a[4,:] = np.mean(CESM2_histo_NN,axis=0)

histmelt = np.mean(np.mean(a,axis=0)[129:149])

print(np.mean(np.mean(a,axis=0)[129:149]))
print(np.mean(np.std(a,axis=0)[129:149]))

b = np.empty(shape=(5,86))
b[0,:] = np.mean(CNRMCM6_ssp585_NN,axis=0)
b[1,:] = np.mean(CNRMESM2_ssp585_NN,axis=0)
b[2,:] = np.mean(MRIESM2_ssp585_NN,axis=0)
b[3,:] = np.mean(UKMO_ssp585_NN,axis=0)
b[4,:] = np.mean(CESM2_ssp585_NN,axis=0)
b = b-histmelt
print(np.mean(np.mean(b,axis=0)[-20:]))
print(np.mean(np.std(b,axis=0)[-20:]))

print(np.mean(np.mean(CNRMCM6_ssp126_NN,axis=0)[-20:])-histmelt)

#sys.exit()

fig = plt.figure(figsize=(7.3,8))

ax1 = plt.subplot(3,2,1)
ax1.set_title(r"(a) Surface melt CNRM-CM6-1 (Gt yr$^{-1}$)", loc="left", y=1.03)
ax1.fill_between(np.arange(1850,2015,1), np.mean(CNRMCM6_histo_NN,axis=0)+np.std(CNRMCM6_histo_NN,axis=0), np.mean(CNRMCM6_histo_NN,axis=0)-np.std(CNRMCM6_histo_NN,axis=0), color="black", alpha=0.2)
ax1.fill_between(np.arange(2015,2101,1), np.mean(CNRMCM6_ssp126_NN,axis=0)+np.std(CNRMCM6_ssp126_NN,axis=0), np.mean(CNRMCM6_ssp126_NN,axis=0)-np.std(CNRMCM6_ssp126_NN,axis=0), color="tab:blue", alpha=0.2)
ax1.fill_between(np.arange(2015,2101,1), np.mean(CNRMCM6_ssp585_NN,axis=0)+np.std(CNRMCM6_ssp585_NN,axis=0), np.mean(CNRMCM6_ssp585_NN,axis=0)-np.std(CNRMCM6_ssp585_NN,axis=0), color="tab:red", alpha=0.2)
ax1.plot(np.arange(1850,2015,1), np.mean(CNRMCM6_histo_NN,axis=0), color="black", linestyle="dotted", label="Historical ANNs")
ax1.plot(np.arange(2015,2101,1), np.mean(CNRMCM6_ssp126_NN,axis=0), color="tab:blue", linestyle="dotted", label="SSP1-2.6 ANNs")
ax1.plot(np.arange(2015,2101,1), np.mean(CNRMCM6_ssp585_NN,axis=0), color="tab:red", linestyle="dotted", label="SSP5-8.5 ANNs")
ax1.plot(np.arange(1950,2015,1), CNRMCM6_histo_MAR, color="black", label="Historical MAR")
ax1.plot(np.arange(2015,2101,1), CNRMCM6_ssp126_MAR, color="tab:blue", label="SSP1-2.6 MAR")
ax1.plot(np.arange(2015,2101,1), CNRMCM6_ssp585_MAR, color="tab:red", label="SSP5-8.5 MAR")
ax1.legend(frameon=False, ncol=2)
ax1.set_xticks(np.arange(1850,2101,20))
ax1.set_xlim([1950,2100])
ax1.set_ylim([-500,3500])
ax1.set_xlabel("Year")
ax1.minorticks_on()
ax1.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax1.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)

ax2 = plt.subplot(3,2,2)
ax2.set_title(r"(b) Surface melt CNRM-ESM2-1 (Gt yr$^{-1}$)", loc="left", y=1.03)
ax2.fill_between(np.arange(1850,2015,1), np.mean(CNRMESM2_histo_NN,axis=0)+np.std(CNRMESM2_histo_NN,axis=0), np.mean(CNRMESM2_histo_NN,axis=0)-np.std(CNRMESM2_histo_NN,axis=0), color="black", alpha=0.2)
ax2.fill_between(np.arange(2015,2101,1), np.mean(CNRMESM2_ssp585_NN,axis=0)+np.std(CNRMESM2_ssp585_NN,axis=0), np.mean(CNRMESM2_ssp585_NN,axis=0)-np.std(CNRMESM2_ssp585_NN,axis=0), color="tab:red", alpha=0.2)
ax2.plot(np.arange(1850,2015,1), np.mean(CNRMESM2_histo_NN,axis=0), color="black", linestyle="dotted", label="Historical")
ax2.plot(np.arange(2015,2101,1), np.mean(CNRMESM2_ssp585_NN,axis=0), color="tab:red", linestyle="dotted", label="SSP5-8.5")
ax2.plot(np.arange(1950,2015,1), CNRMESM2_histo_MAR, color="black")
ax2.plot(np.arange(2015,2101,1), CNRMESM2_ssp585_MAR, color="tab:red")
ax2.set_xticks(np.arange(1850,2101,20))
ax2.set_xlim([1950,2100])
ax2.set_ylim([-500,3500])
ax2.set_xlabel("Year")
ax2.minorticks_on()
ax2.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax2.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)

ax3 = plt.subplot(3,2,3)
ax3.set_title(r"(c) Surface melt MRI-ESM2-0 (Gt yr$^{-1}$)", loc="left", y=1.03)
ax3.fill_between(np.arange(1850,2015,1), np.mean(MRIESM2_histo_NN,axis=0)+np.std(MRIESM2_histo_NN,axis=0), np.mean(MRIESM2_histo_NN,axis=0)-np.std(MRIESM2_histo_NN,axis=0), color="black", alpha=0.2)
ax3.fill_between(np.arange(2015,2101,1), np.mean(MRIESM2_ssp585_NN,axis=0)+np.std(MRIESM2_ssp585_NN,axis=0), np.mean(MRIESM2_ssp585_NN,axis=0)-np.std(MRIESM2_ssp585_NN,axis=0), color="tab:red", alpha=0.2)
ax3.plot(np.arange(1850,2015,1), np.mean(MRIESM2_histo_NN,axis=0), color="black", linestyle="dotted", label="Historical")
ax3.plot(np.arange(2015,2101,1), np.mean(MRIESM2_ssp585_NN,axis=0), color="tab:red", linestyle="dotted", label="SSP5-8.5")
ax3.plot(np.arange(1950,2015,1), MRIESM2_histo_MAR, color="black")
ax3.plot(np.arange(2015,2101,1), MRIESM2_ssp585_MAR, color="tab:red")
ax3.set_xticks(np.arange(1850,2101,20))
ax3.set_xlim([1950,2100])
ax3.set_ylim([-500,3500])
ax3.set_xlabel("Year")
ax3.minorticks_on()
ax3.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax3.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)

ax4 = plt.subplot(3,2,4)
ax4.set_title(r"(d) Surface melt UKESM1-0-LL (Gt yr$^{-1}$)", loc="left", y=1.03)
ax4.fill_between(np.arange(1850,2015,1), np.mean(UKMO_histo_NN,axis=0)+np.std(UKMO_histo_NN,axis=0), np.mean(UKMO_histo_NN,axis=0)-np.std(UKMO_histo_NN,axis=0), color="black", alpha=0.2)
ax4.fill_between(np.arange(2015,2101,1), np.mean(UKMO_ssp585_NN,axis=0)+np.std(UKMO_ssp585_NN,axis=0), np.mean(UKMO_ssp585_NN,axis=0)-np.std(UKMO_ssp585_NN,axis=0), color="tab:red", alpha=0.2)
ax4.plot(np.arange(1850,2015,1), np.mean(UKMO_histo_NN,axis=0), color="black", linestyle="dotted", label="Historical")
ax4.plot(np.arange(2015,2101,1), np.mean(UKMO_ssp585_NN,axis=0), color="tab:red", linestyle="dotted", label="SSP5-8.5")
ax4.plot(np.arange(1950,2015,1), UKMO_histo_MAR, color="black")
ax4.plot(np.arange(2015,2101,1), UKMO_ssp585_MAR, color="tab:red")
ax4.set_xticks(np.arange(1850,2101,20))
ax4.set_xlim([1950,2100])
ax4.set_ylim([-500,3500])
ax4.set_xlabel("Year")
ax4.minorticks_on()
ax4.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax4.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)


ax5 = plt.subplot(3,2,5)
ax5.set_title(r"(e) Surface melt CESM2 (Gt yr$^{-1}$)", loc="left", y=1.03)
ax5.fill_between(np.arange(1850,2015,1), np.mean(CESM2_histo_NN,axis=0)+np.std(CESM2_histo_NN,axis=0), np.mean(CESM2_histo_NN,axis=0)-np.std(CESM2_histo_NN,axis=0), color="black", alpha=0.2)
ax5.fill_between(np.arange(2015,2101,1), np.mean(CESM2_ssp585_NN,axis=0)+np.std(CESM2_ssp585_NN,axis=0), np.mean(CESM2_ssp585_NN,axis=0)-np.std(CESM2_ssp585_NN,axis=0), color="tab:red", alpha=0.2)
ax5.plot(np.arange(1850,2015,1), np.mean(CESM2_histo_NN,axis=0), color="black", linestyle="dotted", label="Historical")
ax5.plot(np.arange(2015,2101,1), np.mean(CESM2_ssp585_NN,axis=0), color="tab:red", linestyle="dotted", label="SSP5-8.5")
ax5.plot(np.arange(1950,2015,1), CESM2_histo_MAR, color="black")
ax5.plot(np.arange(2015,2101,1), CESM2_ssp585_MAR, color="tab:red")
ax5.set_xticks(np.arange(1850,2101,20))
ax5.set_xlim([1950,2100])
ax5.set_ylim([-500,3500])
ax5.set_xlabel("Year")
ax5.minorticks_on()
ax5.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax5.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)

plt.tight_layout()
plt.savefig("/glade/work/raymonds/pyCESM/AImelt/two/CMIP6_projection_mar.pdf", dpi=500)
