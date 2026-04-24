import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Function to read band.dat file
def read_band_dat(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    data = []
    for line in lines:
        parts = line.split()
        if len(parts) == 2:
            qpoint = float(parts[0])
            frequency = float(parts[1])
            data.append((qpoint, frequency))
    return data

# Function to read projected_dos.dat file and sum Te1 and Te2
def read_pdos_dat(filename, n_atoms):
    with open(filename, 'r') as f:
        lines = f.readlines()

    data = []
    for line in lines[1:]:  # Skip the first line
        parts = line.split()
        if len(parts) == 217:
            frequency = float(parts[0])
            pdos_ag = sum(float(part) for part in parts[1:55]) / n_atoms
            pdos_sb = sum(float(part) for part in parts[55:109]) / n_atoms
            pdos_te = sum(float(part) for part in parts[109:217]) / n_atoms
            data.append((frequency, pdos_ag, pdos_sb, pdos_te))
    return data

natoms = 216

# Read the band.dat data
band_data = read_band_dat('band.dat')

# Split data into separate branches
branches = []
current_branch = []

for qpoint, frequency in band_data:
    if qpoint == 0.0 and current_branch:
        branches.append(current_branch)
        current_branch = []
    current_branch.append((qpoint, frequency))

# Append the last branch
if current_branch:
    branches.append(current_branch)

# Read the projected_dos.dat data
pdos_data = read_pdos_dat('projected_dos.dat', natoms)
frequencies, pdos_ag, pdos_sb, pdos_te = zip(*pdos_data)

# Determine the y-axis limits
ylim_min = min(frequencies)
ylim_max = max(frequencies)

# Plotting
fig = plt.figure(figsize=(8, 8))
gs = GridSpec(1, 2, width_ratios=[2, 1], wspace=0.05)

# Plot the band structure
ax1 = fig.add_subplot(gs[0])
for branch in branches:
    qpoints, frequencies_bs = zip(*branch)
    ax1.plot(qpoints, frequencies_bs, linestyle='-', color='red')


# Set x-tick positions and labels
xtick_positions = [0.00000000, 0.02773880, 0.05553430, 0.09480760, 0.13411230, 0.16190780]
xtick_labels = [r'$\Gamma$', r'$Y$', r'$L$', r'$\Gamma$', r'$Z$', r'$N$']

ax1.set_xlabel('Wave vector', fontsize=25)
ax1.set_ylabel('Frequency (THz)', fontsize=25)
ax1.set_xticks(xtick_positions)
ax1.set_xticklabels(xtick_labels, fontsize=16)
ax1.set_xlim(0, xtick_positions[-1])
ax1.set_ylim(0, 5)
ax1.spines['top'].set_linewidth(2.0)
ax1.spines['bottom'].set_linewidth(2.0)
ax1.spines['left'].set_linewidth(2.0)
ax1.spines['right'].set_linewidth(2.0)
ax1.grid(True, linestyle='--', color='black', linewidth=1.0)
ax1.tick_params(axis='x', width=2.0, length=8, color='black', labelsize=25, direction='in')
ax1.tick_params(axis='y', width=2.0, length=8, color='black', labelsize=25, direction='in')
ax1.xaxis.grid(True)  # Turn on vertical grid lines at xticks values
ax1.yaxis.grid(False)  # Turn off y-axis grid

# Plot the projected density of states on a second subplot
ax2 = fig.add_subplot(gs[1])
ax2.plot(pdos_ag, frequencies, linestyle='-', color='#f70084', label='Ag')
ax2.plot(pdos_sb, frequencies, linestyle='-', color='#5f0e3d', label='Sb')
ax2.plot(pdos_te, frequencies, linestyle='-', color='#6464dc', label='Te')
ax2.set_xticks([1])
ax2.set_yticks([])  # Hide the y-axis ticks for the second subplot
ax2.set_xlabel('DOS', fontsize=25)
ax2.spines['top'].set_linewidth(2.0)
ax2.spines['bottom'].set_linewidth(2.0)
ax2.spines['left'].set_linewidth(2.0)
ax2.spines['right'].set_linewidth(2.0)
ax2.set_xlim(0, 1.5)
ax2.set_ylim(0, 5)
ax2.legend(fontsize=14, edgecolor='black', fancybox=False)
ax2.tick_params(axis='x', which='major', width=2.0, length=8, color='black', labelsize=25, direction='in')


plt.savefig('band_structure_pdos.png', dpi=300)

