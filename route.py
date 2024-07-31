import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt

# we should first load csv 
try:
    df = pd.read_csv('Hamburg.csv', header=None, usecols=[0, 1], skip_blank_lines=True)
except Exception as e:
    print(f"Error loading CSV file: {e}")
    raise

df = df.apply(pd.to_numeric, errors='coerce').dropna()

# then check if coordinates are valid
coordinates = df.values
if coordinates.shape[0] == 0:
    raise ValueError("No valid coordinates found in the CSV file.")
else:
    print("Valid coordinates found.")
    print(coordinates) 

#for example here I am selecting 100 randomly
subset_size = 100  
if subset_size > coordinates.shape[0]:
    raise ValueError("Subset size exceeds the number of available coordinates.")


np.random.seed(0) 
subset_indices = np.random.choice(coordinates.shape[0], subset_size, replace=False)
subset_coordinates = coordinates[subset_indices]

# Calculate the distance matrix for 
dist_matrix = squareform(pdist(subset_coordinates, metric='euclidean'))
print("Distance matrix calculated for subset.")

# Solve the assignment problem (TSP) using linear_sum_assignment
row_ind, col_ind = linear_sum_assignment(dist_matrix)
route = np.argsort(col_ind)


for idx in route:
    print(subset_coordinates[idx])

print("Subset shape:", subset_coordinates.shape)
