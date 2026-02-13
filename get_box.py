import sys

def get_center(pdb_file):
    x_coords = []
    y_coords = []
    z_coords = []

    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                # PDB format: X is col 30-38, Y is 38-46, Z is 46-54
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                x_coords.append(x)
                y_coords.append(y)
                z_coords.append(z)

    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    center_z = sum(z_coords) / len(z_coords)

    print(f"center_x = {center_x:.3f}")
    print(f"center_y = {center_y:.3f}")
    print(f"center_z = {center_z:.3f}")

if __name__ == "__main__":
    get_center(sys.argv[1])
