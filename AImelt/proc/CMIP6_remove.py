####################
# This script removes simulations where the near-surface temperatures
# are not provided.
# Written by Raymond Sellevold (R.Sellevold-1@tudelft.nl)
####################

import os, sys

scr = "/glade/scratch/raymonds/AImelt/CMIP6"
scro = "/glade/scratch/raymonds/AImelt/CMIP6_output"

# Remove all output that does not have corresponding temperature
for scenario in ["historical","ssp126","ssp245","ssp370","ssp585"]:
    for key in ["tas", "zg", "clt", "radin", "prsn"]:
        cms = os.listdir("{}/{}/{}".format(scro,scenario,key))
        for cm in cms:
            ensembles = os.listdir("{}/{}/{}/{}".format(scro,scenario,key,cm))
            ensembles = [w.replace("_output.nc","") for w in ensembles]
            for ens in ensembles:
                f_gmt = "{}/{}/tas/{}/{}.nc".format(scr,scenario,cm,ens)
                f_ens = "{}/{}/{}/{}/{}_output.nc".format(scro,scenario,key,cm,ens)
                if not(os.path.isfile(f_gmt)):
                    print(cm,ens)
                    os.system("rm {}".format(f_ens))
