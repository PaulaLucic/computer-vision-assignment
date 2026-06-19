# Delta Reality Computer Vision Assignment

## Goal

The goal of this assignment was to convert the provided local-space point clouds and world-space camera poses into a coordinate system compatible with the provided Unity viewer.

The input data consists of:

* `image1.ply`, `image2.ply`, `image3.ply` — local-space point clouds generated from monocular images
* `traj.txt` — world-space camera poses for the corresponding images

The main challenge was that the data-producing system and the viewer application use different coordinate systems.

## Approach

I implemented a Python transformation pipeline that:

1. loads camera pose matrices from `traj.txt`
2. loads point coordinates and RGB colors from ASCII `.ply` files
3. applies a configurable coordinate system transformation using axis permutations and sign flips
4. transforms both point cloud coordinates and camera poses consistently
5. writes transformed `.ply` files and a transformed `traj.txt` file to the `output/` directory

The transformation is parameterized using:

```python
permutation = [2, 1, 0]
signs = [1, 1, -1]
```

which corresponds to:

```text
[x, y, z] -> [z, y, -x]
```

This setup allows different coordinate-system hypotheses to be tested without rewriting the transformation logic.

## Camera Pose Transformation

The `traj.txt` file contains 4x4 camera pose matrices. Each matrix consists of:

* a 3x3 rotation matrix
* a 3D translation vector
* a homogeneous last row `[0, 0, 0, 1]`

For a coordinate transformation matrix `A`, camera poses are transformed as:

```text
R' = A R A^T
t' = A t
```

This applies the same coordinate system conversion to both the point clouds and the camera poses.

## Validation

The transformed files were tested in the provided Unity viewer.

During testing, I explored multiple coordinate-system hypotheses, including:

* axis permutations
* sign flips
* Unity / computer-vision coordinate convention differences
* alternative pose interpretations

Development was done on macOS, while the provided viewer was a Windows Unity build. Because of this, visual validation required transferring generated files to a separate Windows machine, which limited the number of test iterations.

The submitted implementation represents the final transformation pipeline developed through iterative hypothesis testing and visual validation using the provided viewer.

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the script:

```bash
python transform.py
```

The transformed files will be written to:

```text
output/
```

Expected output files:

```text
output/image1.ply
output/image2.ply
output/image3.ply
output/traj.txt
```

## Project Structure

```text
.
├── input/
│   ├── image1.ply
│   ├── image2.ply
│   ├── image3.ply
│   └── traj.txt
├── output/
├── transform.py
├── requirements.txt
└── README.md
```

## Notes

Large input and output files may be excluded from the GitHub repository depending on file size limits. The script expects the original input files to be placed in the `input/` directory.
