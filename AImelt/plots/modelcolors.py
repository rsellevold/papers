# Make an alphabetical dict of all climate models
# assign a number and a color code to each model
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import os, yaml, sys, cmocean

scratchdir = "/glade/scratch/raymonds/AImelt/CMIP6"

models = []
for scenario in ["ssp126","ssp245","ssp370","ssp585"]:
    for key in ["zg", "tas", "clt", "psl", "radin", "prsn"]:
        cms = os.listdir("{}/{}/{}".format(scratchdir,scenario,key))
        for cm in cms:
            models.append(cm)

models = list(dict.fromkeys(models))
models.sort()
cmmodels = {}
for n,cm in enumerate(models):
    cmmodels[cm] = n

cmap = plt.get_cmap("rainbow",len(models))
markers = ["o","v","^","<",">"]
for n in range(cmap.N):
    rgb = cmap(n)[:3]
    cmmodels[models[n]] = [n, clr.rgb2hex(rgb), False, markers[n%len(markers)]]

with open('cmclr.yml', 'w') as outfile:
        yaml.dump(cmmodels, outfile, default_flow_style=False)
