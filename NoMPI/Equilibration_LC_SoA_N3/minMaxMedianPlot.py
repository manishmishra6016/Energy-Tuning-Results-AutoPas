import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

time_data = {
    "C04": [9753.0, 9774.0, 9788.7, 9801.2, 9702.0, 9715.5, 9737.6, 9803.8, 9705.9, 9798.3],  #Mean: 9758.0  Median: 9763.5
    "Sliced": [9686.7, 9496.6, 9719.4, 9709.0, 9738.4, 9728.3, 9716.0, 9720.1, 9620.7, 9753.0], #Mean: 9688.82 Median: 9717.7
    "Time-Optimal": [9842.5, 9686.9, 9751.8, 9690.5, 9778.9, 9689.7, 9767.0, 9833.1, 9742.0, 9644.6], #Mean: 9742.7 Median: 9746.9 worst: 9842.5
    "Energy-Optimal": [9553.5, 9643.2, 9774.1, 9745.9, 9662.0, 9880.8, 9781.5, 9629.5, 9520.3, 9570.1], #Mean:  9676.09 Median:  9652.6, worst:9880.8
}

# top 3 worst runs for time-optimal -1, 7, 8 
# top 3 worst runs for energy-optimal - 2, 6, 7
energy_data = {
    "C04": [3876.7, 3767.3, 3822.1, 3878.2, 3842.1, 3788.7, 3727.4, 3867.1, 3844.2, 3880.0],  #Mean:  3829.4 Median: 3843.1
    "Sliced": [3596.1, 3488.4, 3637.1, 3633.0, 3676.8, 3708.1, 3682.8, 3577.4, 3515.4, 3686.6], #Mean:  3620.2 Median: 3635.0 
    "Time-Optimal": [3900, 3621.4, 3622.9, 3569.3, 3627.9, 3605.2, 3709.9, 3798.1, 3641.3, 3652.1], #Mean: 3674.8 Median:  3634.6, worst: 3900
    "Energy-Optimal": [3458.8, 3669.0, 3664.5, 3577.4, 3649.4, 3760.5, 3667.6, 3577.7, 3494.1, 3626.2], #Mean: 3614.5 Median: 3637.8 , worst: 3760.5
}

# Data for iterations>1000
# Median, mean values are copied from above and are not correct.
"""
time_data = {
    "C04": [9657.5, 9678.2, 9692.6, 9704.9, 9606.8, 9620.2, 9641.8, 9707.7, 9610.7, 9702.5],  #Mean: 9758.0  Median: 9763.5
    "Sliced": [9593.4, 9405.3, 9626.8, 9616.1, 9644.8, 9635.4, 9622.8, 9627.0, 9528.3, 9659.6], #Mean: 9688.82 Median: 9717.7
    "Time Optimal": [9742.3, 9594.1, 9658.5, 9597.5, 9684.8, 9596.4, 9673.4, 9738.7, 9648.5, 9552.1], #Mean: 9742.7 Median: 9746.9
    "Energy Optimal": [9462.3, 9550.8, 9680.5, 9652.4, 9569.4, 9786.0, 9687.7, 9537.1, 9429.1, 9478.0], #Mean:  9676.09 Median:  9652.6
}

energy_data = {
    "C04": [3838.9, 3730.4, 3784.7, 3840.2, 3804.4, 3751.6, 3690.9, 3829.4, 3806.5, 3842.2],  #Mean:  3829.4 Median: 3843.1
    "Sliced": [3561.4, 3454.9, 3602.4, 3598.1, 3641.4, 3672.7, 3647.5, 3543.0, 3481.6, 3651.2], #Mean:  3620.2 Median: 3635.0 
    "Time Optimal": [3862.6, 3587.3, 3588.4, 3535.0, 3593.1, 3570.5, 3674.5, 3762.0, 3606.6, 3617.2], #Mean: 3674.8 Median:  3634.6
    "Energy Optimal": [3425.6, 3633.8, 3629.4, 3543.0, 3614.4, 3724.4, 3632.3, 3523.6, 3460.5, 3591.4], #Mean: 3614.5 Median: 3637.8 
}
"""

fig, (ax_time, ax_energy) = plt.subplots(
    2, 1, sharex=True, figsize=(8, 5), constrained_layout=True
)

cases = ["C04", "Sliced", "Time-Optimal", "Energy-Optimal"]
positions = np.arange(len(cases))

