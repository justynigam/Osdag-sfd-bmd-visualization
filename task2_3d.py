import xarray as xr
import plotly.graph_objects as go
import numpy as np
from node import nodes
from element import members

# --- CONFIGURATION ---
SCALE_FACTOR = 0.5
girders = {
    'Girder 1': [13, 22, 31, 40, 49, 58, 67, 76, 81],
    'Girder 2': [14, 23, 32, 41, 50, 59, 68, 77, 82],
    'Girder 3': [15, 24, 33, 42, 51, 60, 69, 78, 83], # Centre girder
    'Girder 4': [16, 25, 34, 43, 52, 61, 70, 79, 84],
    'Girder 5': [17, 26, 35, 44, 53, 62, 71, 80, 85]
}

ds = xr.open_dataset('screening_task.nc')
fig = go.Figure()

# --- 1. DRAW BRIDGE FRAME  ---
edge_x, edge_y, edge_z = [], [], []
for start, end in members.values():
    x0, y0, z0 = nodes[start]
    x1, y1, z1 = nodes[end]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    edge_z.extend([z0, z1, None])

fig.add_trace(go.Scatter3d(
    x=edge_x, y=edge_y, z=edge_z,
    mode='lines',
    line=dict(color='lightgrey', width=2),
    name='Bridge Frame',
    hoverinfo='none'
))

# FUNCTION TO ADD TRACES 
#  FUNCTION TO ADD TRACES WITH SMART HOVER 
def create_girder_trace(girder_name, element_ids, component, color, is_visible):
    x_vals, y_vals, z_vals = [], [], []
    hover_texts = [] # List to store text for each point
    
    for elem_id in element_ids:
        start_id, end_id = members[elem_id]
        xs, ys, zs = nodes[start_id]
        xe, ye, ze = nodes[end_id]
        
        # Get Force Data
        val_i = ds.sel(Element=elem_id)['forces'].sel(Component=f'{component}_i').values
        val_j = ds.sel(Element=elem_id)['forces'].sel(Component=f'{component}_j').values
        
        # Draw "Curtain" path (5 points per element)
        x_vals.extend([xs, xs, xe, xe, None])
        y_vals.extend([0, val_i * SCALE_FACTOR, val_j * SCALE_FACTOR, 0, None])
        z_vals.extend([zs, zs, ze, ze, None])
        
        # Custom Hover Text for each point
        # We format the number to 2 decimal places
        unit = 'kN-m' if 'Mz' in component else 'kN'
        label_i = f"Elem {elem_id}<br>Val: {val_i:.2f} {unit}"
        label_j = f"Elem {elem_id}<br>Val: {val_j:.2f} {unit}"
        base_label = f"Elem {elem_id}<br>Base Node"
        
        hover_texts.extend([base_label, label_i, label_j, base_label, None])
        
    return go.Scatter3d(
        x=x_vals, y=y_vals, z=z_vals,
        mode='lines',
        line=dict(color=color, width=4),
        name=f'{girder_name} ({component})',
        visible=is_visible,
        text=hover_texts,      # Add the text list
        hoverinfo='text+name'  # Tell Plotly to use our text
    )

# 2. ADD BENDING MOMENT TRACES  
# These will be traces 1, 2, 3, 4, 5
for name, ids in girders.items():
    fig.add_trace(create_girder_trace(name, ids, 'Mz', 'blue', True))

# 3. ADD SHEAR FORCE TRACES (Initially Hidden) 
# These will be traces 6, 7, 8, 9, 10
for name, ids in girders.items():
    fig.add_trace(create_girder_trace(name, ids, 'Vy', 'red', False))
# Here i Provided option to see Bending moment and Shear force
# 4. CREATE DROPDOWN MENU
fig.update_layout(
    title="3D Bridge Forces (Interactive)",
    scene=dict(
        xaxis_title='Length (X)',
        yaxis_title='Force Magnitude (Y)',
        zaxis_title='Width (Z)',
        aspectmode='data'
    ),
    updatemenus=[dict(
        type="buttons",
        direction="left",
        x=0.05, y=1.0, # Position of buttons
        buttons=list([
            dict(
                label="Show Bending Moment (Mz)",
                method="update",
                args=[{"visible": [True, True, True, True, True, True, False, False, False, False, False]},
                      {"title": "3D Bending Moment Diagram (Mz)"}]
            ),
            dict(
                label="Show Shear Force (Vy)",
                method="update",
                args=[{"visible": [True, False, False, False, False, False, True, True, True, True, True]},
                      {"title": "3D Shear Force Diagram (Vy)"}]
            ),
        ]),
    )]
)
# Export the interactive model to HTML so that you can view in web browser later 
fig.write_html("3d_view/Interactive_Bridge_Model.html")
print("Successfully exported 3D model to 'Interactive_Bridge_Model.html'")

fig.show()