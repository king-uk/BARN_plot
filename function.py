import numpy as np
import matplotlib.pyplot as plt

import csv
import math

def load_map(file_path):
    grid = np.loadtxt(file_path, dtype=float)
    return grid

def show_traj(grid_map, visual_traj=None, res=0.1, obstacle_value=10, clear=True, ij_as_xy=True):
    grid = np.asarray(grid_map)
    H, W = grid.shape

    if clear:
        plt.clf()

    hl = res * 0.5

    if ij_as_xy:
        for i in range(H):
            for j in range(W):
                if grid[i, j] == obstacle_value:
                    mx = i * res
                    my = j * res
                    oX = [mx - hl, mx + hl, mx + hl, mx - hl, mx - hl]
                    oY = [my - hl, my - hl, my + hl, my + hl, my - hl]
                    plt.plot(oX, oY, "k-")
    else:
        for i in range(H):
            for j in range(W):
                if grid[i, j] == obstacle_value:
                    mx = j * res
                    my = i * res
                    oX = [mx - hl, mx + hl, mx + hl, mx - hl, mx - hl]
                    oY = [my - hl, my - hl, my + hl, my + hl, my - hl]
                    plt.plot(oX, oY, "k-")

    if visual_traj is not None and len(visual_traj) > 0:
        xs = [p[0] for p in visual_traj]
        ys = [p[1] for p in visual_traj]
        plt.plot(xs, ys, color="blue", linewidth=1.0)

    ymax = W * res if not ij_as_xy else W * res
    xmax = H * res if not ij_as_xy else H * res
    plt.xlim(0.0, xmax)
    plt.ylim(0.0, ymax)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.grid(True)

    plt.show()
    
def get_path(path, cols=(2, 3), has_header='auto'):
    c1, c2 = cols
    visual_traj = []

    with open(path, newline='') as f:
        sample = f.read(4096)
        f.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample)
        except Exception:
            dialect = csv.excel

        reader = csv.reader(f, dialect)

        if has_header == 'auto':
            try:
                _has_header = csv.Sniffer().has_header(sample)
            except Exception:
                _has_header = False
        else:
            _has_header = bool(has_header)

        if _has_header:
            next(reader, None)

        for row in reader:
            if not row:
                continue
            if len(row) < max(c1, c2):
                continue
            try:
                x = float(row[c1 - 1].strip())
                y = float(row[c2 - 1].strip())
            except ValueError:
                continue
            if not (math.isfinite(x) and math.isfinite(y)):
                continue
            visual_traj.append([x, y])
    return visual_traj
