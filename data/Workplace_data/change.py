import h5py

# Path to your HDF5 file
hdf5_file_path = 'ffd13ca14b85fec66cf1b4a8fc3914e.h5'

# Open the HDF5 file
with h5py.File(hdf5_file_path, 'a') as f:
    # Check if the dataset 'point_cloud' exists and 'data' does not exist
    if 'point_cloud' in f and 'data' not in f:
        # Rename 'point_cloud' to 'data'
        f['data'] = f['point_cloud']
        del f['point_cloud']
