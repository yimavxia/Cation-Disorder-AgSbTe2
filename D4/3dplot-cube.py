import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.ticker import ScalarFormatter
from matplotlib.colors import LinearSegmentedColormap


# Load data
data = np.loadtxt("array_od_xx.txt")
delta_freq = 2

nrows, ncols = data.shape
xpos, ypos = np.meshgrid(np.arange(ncols)*delta_freq, np.arange(nrows)*delta_freq)
xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros_like(xpos)
dz = data.flatten()
dx = dy = 0.9

# Filter out zero bars
nonzero_mask = dz > 0
xpos_nz = xpos[nonzero_mask]
ypos_nz = ypos[nonzero_mask]
zpos_nz = zpos[nonzero_mask]
dz_nz = dz[nonzero_mask]

colors = ['#440154', '#3b528b', '#21908d', '#5dc962', '#fde725', '#f03b20']
custom_cmap = LinearSegmentedColormap.from_list('custom_heat', colors, N=256)

# Normalize color based on bar height
norm = Normalize(vmin=0, vmax=0.04)
colors_nz = custom_cmap(norm(dz_nz))  

# Create 3D plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=40, azim=30)

# Remove background panes (gray planes)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
#ax.zaxis.pane.fill = False

# Remove grid lines
ax.grid(False)

# Set axis limits (adjust as needed)
ax.set_xlim(0, 30)
ax.set_ylim(0, 30)
ax.set_zlim(0, 0.04)
ax.invert_xaxis()
ax.invert_yaxis()

# Plot bars
ax.bar3d(xpos_nz, ypos_nz, zpos_nz, dx, dy, dz_nz, color=colors_nz, edgecolor='none')

"""
# Change tick labels manually to show 0–8
tick_locs = np.linspace(0, 0.08, 5)
ax.set_zticks(tick_locs)
ax.set_zticklabels([f'{v*100:.0f}' for v in tick_locs])  # 0, 2, 4, ..., 8
"""

ax.set_zticks([])
ax.plot([-1, -1], [30, 30], [0, 0.04], color='black', linewidth=2.5)

z_ticks = np.linspace(0, 0.04, 5)
z_subticks = np.linspace(0.005, 0.035, 4)
for z in z_ticks:
    ax.plot([-1, -0.1], [30, 30], [z, z], color='black', linewidth=1.5)
for z in z_ticks:
    if z in [0]:
        continue
    ax.text(-2.5, 31, z, f'{z*100:.0f}', fontsize=15, va='center')
for z in z_subticks :
    ax.plot([-1, -0.5], [30, 30], [z, z], color='black', linewidth=1.5)
    
ax.set_xticks([])
ax.plot([-1, 30], [-1, -1], [0, 0], color='black', linewidth=2.5)
x_ticks = np.linspace(5, 30, 6)
x_subticks = np.linspace(2.5, 27.5, 6)
for x in x_ticks:
    ax.plot([x, x], [-1, -0.1], [0, 0], color='black', linewidth=1.5)
for x in x_ticks:
    if x in [0]:
        continue
    ax.text(x, -2, 0, f'{x:.0f}', fontsize=15, va='center')
for x in x_subticks :
    ax.plot([x, x], [-1, -0.5], [0, 0], color='black', linewidth=1.5)

ax.set_yticks([])
ax.plot([-1, -1], [-1, 30], [0, 0], color='black', linewidth=2.5)
y_ticks = np.linspace(5, 30, 6)
y_subticks = np.linspace(2.5, 27.5, 6)
for y in y_ticks:
    ax.plot([-1, -0.1], [y, y], [0, 0], color='black', linewidth=1.5)
for y in y_ticks:
    if y in [0]:
        continue
    ax.text(-3.5, y, 0, f'{y:.0f}', fontsize=15, va='center')
for y in y_subticks :
    ax.plot([-1, -0.5], [y, y], [0, 0], color='black', linewidth=1.5)
    
#ax.plot([-1, 0], [-1, 0], [0, 0], color='black', linewidth=1.5)
ax.text(-2, -2, 0, f'0', fontsize=15, va='center')

# Then add unit in label
#ax.set_zlabel('Thermal conductivity ($10^{-2}$ W/mK)', fontsize=14)
#ax.set_xlabel('Frequency (rad/ps)', fontsize=18)
#ax.set_ylabel('Frequency (rad/ps)', fontsize=18)



"""
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='z', labelsize=15)
"""

# Add cube outline with dashed lines
cube_lines_front = [
    # Bottom square
    [(0,0,0), (30,0,0)],
#    [(30,0,0), (30,30,0)],
#    [(30,30,0), (0,30,0)],
    [(0,30,0), (0,0,0)],
    
    # Top square
    [(-1,-1,0.04), (30,-1,0.04)],
    [(30,-1,0.04), (30,30,0.04)],
    [(30,30,0.04), (-1,30,0.04)],
    [(-1,30,0.04), (-1,-1,0.04)],
    
    # Vertical edges
    [(-1,-1,0), (-1,-1,0.04)],
    [(30,-1,0), (30,-1,0.04)],
#    [(30,30,0), (30,30,0.08)],
    [(-1,30,0), (-1,30,0.04)],
]

for start, end in cube_lines_front:
    ax.plot([start[0], end[0]],
            [start[1], end[1]],
            [start[2], end[2]],
            color='black', linestyle='--', linewidth=0.8, zorder=5)

cube_lines_back = [
    # Bottom square                                                                                                                     
#    [(0,0,0), (30,0,0)],
    [(30,0,0), (30,30,0)],
    [(30,30,0), (0,30,0)],
#    [(0,30,0), (0,0,0)],

    # Vertical edges                                                                                                                    
#    [(-1,-1,0), (-1,-1,0.08)],
#    [(30,-1,0), (30,-1,0.08)],
    [(30,30,0), (30,30,0.04)],
#    [(-1,30,0), (-1,30,0.08)],
]

for start, end in cube_lines_back:
    ax.plot([start[0], end[0]],
            [start[1], end[1]],
            [start[2], end[2]],
            color='black', linestyle='--', linewidth=0.8, zorder=1)

    
"""
# Draw solid axis lines (replace dashed cube)
axis_lines = [
    [(0, 0, 0), (30, 0, 0)],
    [(0, 0, 0), (0, 30, 0)],
    [(0, 30, 0), (30, 30, 0)],
    [(30, 0, 0), (30, 30, 0)]
]

# Plot each axis line as bold
for start, end in axis_lines:
    ax.plot(
        [start[0], end[0]],
        [start[1], end[1]],
        [start[2], end[2]],
        color='black', linestyle='-', linewidth=0.8
    )
"""
    
# Save figure
plt.savefig('od_bar_plot_colored.pdf')
