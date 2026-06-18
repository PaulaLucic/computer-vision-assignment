from pathlib import Path
import numpy as np

# path to folder
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

# load, reshape
def load_traj(file_path):

    data = np.loadtxt(file_path)

    matrices = data.reshape(3, 4, 4)

    return matrices

# call function
matrices = load_traj(INPUT_DIR / "traj.txt")
positions = matrices[:, :3, 3]

# check
print("Camera positions:")
print(positions)

# load points (as float) and colors, without header
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

# call function
points, colors = load_ply(INPUT_DIR / "image1.ply")

# check
print("Points shape:", points.shape)
print("Colors shape:", colors.shape)
print("First 5 points:")
print(points[:5])
print("First 5 colors:")
print(colors[:5])


# transforms points according to given permutation and signs
def transform_points(points, permutation, signs):
    transformed_points = points[:, permutation]
    transformed_points = transformed_points * signs
    return transformed_points


#converts permutation + signs to one 3 x 3 matrix
def build_axis_transform(permutation, signs):
    axis_transform = np.zeros((3, 3))

    for new_axis, old_axis in enumerate(permutation):
        axis_transform[new_axis, old_axis] = signs[new_axis]

    return axis_transform


# transforms cameras position and rotation according to given permutation and signs
def transform_poses(poses, permutation, signs):
    axis_transform = build_axis_transform(permutation, signs)

    transformed_poses = poses.copy()

    for i in range(len(poses)):
        transformed_poses[i, :3, :3] = (
            axis_transform @ poses[i, :3, :3] @ axis_transform.T
        ) # transform camera rotation

        transformed_poses[i, :3, 3] = (
            axis_transform @ poses[i, :3, 3]
        ) # transform camera position

    return transformed_poses

# creates new file with transformed camera poses
def save_traj(file_path, poses):
    flat_poses = poses.reshape(3, 16)
    np.savetxt(file_path, flat_poses)

# creates new file with transformed points
def save_ply(input_file_path, output_file_path, points, colors):

    header = []

    with open(input_file_path, "r") as f:
        for line in f:
            header.append(line)

            if line.strip() == "end_header":
                break

    with open(output_file_path, "w") as f:
        f.writelines(header)

        for i in range(len(points)):
            x, y, z = points[i]
            r, g, b = colors[i]

            f.write(f"{x} {y} {z} {r} {g} {b}\n")


# call function
permutation = [2, 1, 0]
signs = [1, 1, -1]

transformed_points = transform_points(points, permutation, signs)
transformed_matrices = transform_poses(matrices, permutation, signs)
save_traj(OUTPUT_DIR / "traj.txt", transformed_matrices)
save_ply(
    INPUT_DIR / "image1.ply",
    OUTPUT_DIR / "image1.ply",
    transformed_points,
    colors
)
