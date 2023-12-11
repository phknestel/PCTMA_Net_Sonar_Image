import numpy as np
import h5py
import os

def scale_point_cloud(point_cloud, scale_factor):
    # Scale the point cloud by the given factor
    return point_cloud * scale_factor

def process_directory(directory, scale_factor):
    for filename in os.listdir(directory):
        if filename.endswith(".h5"):
            h5_file_path = os.path.join(directory, filename)

            with h5py.File(h5_file_path, 'r+') as file:
                if 'point_cloud' in file:  # Adjust this key if needed
                    point_cloud = file['point_cloud'][:]
                    
                    # Scale the point cloud
                    scaled_point_cloud = scale_point_cloud(point_cloud, scale_factor)

                    # Replace the old dataset with the scaled one
                    del file['point_cloud']
                    file.create_dataset('point_cloud', data=scaled_point_cloud)
                    print(f"Scaled {filename}")

# Replace with your directory path
your_directory = './'

# Scaling factor to reduce the range by half
scale_factor = 0.5

process_directory(your_directory, scale_factor)
