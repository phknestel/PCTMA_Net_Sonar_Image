import numpy as np
import h5py
import os

def normalize_point_cloud(point_cloud, target_min, target_max):
    pc_min = np.min(point_cloud, axis=0)
    pc_max = np.max(point_cloud, axis=0)
    scale_factor = (target_max - target_min) / (pc_max - pc_min)
    normalized_pc = (point_cloud - pc_min) * scale_factor + target_min
    return normalized_pc

def process_file(file_path, target_min, target_max):
    with h5py.File(file_path, 'r+') as file:
        if 'point_cloud' in file:  # Adjust this key if needed
            point_cloud = file['point_cloud'][:]
            normalized_point_cloud = normalize_point_cloud(point_cloud, target_min, target_max)
            del file['point_cloud']
            file.create_dataset('point_cloud', data=normalized_point_cloud)
            print(f"Normalized {file_path}")

def process_directory(root_dir, target_min, target_max):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.h5'):
                file_path = os.path.join(dirpath, filename)
                process_file(file_path, target_min, target_max)

# Define target bounding box range
target_min = np.array([-0.27, -0.23, -0.25])  # Adjust as necessary
target_max = np.array([0.27, 0.23, 0.25])     # Adjust as necessary

# Start from the current directory or a specified directory
current_directory = os.getcwd()  # or replace with 'path_to_your_directory'
process_directory(current_directory, target_min, target_max)