offset = 0.0  # no grouping needed since separate subplots
single_config_marker='^'

# ---- TIME PLOT ----
for i, case in enumerate(cases):
    d = np.array(time_data[case])  # list of 10 runs

    min_val = d.min()
    max_val = d.max()
    median_val = np.median(d)
    mean_val = np.mean(d)
    print(case,"(time) -- Mean: ", mean_val," -- Median: ", median_val)

    x = positions[i]

    ax_time.vlines(x, min_val, max_val, color="tab:blue", linewidth=1)
    ax_time.plot([x-0.2, x+0.2], [median_val, median_val],
                 color="tab:blue", linewidth=3)
    ax_time.plot([x-0.2, x+0.2], [mean_val, mean_val],
                 color="tab:blue", linestyle = "--", linewidth=3)

    jitter = np.random.normal(x, 0.1, size=len(d))
    if (case == "C04" or case == "Sliced"):
        ax_time.plot(jitter, d, single_config_marker, alpha=0.6, color="tab:blue")
    if (case == "Time-Optimal"):
        for i in [0, 1, 2, 5, 6, 7, 8]:
            ax_time.plot(jitter[i], d[i], 'X', alpha=0.6, color="tab:blue")
        for i in [3, 4, 9]:
            ax_time.plot(jitter[i], d[i], 'o', alpha=0.6, color="tab:blue")
    elif (case == "Energy-Optimal"):
        ax_time.plot(jitter, d, 'o', alpha=0.6, color="tab:blue")

ax_time.set_ylabel("Time (s)", fontsize=14)
ax_time.set_ylim(9450,10100)
#ax_time.set_title("Runtime Variability")
ax_time.tick_params(axis="y", labelsize=12)

# ---- ENERGY PLOT ----
for i, case in enumerate(cases):
    d = np.array(energy_data[case])

    min_val = d.min()
    max_val = d.max()
    median_val = np.median(d)
    mean_val = np.mean(d)
    print(case,"(Energy) -- Mean: ", mean_val," -- Median: ", median_val)

    x = positions[i]

    ax_energy.vlines(x, min_val, max_val, color="tab:orange", linewidth=1)
    ax_energy.plot([x-0.2, x+0.2], [median_val, median_val],
                   color="tab:orange", linewidth=3)
    ax_energy.plot([x-0.2, x+0.2], [mean_val, mean_val],
                 color="tab:orange", linestyle = "--", linewidth=3)

    jitter = np.random.normal(x, 0.02, size=len(d))
    if (case == "C04" or case == "Sliced"):
        ax_energy.plot(jitter, d, single_config_marker, alpha=0.6, color="tab:orange")
    if (case == "Time-Optimal"):
        for i in [0, 1, 2, 5, 6, 7, 8]:
            ax_energy.plot(jitter[i], d[i], 'X', alpha=0.6, color="tab:orange")
        for i in [3, 4, 9]:
            ax_energy.plot(jitter[i], d[i], 'o', alpha=0.6, color="tab:orange")
    elif (case == "Energy-Optimal"):
        ax_energy.plot(jitter, d, 'o', alpha=0.6, color="tab:orange")
    #ax_energy.plot(jitter, d, 'o', alpha=0.6, color="tab:orange")

ax_energy.set_ylabel("Energy (KJ)", fontsize=14)
ax_energy.set_ylim(3420,3950)
ax_energy.set_xticks(positions)
ax_energy.set_xticklabels(cases, fontsize=14)
ax_energy.tick_params(axis="y", labelsize=12)

# Custom legend handles (marker-only, black, no lines)
legend_elements = [
    Line2D([0], [0], marker='^', color='black', linestyle='None',
           markersize=8, label='Single Configuration (C04, Sliced)'),
    Line2D([0], [0], marker='o', color='black', linestyle='None',
           markersize=8, label='Less than 15% C04'),
    Line2D([0], [0], marker='X', color='black', linestyle='None',
           markersize=8, label='More than 15% C04'),
    Line2D([0], [0], color='black', linewidth=3, label='Median'),
    Line2D([0], [0], color='black', linestyle='--', linewidth=3, label='Mean'),
]

# Add legend only once
fig.legend(handles=legend_elements,
           loc="upper center",
           bbox_to_anchor=(0.55, 0.98),
           ncol=3,
           fontsize=11,
           frameon=True)

plt.show()
