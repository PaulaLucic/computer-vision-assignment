from pathlib import Path
import numpy as np

traj_path = Path("input") / "traj.txt"

data = np.loadtxt(traj_path)

matrices = data.reshape(3, 4, 4)

print("Shape:", matrices.shape)
print(matrices)

positions = matrices[:, :3, 3]

print("Camera positions:")
print(positions)



print("\nFirst 5 points from image1.ply:")

file_path = "input/image1.ply"

with open(file_path, "r") as f:
    for line in f:
        if line.strip() == "end_header":
            break
    
    all_points = []

    for i in range(5):
        line = f.readline()

        parts = line.split()

        coords = [float(value) for value in parts[:3]]
        colors = [int(value) for value in parts[3:]]

        all_points.append(coords)

    points = np.array(all_points)

    print("Original points:")
    print(points)

    transformed_points = points[:, [2, 1, 0]]

    print("Transformed points:")
    print(transformed_points)