import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
#df_all = pd.read_csv("./energy_trial2_10samples/AutoPas_iterationPerformance_Rank0_2025-09-08_15-45-10.csv")
#df_all = pd.read_csv("./time_trial1_10samples/AutoPas_iterationPerformance_Rank0_2025-09-08_18-13-30.csv")
#df_all = pd.read_csv("./time_trial1/AutoPas_iterationPerformance_Rank0_2025-09-04_14-52-40.csv")
#df_all = pd.read_csv("./energy_trial1/AutoPas_iterationPerformance_Rank0_2025-09-04_15-41-53.csv")
#df_all = pd.read_csv("./LC_C04_AoS_N3/AutoPas_iterationPerformance_Rank0_2025-09-17_13-50-57.csv")
#df_all = pd.read_csv("./LC_C04_and_VL_ListIter/AutoPas_iterationPerformance_Rank0_2025-11-17_13-30-10.csv")
df_all = pd.read_csv("./LC_C04_and_VL_ListIter_10daa56e0/AutoPas_iterationPerformance_Rank0_2026-02-22_12-11-07.csv")

print("runtime: ", df_all["computeInteractionsTotal[ns]"].sum()*1e-9)
print("Energy: ", df_all["energyJoules[J]"].sum())

# Plotting all iterations
#df = df_all[df_all["inTuningPhase"].astype(str).str.lower() == "false"]

# plotting weighted average
df_nontuning = df_all[df_all["inTuningPhase"].astype(str).str.lower() == "false"]

cols_to_keep = ["Iteration", "energyJoules[J]", "computeInteractionsTotal[ns]", "Traversal"]  
df_filt  = df_nontuning[cols_to_keep]
df_tmp = df_filt.copy()

