# Osdag Screening Task - SFD & BMD Visualization

## 📋 Project Overview

This project implements **Shear Force Diagrams (SFD)** and **Bending Moment Diagrams (BMD)** for a bridge grillage model using data from an Xarray dataset. The project is part of the Osdag FOSSEE screening assignment.

## 🎯 Tasks Completed

### Task-1: 2D SFD & BMD for Central Girder
- Creates 2D plots for the **central longitudinal girder** (elements: `[15, 24, 33, 42, 51, 60, 69, 78, 83]`)
- Extracts `Mz` (Bending Moment) and `Vy` (Shear Force) from Xarray dataset
- Uses Matplotlib for visually clear diagrams with proper labels, titles, and legends

### Task-2: 3D SFD & BMD for All Girders
- Creates interactive 3D visualization for **all 5 girders** using Plotly
- MIDAS-style "curtain" extrusion effect showing force magnitudes
- Interactive buttons to toggle between Bending Moment (Mz) and Shear Force (Vy)
- Proper scaling, axes labels, and color coding (Blue = Mz, Red = Vy)

## 📁 Project Structure

```
Osdag project/
├── task1_2d.py          # Task 1: 2D SFD & BMD plotting script
├── task2_3d.py          # Task 2: 3D interactive visualization
├── screening_task.nc    # Xarray dataset with force values
├── node.py              # Node coordinates [x, y, z]
├── element.py           # Element connectivity [start_node, end_node]
├── 2d_images/
│   └── Task1_2D_Results.png   # Generated 2D plots
├── 3d_view/
│   └── Interactive_Bridge_Model.html  # Interactive 3D visualization
└── README.md            # This file
```

## 🚀 How to Run

### Prerequisites
```bash
pip install xarray netcdf4 matplotlib plotly numpy
```

### Run Task 1 (2D Plots)
```bash
python task1_2d.py
```
**Output:** `2d_images/Task1_2D_Results.png`

### Run Task 2 (3D Visualization)
```bash
python task2_3d.py
```
**Output:** `3d_view/Interactive_Bridge_Model.html` (open in browser)

## 📊 Girder Element Mapping

| Girder | Element IDs |
|--------|-------------|
| Girder 1 | [13, 22, 31, 40, 49, 58, 67, 76, 81] |
| Girder 2 | [14, 23, 32, 41, 50, 59, 68, 77, 82] |
| Girder 3 (Central) | [15, 24, 33, 42, 51, 60, 69, 78, 83] |
| Girder 4 | [16, 25, 34, 43, 52, 61, 70, 79, 84] |
| Girder 5 | [17, 26, 35, 44, 53, 62, 71, 80, 85] |

## 🔧 Technical Details

- **Xarray Dataset:** `screening_task.nc` contains force components (`Mz_i`, `Mz_j`, `Vy_i`, `Vy_j`)
- **Sign Convention:** Values used as stored in dataset (no manual flipping)
- **Coordinate System:** X = Bridge Length, Y = Force Magnitude, Z = Bridge Width

## 📝 License

Licensed under Creative Commons Attribution-ShareAlike 4.0 International License by FOSSEE.

## 👤 Author

[Your Name]

---
*Osdag FOSSEE Screening Task Submission*
