from pathlib import Path
import numpy as np

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

def load_traj(file_path):

    data = np.loadtxt(file_path)

    matrices = data.reshape(3, 4, 4)

    return matrices

matrices = load_traj(INPUT_DIR / "traj.txt")
positions = matrices[:, :3, 3]

print("Camera positions:")
print(positions)


def load_ply(file_path):
    print("Loading file:", file_path)

    with open(file_path, "r") as f:
        for line in f:
            if line.strip() == "end_header":
                break

        all_points = []
        all_colors = []

        for line in f:
            parts = line.split()

            coords = [float(value) for value in parts[:3]]
            colors = [int(value) for value in parts[3:]]

            all_points.append(coords)
            all_colors.append(colors)

    points = np.array(all_points)
    colors = np.array(all_colors)

    return points, colors


points, colors = load_ply(INPUT_DIR / "image1.ply")

print("Points shape:", points.shape)
print("Colors shape:", colors.shape)
print("First 5 points:")
print(points[:5])
print("First 5 colors:")
print(colors[:5])
