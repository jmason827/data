import re
import os
import sys
import numpy as np
import seaborn as sns
import scipy.stats as sts
import matplotlib.pyplot as plt

fin = r'D:\docs\data\datasets\ufs_violins_all_data_since_240512.csv'
with open(fin, 'r', encoding='utf-8') as f:
    lines = [re.sub(r'\n', r'', line).split(',') for line in f.readlines()]
headers = lines[0]
rows = [ {h : line[i] for i, h in enumerate(headers)} for line in lines[1:] ]

k = 'prep_plus_main (min)'
orgs = sorted(list(set([row['org'] for row in rows])))
gpns = sorted(list(set([row['gpn'] for row in rows])))
ufs_chips = sorted(list(set([row['ufs'] for row in rows])))
tc_by_gpn_by_org = {gpn : {org : [r for r in rows if r['org'] == org and r['gpn'] == gpn] for org in orgs} for gpn in gpns}
tc_by_gpn_by_org_by_ufs = {gpn : {org : {} for org in orgs} for gpn in gpns}
for gpn_010 in tc_by_gpn_by_org.keys():
    for org in tc_by_gpn_by_org[gpn_010].keys():
        for ufs in ufs_chips:
            ufs_cycle_times = [float(r[k]) for r in tc_by_gpn_by_org[gpn_010][org] if r['ufs'] == ufs]
            if len(ufs_cycle_times) > 0:
                tc_by_gpn_by_org_by_ufs[gpn_010][org][ufs] = ufs_cycle_times

tc_by_gpn_by_org = {gpn : {org : [float(r[k]) for r in rows if r['org'] == org and r['gpn'] == gpn] for org in tc_by_gpn_by_org[gpn].keys()} for gpn in tc_by_gpn_by_org.keys()}
common = {}
for gpn_010 in tc_by_gpn_by_org.keys():
    is_common = True
    for org in orgs:
        if len(tc_by_gpn_by_org[gpn_010][org]) <= 0:
            is_common = False
            break
    if is_common:
        common[gpn_010] = tc_by_gpn_by_org_by_ufs[gpn_010]

# let's look at some cycle time (prepare plus main) qq plots by org
for gpn_010 in common.keys():
    tc_max = 0
    tc_min = 9999
    for org in common[gpn_010].keys():
        ufs_labels = sorted(common[gpn_010][org].keys())
        common[gpn_010][org]['by_ufs'] = [common[gpn_010][org][ufs] for ufs in ufs_labels]
        tc_max = max([max(common[gpn_010][org][ufs]) for ufs in ufs_labels]) if max([max(common[gpn_010][org][ufs]) for ufs in ufs_labels]) > tc_max else tc_max
        tc_min = min([min(common[gpn_010][org][ufs]) for ufs in ufs_labels]) if min([min(common[gpn_010][org][ufs]) for ufs in ufs_labels]) < tc_min else tc_min
        common[gpn_010][org]['labels'] = ufs_labels

    n_bins = 150
    linspace_bins = np.linspace(tc_min, tc_max, n_bins)

    colors = ['lightcoral', 'sienna', 'deepskyblue', 'cyan', 'blue', 'darkorchid', 'fuchsia']
    colors.reverse()
    ufs_colors = {ufs : colors.pop() for ufs in ufs_chips}
    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)
    sts.probplot(tc_by_gpn_by_org[gpn_010]['G1'], dist="norm", plot=ax0)
    ax0.set_title(f"G1 {gpn_010} vs. Normal Dist.")

    labels = common[gpn_010]['G1']['labels']
    plot_colors = [ufs_colors[ufs] for ufs in labels]
    n, g1_bins, patches = ax1.hist(common[gpn_010]['G1']['by_ufs'], linspace_bins, density=False, histtype='bar', color=plot_colors, label=labels, stacked=True)
    ax1.legend(prop={'size': 10})
    ax1.set_xlabel("Cycle Time (min)")
    ax1.set_title(f'G1 {gpn_010}')

    sts.probplot(tc_by_gpn_by_org[gpn_010]['PL1'], dist="norm", plot=ax2)
    ax2.set_title(f"PL1 {gpn_010} vs. Normal Dist.")

    labels = common[gpn_010]['PL1']['labels']
    plot_colors = [ufs_colors[ufs] for ufs in labels]
    ax3.hist(common[gpn_010]['PL1']['by_ufs'], linspace_bins, density=False, histtype='bar', color=plot_colors, label=labels, stacked=True)
    ax3.legend(prop={'size': 10})
    ax3.set_xlabel("Cycle Time (min)")
    ax3.set_title(f'PL1 {gpn_010}')

    fig.tight_layout()
    plt.show()
    input()