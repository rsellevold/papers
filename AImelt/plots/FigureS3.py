import yaml
import matplotlib.pyplot as plt
import numpy as np
plt.style.use("publication")

fig = plt.figure(figsize=(7.3,8))
ax1 = plt.subplot(1,1,1)
ax1.set_title(r"End of century melt anomaly (Gt yr$^{-1}$)", loc="left", y=1.01)

with open("cmclr.yml", "r") as f:
    cmclr = yaml.safe_load(f)

markers = ["o","v","^","<",">"]
i = 0
for model,item in cmclr.items():
    for scenario in ["ssp370"]:#["ssp126","ssp245","ssp370","ssp585"]:
        try:
            temp = np.load(f"../data/temp.{model}.{scenario}.npy")[0,:]
            temp = np.mean(temp[-20:])
            melt = np.load(f"../data/{model}.{scenario}.npy")
            melt = np.mean(np.mean(melt,axis=0)[-20:]) - 521
            print(model,scenario,melt,temp)
            if item[2]:
                ax1.scatter(temp, melt, c=item[1], marker=item[3])
            else:
                ax1.scatter(temp, melt, c=item[1], marker=item[3], label=model)
                item[2] = True
        except FileNotFoundError:
            None

ax1.legend(ncol=2,frameon=False)
ax1.minorticks_on()
ax1.tick_params("both", length=6, width=0.8, which="major", bottom=True, top=True, left=True, right=True)
ax1.tick_params("both", length=2, width=0.4, which="minor", bottom=True, top=True, left=True, right=True)
ax1.set_xlabel("Global mean temperature anomaly (K)")
plt.tight_layout()
plt.savefig("/glade/work/raymonds/pyCESM/AImelt/temp_and_melt.pdf", dpi=500)
