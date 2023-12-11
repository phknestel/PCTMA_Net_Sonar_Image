import h5py

# Replace with the path to one of your actual HDF5 files
file_path = 'test1588.h5'

with h5py.File(file_path, 'r') as f:
    print("Datasets in the HDF5 file:")
    for key in f.keys():
        print(key)
        print("Shape (resolution) of the dataset:", f[key].shape)
