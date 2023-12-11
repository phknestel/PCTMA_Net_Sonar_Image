import numpy as np
import h5py
import os

def scale_point_cloud(point_cloud, scale_factor):
    return point_cloud * scale_factor

def process_file(file_path, scale_factor):
    with h5py.File(file_path, 'r+') as file:
        if 'point_cloud' in file:  # Adjust this key if needed
            point_cloud = file['point_cloud'][:]
            scaled_point_cloud = scale_point_cloud(point_cloud, scale_factor)
            del file['point_cloud']
            file.create_dataset('point_cloud', data=scaled_point_cloud)
            print(f"Reversed scaling for {file_path}")

def process_directory(root_dir, scale_factor):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.h5'):
                file_path = os.path.join(dirpath, filename)
                process_file(file_path, scale_factor)

# Scaling factor to reverse the previous scaling (initial scaling was 0.5, so reverse is 2)
reverse_scale_factor = 2

# Start from the current directory
current_directory = os.getcwd()
process_directory(current_directory, reverse_scale_factor)

