def extract_cex_from_file(file_name):
# Open the file for reading
    with open(file_name, 'r') as file:
        # Initialize an empty list to store the values
        x_values = []

        # Iterate through each line in the file
        for line in file:
            # Split each line into key and value
            line = line.replace('(', '').replace(')', '')
            parts = line.strip().split()
            if len(parts) == 2:
                key, value = parts[0], parts[1]
                # Check if the key starts with 'X_' to identify X values
                if key.startswith('X_'):
                    # Remove any trailing ')' from the value and then convert it to a float
                    value = float(value.rstrip(')'))
                    x_values.append(value)
    # Print the list of X values
    return x_values

if __name__ == "__main__":
    cex = extract_cex_from_file('cex.txt')
    print(cex)

