import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import os

# Create output directory if it doesn't exist
os.makedirs('2d_images', exist_ok=True)

# STEP 1: LOAD THE DATA 
ds = xr.open_dataset('screening_task.nc') 

# STEP 2: DEFINE VARIABLES 
central_girder_ids = [15, 24, 33, 42, 51, 60, 69, 78, 83]
plot_data_Mz = {'x': [], 'y': []}
plot_data_Vy = {'x': [], 'y': []}

current_distance = 0.0
element_length = 25.0 / 9.0 

# STEP 3: PROCESS THE DATA 
for elem_id in central_girder_ids:
    element_data = ds.sel(Element=elem_id) 
    
    # Bending Moment (Mz) 
    mz_i = element_data['forces'].sel(Component='Mz_i').values
    mz_j = element_data['forces'].sel(Component='Mz_j').values
    
    plot_data_Mz['x'].append(current_distance)
    plot_data_Mz['y'].append(mz_i)
    plot_data_Mz['x'].append(current_distance + element_length)
    plot_data_Mz['y'].append(mz_j)
    
    # Shear Force (Vy) 
    vy_i = element_data['forces'].sel(Component='Vy_i').values
    vy_j = element_data['forces'].sel(Component='Vy_j').values
    
    plot_data_Vy['x'].append(current_distance)
    plot_data_Vy['y'].append(vy_i)
    plot_data_Vy['x'].append(current_distance + element_length)
    plot_data_Vy['y'].append(vy_j)
    
    current_distance += element_length

# STEP 4: Generate the Plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Plot 1: Bending Moment
ax1.plot(plot_data_Mz['x'], plot_data_Mz['y'], label='Bending Moment (Mz)', color='blue')
ax1.fill_between(plot_data_Mz['x'], plot_data_Mz['y'], alpha=0.3, color='blue')
ax1.set_title('Bending Moment Diagram (Central Girder)')
ax1.set_xlabel('Bridge Length (m)')
ax1.set_ylabel('Moment (kN-m)')
ax1.grid(True)
ax1.legend()

# Plot 2: Shear Force
ax2.plot(plot_data_Vy['x'], plot_data_Vy['y'], label='Shear Force (Vy)', color='red')
ax2.fill_between(plot_data_Vy['x'], plot_data_Vy['y'], alpha=0.3, color='red')
ax2.set_title('Shear Force Diagram (Central Girder)')
ax2.set_xlabel('Bridge Length (m)')
ax2.set_ylabel('Shear Force (kN)')
ax2.grid(True)
ax2.legend()

# Save the figure as a high-quality PNG file
plt.savefig('2d_images/Task1_2D_Results.png', dpi=300)

plt.tight_layout()
plt.show()