# Create 10-iteration bins
df_tmp["Iteration_bin"] = (df_tmp["Iteration"] // 100)
# Average over bins
df = df_tmp.groupby("Iteration_bin").agg({
    "Iteration": "mean",                      # avg iteration number
    "computeInteractionsTotal[ns]": "mean",     # avg of measurement
    "energyJoules[J]" : "mean",
    "Traversal": lambda x: x.iloc[1]
}).reset_index(drop=True)

# Setup figure
fig, ax1 = plt.subplots(figsize=(10,6))
plt.rcParams['legend.fontsize'] = 14

### Plotting median config from the tuning data
#df_td = pd.read_csv("./energy_trial1/AutoPas_tuningData_Rank0_pairwise_2025-09-04_15-41-53.csv") #df_td - df_tuningData
df_td = pd.read_csv("./energy_trial1_10daa56e0/AutoPas_tuningData_Rank0_pairwise_2026-02-22_12-15-01.csv") #df_td - df_tuningData
iteration = list(range(15))
median_energy = []
median_energy_2 = []
tuningData_iterations = []
k = 9

for i in iteration:
    df_filtered = df_td[(df_td["Iteration"] >= i*10000) & (df_td["Iteration"] < (i*10000+1000))].copy()
    df_filtered["Config"] = (
        df_filtered["Container"].astype(str) + " | " +
        df_filtered["Traversal"].astype(str) + " | " +
        df_filtered["Data Layout"].astype(str) + " | " +
        df_filtered["Newton 3"].astype(str) + " | " +
        df_filtered["Load Estimator"].astype(str)
    )
    df_sorted_energy = df_filtered.sort_values(by=["Smoothed"])
    median_energy.append(df_sorted_energy.iloc[23]["Smoothed"]/1e9)
    median_energy_2.append(df_sorted_energy.iloc[k]["Smoothed"]/1e9)
    print(len(df_sorted_energy))
    tuningData_iterations.append(df_sorted_energy.iloc[k]["Iteration"])
###


# First axis: energyJoules
ax1.set_xlabel("Iteration", fontsize=14)
ax1.set_ylabel("Compute Interactions Energy (Joules)", fontsize=14) #, color="tab:green"
line1, = ax1.plot(df["Iteration"], df["energyJoules[J]"], marker="+", markersize=5, linestyle="", color="tab:green", label="Energy - AutoPas optimal AC")
#line3, = ax1.plot(tuningData_iterations, median_energy, marker="x", markersize=4, linestyle="-.", linewidth=3, color="tab:purple", label="Energy (J) - 75th percentile AC")
line4, = ax1.plot(tuningData_iterations, median_energy_2, marker="o", markersize=4, linestyle="-.", linewidth=3, color="tab:brown", label="Energy - 90th percentile AC")
ax1.tick_params(axis="y", labelsize=14) #, labelcolor="tab:green"
ax1.tick_params(axis="x", labelsize=14)



# Second axis: computeInteractionsTotal[ns]
ax2 = ax1.twinx()
ax2.set_ylabel("Compute Interactions Runtime (ms)", color="tab:blue", fontsize=14)
line2, = ax2.plot(df["Iteration"], df["computeInteractionsTotal[ns]"]*1e-6, marker="s", markersize=4, linestyle="", color="tab:blue", label="Time - AutoPas Optimal AC")
ax2.set_ylim(1, 6)
ax2.tick_params(axis="y", labelcolor="tab:blue", labelsize=14)

# Shade regions by configuration
current_config = None
start_idx = 0
colors = plt.cm.tab10.colors  # color palette
color_map = {}


shaded_patches = []

for i, row in df.iterrows():
    config = row["Traversal"]
    if config != current_config:
        if current_config is not None:
            # Shade the region for the previous config
            patch = ax1.axvspan(start_idx, row["Iteration"], 
                        facecolor=color_map[current_config], alpha=0.1,
                        label=current_config if current_config not in ax1.get_legend_handles_labels()[1] else "")
            shaded_patches.append(patch)
        # assign color if new
        if config not in color_map:
            color_map[config] = colors[len(color_map) % len(colors)]
        current_config = config
        start_idx = row["Iteration"]

# Shade final region
patch = ax1.axvspan(start_idx, row["Iteration"],
                    facecolor=color_map[current_config], alpha=0.3,
                    label=current_config if current_config not in ax1.get_legend_handles_labels()[1] else "")
shaded_patches.append(patch)

total_energy = df["energyJoules[J]"].sum()
print("Total energy (J):", total_energy)

# Combine all legend handles
handles = [line1, line4, line2] + shaded_patches
labels = [h.get_label() for h in handles]

labels[3] = "VL_ListIteration_AoS_NoN3"
labels[4] = "LC_C04_AoS_N3"
# Filter out empty labels and keep unique ones
unique = {}
for handle, label in zip(handles, labels):
    if label and label not in unique:  # non-empty & unique
        unique[label] = handle

# Title and legend
# fig.suptitle("Iteration vs Energy & ComputeInteractionTime (inTuningPhase = false)")
ax1.legend(unique.values(), unique.keys(), bbox_to_anchor=(0.45, 0.5 ), loc="center left",
           frameon=True,           # ensure a frame is drawn
           framealpha=1.0,         # fully opaque
           facecolor='white',      # background color
           edgecolor='black')      # border color


fig.tight_layout()
plt.show()



#Plotting power

df_tmp = df_all[df_all["Iteration"] < 100010]
df_tmp["Power"] = df_tmp["energyJoules[J]"]/df_tmp["computeInteractionsTotal[ns]"]*1e9


# Create 10-iteration bins
df_tmp["Iteration_bin"] = (df_tmp["Iteration"] // 1000)
# Average over bins
df = df_tmp.groupby("Iteration_bin").agg({
    "Iteration": "mean",                      # avg iteration number
    "Power": "mean"
}).reset_index(drop=True)

fig, ax1 = plt.subplots(figsize=(10,6))
plt.rcParams['legend.fontsize'] = 14

ax1.plot(df["Iteration"], df["Power"], marker="o", markersize=3, linestyle="-.", color="tab:blue", label="Power (W)")
plt.show()
