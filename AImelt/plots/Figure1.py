import sys
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.stats as ss
plt.style.use("publication")


# Load data
areascale = (1693952*1e+6)/1e+12
varlist = ["TREFHT", "Z500", "CLDTOT", "RADIN", "PRECS"]
for key in varlist:
	f = xr.open_dataset("../models/saved/nn_10/{}/output.nc".format(key))
	vars()["meltts_{}".format(key)] = f.meltts
	vars()["meltmapts_{}".format(key)] = f.meltpermap

fm = xr.open_dataset("/glade/scratch/raymonds/SSP_HIGH/histssp/lnd/rproc/timeseries/GrIS_integrated.annavg.nc")
melt = fm.MELT_ICE.values * 1e+12 / (1844610 * 1e+6) * areascale

# Plot
colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
labels = [r"T$_{2m}$", r"Z$_{500}$", "CC", "RAD$_{in}$", "SNOW"]
fig = plt.figure(figsize=(7.3,7.3))

meltens = np.empty(shape=(5,2100-1950+1))
meltens[0,:] = meltts_TREFHT.values
meltens[1,:] = meltts_Z500.values
meltens[2,:] = meltts_CLDTOT.values
meltens[3,:] = meltts_RADIN.values
meltens[4,:] = meltts_PRECS.values

mm = np.mean(meltens, axis=0)

#_, _, r, _, _ = ss.linregress(melt, mm)
#_, _, r, _, _ = ss.linregress(melt[:132]-np.convolve(melt, np.ones((20,))/20, mode="valid"), mm[:132]-np.convolve(mm, np.ones((20,))/20, mode="valid"))
#print(np.mean(melt[-20:])-np.mean(mm[-20:]))
#sys.exit()

#ax1 = plt.subplot(3,2,1)
#ax1.set_title(r"(a) Melt (Gt yr$^{-1}$)", loc="left", y=1.04)
#ax1.fill_between(f.year.values, np.mean(meltens, axis=0)+np.std(meltens, axis=0), np.mean(meltens, axis=0)-np.std(meltens, axis=0), color="tab:blue", alpha=0.2)
#ax1.plot(f.year.values, np.mean(meltens, axis=0), color="tab:blue", linewidth=1, label="Prediction mean")
#ax1.plot(f.year.values, melt, color="black", linewidth=1, label="CESM2 simulated")
#ax1.legend(frameon=False)
#ax1.set_xlim([1950,2100])
#ax1.minorticks_on()
#ax1.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
#ax1.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)
#ax1.set_ylim([0,3000])

meltcheck = np.zeros(shape=(2100-1950+1))
mm1 = melt-(np.mean(meltens, axis=0)-0.5*np.std(meltens, axis=0))
mm2 = melt-(np.mean(meltens, axis=0)+0.5*np.std(meltens, axis=0))

for t in range(2100-1950+1):
    if mm1[t] > 0 and mm2[t]<0:
        meltcheck[t] = 1

ax3 = plt.subplot(3,2,1)
ax3.set_title(r"(a) T$_{2m}$ (Gt yr$^{-1}$)", loc="left", y=1.04)
ax3.plot(f.year.values, melt, color="black")
ax3.plot(f.year.values, meltmapts_TREFHT[0,:].values, color=colors[2], linewidth=1)
ax3.plot(f.year.values, meltmapts_TREFHT[3,:].values, color=colors[1], linewidth=1)
ax3.plot(f.year.values, meltts_TREFHT.values, color=colors[0], linewidth=1)
ax3.set_xlim([1950,2100])
ax3.minorticks_on()
ax3.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax3.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)
ax3.set_ylim([0,3000])


ax4 = plt.subplot(3,2,2)
ax4.set_title(r"(b) Z$_{500}$ (Gt yr$^{-1}$)", loc="left", y=1.04)
ax4.plot(f.year.values, melt, color="black")
ax4.plot(f.year.values, meltmapts_Z500[0,:].values, color=colors[3], linewidth=1)
ax4.plot(f.year.values, meltmapts_Z500[2,:].values, color=colors[2], linewidth=1)
ax4.plot(f.year.values, meltmapts_Z500[3,:].values, color=colors[1], linewidth=1)
ax4.plot(f.year.values, meltts_Z500.values, color=colors[0], linewidth=1)
ax4.set_xlim([1950,2100])
ax4.minorticks_on()
ax4.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax4.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)
ax4.set_ylim([0,3000])


ax5 = plt.subplot(3,2,3)
ax5.set_title(r"(c) CC (Gt yr$^{-1}$)", loc="left", y=1.04)
ax5.plot(f.year.values, melt, color="black")
ax5.plot(f.year.values, meltmapts_CLDTOT[0,:].values, color=colors[3], linewidth=1)
ax5.plot(f.year.values, meltmapts_CLDTOT[1,:].values, color=colors[2], linewidth=1)
ax5.plot(f.year.values, meltmapts_CLDTOT[2,:].values, color=colors[1], linewidth=1)
ax5.plot(f.year.values, meltts_CLDTOT.values, color=colors[0], linewidth=1)
ax5.set_xlim([1950,2100])
ax5.minorticks_on()
ax5.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax5.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)
ax5.set_ylim([0,3000])


ax7 = plt.subplot(3,2,4)
ax7.set_title(r"(d) RAD$_{in}$ (Gt yr$^{-1}$)", loc="left", y=1.04)
ax7.plot(f.year.values, melt, color="black")
ax7.plot(f.year.values, meltmapts_RADIN[3,:].values, color=colors[2], linewidth=1)
ax7.plot(f.year.values, meltmapts_RADIN[2,:].values, color=colors[1], linewidth=1)
ax7.plot(f.year.values, meltts_RADIN.values, color=colors[0], linewidth=1)
ax7.set_xlim([1950,2100])
ax7.minorticks_on()
ax7.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax7.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)
ax7.set_xlabel("Year")
ax7.set_ylim([0,3000])


ax8 = plt.subplot(3,2,5)
ax8.set_title(r"(e) SNOW (Gt yr$^{-1}$)", loc="left", y=1.04)
ax8.plot(f.year.values, melt, color="black")
ax8.plot(f.year.values, meltts_PRECS.values, color=colors[0], linewidth=1)
ax8.set_xlim([1950,2100])
ax8.minorticks_on()
ax8.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax8.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)
ax8.set_xlabel("Year")
ax8.set_ylim([0,3000])


plt.tight_layout()
plt.savefig("/glade/work/raymonds/pyCESM/AImelt/meltts_cesm2.pdf")
