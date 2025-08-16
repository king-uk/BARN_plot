import function as plot


if __name__ == "__main__":
    # Example usage
    map = 269

    grid_map = plot.load_map("BARN_dataset/txt_files/output_"+str(map)+".txt")
    visual_traj = plot.get_path("path_csv/plan_fromXis0.5.csv", cols=(2, 3), has_header=True)
    plot.show_traj(grid_map, visual_traj)