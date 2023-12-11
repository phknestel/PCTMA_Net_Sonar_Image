import numpy as np
import h5py
import os

def center_point_cloud(point_cloud):
    centroid = np.mean(point_cloud, axis=0)
    return point_cloud - centroid

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".h5"):
            h5_file_path = os.path.join(directory, filename)

            with h5py.File(h5_file_path, 'r+') as file:
                if 'point_cloud' in file:  # Change 'data' to your dataset key if different
                    point_cloud = file['point_cloud'][:]
                    centered_point_cloud = center_point_cloud(point_cloud)

                    # Replace the old dataset with the centered one
                    del file['point_cloud']
                    file.create_dataset('point_cloud', data=centered_point_cloud)
                    print(f"Processed {filename}")

# Replace with your directory path
your_directory = './'
process_directory(your_directory)

