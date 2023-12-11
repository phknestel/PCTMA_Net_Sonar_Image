import numpy as np
import h5py
from plyfile import PlyData, PlyElement

def save_point_cloud_as_ply(points, filename):
    structured_points = np.array([(point[0], point[1], point[2]) for point in points],
                                 dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    vertex = PlyElement.describe(structured_points, 'vertex')
    PlyData([vertex], text=True).write(filename)

# Replace with the path to your dataset
h5_file_path = 'gt1588.h5'

with h5py.File(h5_file_path, 'r') as file:
    # Assuming 'data' is the key for your point clouds
    point_cloud = file['point_cloud'][:]  # This is now treated as a single point cloud

# Specify the output PLY file path
ply_filename = './entire_point_cloud_gt.ply'

# Save the entire dataset as one PLY file
save_point_cloud_as_ply(point_cloud, ply_filename)
print(f"Saved point cloud to {ply_filename}")
