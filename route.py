import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt

# Load the CSV file
try:
    df = pd.read_csv('Hamburg.csv', header=None, usecols=[0, 1], skip_blank_lines=True)
except Exception as e:
    print(f"Error loading CSV file: {e}")
    raise

df = df.apply(pd.to_numeric, errors='coerce').dropna()

# Validate coordinates and select values
coordinates = df.values
if coordinates.shape[0] == 0:
    raise ValueError("No valid coordinates found in the CSV file.")
else:
    print("Valid coordinates found.")
    print(coordinates) 

# Define the size of the subset
subset_size = 100  # Example subset size; adjust as needed
if subset_size > coordinates.shape[0]:
    raise ValueError("Subset size exceeds the number of available coordinates.")

# Randomly select a subset of coordinates
np.random.seed(0)  # For reproducibility
subset_indices = np.random.choice(coordinates.shape[0], subset_size, replace=False)
subset_coordinates = coordinates[subset_indices]

# Calculate the distance matrix for the subset
dist_matrix = squareform(pdist(subset_coordinates, metric='euclidean'))
print("Distance matrix calculated for subset.")

# Solve the assignment problem (TSP) using linear_sum_assignment
row_ind, col_ind = linear_sum_assignment(dist_matrix)
route = np.argsort(col_ind)

# Print the route
for idx in route:
    print(subset_coordinates[idx])

print("Subset shape:", subset_coordinates.shape)
