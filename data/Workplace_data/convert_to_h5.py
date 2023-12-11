import os
import numpy as np
import h5py

def convert_to_h5(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                data = np.loadtxt(file_path)  # Assuming the data is in a simple format that np.loadtxt can read

                # Create an output path for the HDF5 file
                relative_path = os.path.relpath(root, input_dir)
                h5_output_path = os.path.join(output_dir, relative_path)
                os.makedirs(h5_output_path, exist_ok=True)
                print("Creating directory:", h5_output_path)
                print("Processing file:", file_path)

                with h5py.File(os.path.join(h5_output_path, file.replace(".txt", ".h5")), 'w') as h5f:
                    h5f.create_dataset('point_cloud', data=data)

# Example usage
input_directory = "./"  # The root directory you provided
output_directory = "./"  # Output directory for HDF5 files
convert_to_h5(input_directory, output_directory)

