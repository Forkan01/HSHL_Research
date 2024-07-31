import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt
#we first need to load csv 
try:
    df = pd.read_csv('/home/ageda/mehdi/PHI/Abdullah/RouteVehicle1_Seeveta-Hamburg.csv', header=None, usecols=[0, 1], skip_blank_lines=True)
except Exception as e:
    print(f"Error loading CSV file: {e}")
    raise
df = df.apply(pd.to_numeric, errors='coerce').dropna()
#then validate coordinates and select value
coordinates = df.values
if coordinates.shape[0] == 0:
    raise ValueError("No valid coordinates found in the CSV file.")
else:
    print("Valid coordinates found.")
    print(coordinates) 

# squareform distance to vector for compare  it will give us matrix 
dist_matrix = squareform(pdist(coordinates, metric='euclidean'))
print("Distance matrix calculated.")


#linear_sum_assignment calucalte TSP problem for fidning best route 
row_ind, col_ind = linear_sum_assignment(dist_matrix)
route = np.argsort(col_ind)
for idx in route:
    print(coordinates[idx])
