import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
plt.style.use("publication")

for m in ["glbmean","proj"]:
    for sc in ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]:
        vars()[m+"_"+sc] = np.load(m+"_"+sc+".npy")

meanmelt = np.mean(np.mean(proj_historical,axis=0)[129:149])
meantemp = np.mean(np.mean(glbmean_historical,axis=0)[129:149])
print(meantemp)

for sc in ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]:
    vars()["proj_"+sc] = vars()["proj_"+sc]

print(np.mean(np.std(proj_ssp585,axis=0)[-20:]))

fig = plt.figure(figsize=(7.3,9))

ax1 = plt.subplot(2,2,1)
ax1.set_title(r"(a) Global mean T$_{2m}$ anomaly (K)", loc="left", y=1.02)
ax1.fill_between(np.arange(1850,2015,1), np.mean(glbmean_historical,axis=0)-meantemp-0.5*np.std(glbmean_historical,axis=0), np.mean(glbmean_historical,axis=0)-meantemp+0.5*np.std(glbmean_historical,axis=0), color="black", alpha=0.2)
ax1.fill_between(np.arange(2015,2101,1), np.mean(glbmean_ssp126,axis=0)-meantemp-0.5*np.std(glbmean_ssp126,axis=0), np.mean(glbmean_ssp126,axis=0)-meantemp+0.5*np.std(glbmean_ssp126,axis=0), color="tab:blue", alpha=0.2)
ax1.fill_between(np.arange(2015,2101,1), np.mean(glbmean_ssp245,axis=0)-meantemp-0.5*np.std(glbmean_ssp245,axis=0), np.mean(glbmean_ssp245,axis=0)-meantemp+0.5*np.std(glbmean_ssp245,axis=0), color="tab:orange", alpha=0.2)
ax1.fill_between(np.arange(2015,2101,1), np.mean(glbmean_ssp370,axis=0)-meantemp-0.5*np.std(glbmean_ssp370,axis=0), np.mean(glbmean_ssp370,axis=0)-meantemp+0.5*np.std(glbmean_ssp370,axis=0), color="tab:green", alpha=0.2)
ax1.fill_between(np.arange(2015,2101,1), np.mean(glbmean_ssp585,axis=0)-meantemp-0.5*np.std(glbmean_ssp585,axis=0), np.mean(glbmean_ssp585,axis=0)-meantemp+0.5*np.std(glbmean_ssp585,axis=0), color="tab:red", alpha=0.2)
ax1.plot(np.arange(1850,2015,1), np.mean(glbmean_historical,axis=0)-meantemp, color="black", label="Historical")
ax1.plot(np.arange(2015,2101,1), np.mean(glbmean_ssp126,axis=0)-meantemp, color="tab:blue", label="SSP1-2.6")
ax1.plot(np.arange(2015,2101,1), np.mean(glbmean_ssp245,axis=0)-meantemp, color="tab:orange", label="SSP2-4.5")
ax1.plot(np.arange(2015,2101,1), np.mean(glbmean_ssp370,axis=0)-meantemp, color="tab:green", label="SSP3-7.0")
ax1.plot(np.arange(2015,2101,1), np.mean(glbmean_ssp585,axis=0)-meantemp, color="tab:red", label="SSP5-8.5")
ax1.minorticks_on()
ax1.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax1.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)
ax1.set_xlabel("Year")
ax1.set_xlim([1950,2100])
ax1.set_ylim([-0.5, 5.8])
ax1.legend(frameon=False)
pos = ax1.get_position()
ax1.set_position([pos.x0-0.01, pos.y0-0.07, pos.width, pos.height+0.1])

ax2 = plt.subplot(2,2,2)
ax2.set_title(r"(b) Melt anomaly (Gt yr$^{-1}$)", loc="left", y=1.02)
ax2.fill_between(np.arange(1850,2015,1), np.mean(proj_historical,axis=0)-meanmelt-0.5*np.std(proj_historical,axis=0), np.mean(proj_historical,axis=0)-meanmelt+0.5*np.std(proj_historical,axis=0), color="black", alpha=0.2)
ax2.fill_between(np.arange(2015,2101,1), np.mean(proj_ssp126,axis=0)-meanmelt-0.5*np.std(proj_ssp126,axis=0), np.mean(proj_ssp126,axis=0)-meanmelt+0.5*np.std(proj_ssp126,axis=0), color="tab:blue", alpha=0.2)
ax2.fill_between(np.arange(2015,2101,1), np.mean(proj_ssp245,axis=0)-meanmelt-0.5*np.std(proj_ssp245,axis=0), np.mean(proj_ssp245,axis=0)-meanmelt+0.5*np.std(proj_ssp245,axis=0), color="tab:orange", alpha=0.2)
ax2.fill_between(np.arange(2015,2101,1), np.mean(proj_ssp370,axis=0)-meanmelt-0.5*np.std(proj_ssp370,axis=0), np.mean(proj_ssp370,axis=0)-meanmelt+0.5*np.std(proj_ssp370,axis=0), color="tab:green", alpha=0.2)
ax2.fill_between(np.arange(2015,2101,1), np.mean(proj_ssp585,axis=0)-meanmelt-0.5*np.std(proj_ssp585,axis=0), np.mean(proj_ssp585,axis=0)-meanmelt+0.5*np.std(proj_ssp585,axis=0), color="tab:red", alpha=0.2)
ax2.plot(np.arange(1850,2015,1), np.mean(proj_historical,axis=0)-meanmelt, color="black", label="Historical")
ax2.plot(np.arange(2015,2101,1), np.mean(proj_ssp126,axis=0)-meanmelt, color="tab:blue", label="SSP1-2.6")
ax2.plot(np.arange(2015,2101,1), np.mean(proj_ssp245,axis=0)-meanmelt, color="tab:orange", label="SSP2-4.5")
ax2.plot(np.arange(2015,2101,1), np.mean(proj_ssp370,axis=0)-meanmelt, color="tab:green", label="SSP3-7.0")
ax2.plot(np.arange(2015,2101,1), np.mean(proj_ssp585,axis=0)-meanmelt, color="tab:red", label="SSP5-8.5")
ax2.minorticks_on()
ax2.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax2.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)
ax2.set_xlabel("Year")
ax2.set_xlim([1950,2100])
ax2.set_ylim([-200, 2000])
pos = ax2.get_position()
ax2.set_position([pos.x0+0.01, pos.y0-0.07, pos.width, pos.height+0.1])

varunc = np.load("varunc.npy")
ensunc = np.load("ensunc.npy")
modunc = np.load("modunc.npy")
scenunc = np.load("scenunc.npy")

ax3 = plt.subplot(2,2,3)
ax3.set_title(r"(c) Source of uncertainty (Gt yr$^{-1}$)", loc="left", y=1.02)
ax3.plot(np.arange(1850,2101,1), varunc, color="tab:purple", label="Variable")
ax3.plot(np.arange(1850,2101,1), ensunc, color="tab:olive", label="Internal climate")
ax3.plot(np.arange(1850,2101,1), modunc, color="tab:cyan", label="Model")
ax3.plot(np.arange(2015,2101,1), scenunc, color="tab:pink", label="Scenario")
ax3.legend(frameon=False)
ax3.minorticks_on()
ax3.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax3.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)
ax3.set_xlabel("Year")
ax3.set_xlim([1950,2100])
pos = ax3.get_position()
ax3.set_position([pos.x0-0.01, pos.y0+0.01, pos.width*2+0.09, pos.height-0.1])

plt.savefig("/glade/work/raymonds/pyCESM/AImelt/two/tproj.pdf")
