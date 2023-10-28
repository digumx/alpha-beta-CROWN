import os
import re
import pandas as pd

# Define a regular expression pattern to match property lines

# Create lists to store data
network_names = []
property_texts = []
property_statuses = []
times = []

# Specify the directory containing the files
directory = '/home/testing/alpha-beta-CROWN'  # Replace with the directory containing your files

# List all files in the directory
file_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.vnnlib')]

# Process each file
for file_path in file_paths:
    # Initialize variables to store data for each file
    network_name = None
    property_text = None
    property_status = None
    time = None
    
    # Read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Match the property line and extract property text
            if line.startswith('vnnlib_path:'):
                property_text = line.split(': ')[1]
            # Check for property status (sat, unsat, timeout)
            if line.startswith('Result:'):
                property_status = line.split(': ')[1]

     
            if line.startswith('Time:'):
                time = line.split(': ')[1]

            # Extract network name
            if line.startswith('onnx_path:'):
                network_name = line.split(': ')[1]


    # Append data to lists
    network_names.append(network_name)
    property_texts.append(property_text)
    property_statuses.append(property_status)
    times.append(time)
# Create a DataFrame
data = {
    'Network Name': network_names,
    'Property': property_texts,
    'Property Status': property_statuses,
    'Time': times
}
df = pd.DataFrame(data)

# Define the output Excel file path
output_excel_file = 'output.xlsx'

# Write the data to an Excel file
df.to_excel(output_excel_file, index=False)

print(times)
print(f"Data has been written to {output_excel_file}")
