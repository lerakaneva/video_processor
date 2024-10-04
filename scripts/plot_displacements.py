import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np
import os

def calculate_displacements(df, track_id, pixel_size):
    """
    Calculate displacements for a given track ID.

    Parameters:
    - df: DataFrame containing trajectory data.
    - track_id: The specific track ID for which to calculate displacements.
    - pixel_size: Size of one pixel in micrometers.
    
    Returns:
    - DataFrame with columns ['frame_y', 'displacement_from_start', 'displacement_from_previous']
    """
    # Filter the DataFrame for the specific track_id and sort by time
    track_data = df[df['track_id'] == track_id].sort_values(by='frame_y')
    # Calculate displacements from the start and from the previous position
    start_x, start_y = track_data.iloc[0]['x'], track_data.iloc[0]['y']
    track_data['displacement_from_start'] = np.sqrt((track_data['x'] - start_x) ** 2 + (track_data['y'] - start_y) ** 2) * pixel_size
    track_data['displacement_from_previous'] = np.sqrt(track_data['x'].diff() ** 2 + track_data['y'].diff() ** 2).fillna(0) * pixel_size
    track_data['dx'] = track_data['x'].diff().fillna(0) * pixel_size
    track_data['dy'] = track_data['y'].diff().fillna(0) * pixel_size

    return track_data[['frame_y', 'displacement_from_start', 'displacement_from_previous', 'dx', 'dy']]

def plot_displacement_from_start(track_displacements, track_id, output_dir):
    """
    Plot and save the displacement from start over time for a given track ID.

    Parameters:
    - track_displacements: DataFrame containing displacements for the track ID.
    - track_id: The specific track ID.
    - output_dir: Directory to save the plot.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(track_displacements['frame_y'], track_displacements['displacement_from_start'], label='Displacement from Start', marker='o')
    plt.xlabel('Time (frames)')
    plt.ylabel('Displacement from Start (µm)')
    plt.title(f'Displacement from Start for Track ID: {track_id}')
    plt.grid(True)

    # Save plot to output directory
    output_path = f"{output_dir}/displacement_from_start_track_{track_id}.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Saved displacement from start plot to {output_path}")

def plot_displacement_from_previous(track_displacements, track_id, output_dir):
    """
    Plot and save the displacement from the previous position over time for a given track ID.

    Parameters:
    - track_displacements: DataFrame containing displacements for the track ID.
    - track_id: The specific track ID.
    - output_dir: Directory to save the plot.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(track_displacements['frame_y'], track_displacements['displacement_from_previous'], label='Displacement from Previous', marker='x')
    plt.xlabel('Time (frames)')
    plt.ylabel('Displacement from Previous (µm)')
    plt.title(f'Displacement from Previous Position for Track ID: {track_id}')
    plt.grid(True)

    # Save plot to output directory
    output_path = f"{output_dir}/displacement_from_previous_track_{track_id}.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Saved displacement from previous position plot to {output_path}")

    # Plot dx over time
    plt.figure(figsize=(10, 5))
    plt.plot(track_displacements['frame_y'], track_displacements['dx'], label='dx', marker='o', color='blue')
    plt.xlabel('Time (frames)')
    plt.ylabel('dx (um)')
    plt.title(f'dx over Time for Track ID: {track_id}')
    plt.grid(True)

    # Save plot for dx
    output_path_dx = os.path.join(output_dir, f"dx_track_{track_id}.png")
    plt.savefig(output_path_dx)
    plt.close()
    print(f"Saved dx plot to {output_path_dx}")

    # Plot dy over time
    plt.figure(figsize=(10, 5))
    plt.plot(track_displacements['frame_y'], track_displacements['dy'], label='dy', marker='o', color='red')
    plt.xlabel('Time (frames)')
    plt.ylabel('dy (um)')
    plt.title(f'dy over Time for Track ID: {track_id}')
    plt.grid(True)

    # Save plot for dy
    output_path_dy = os.path.join(output_dir, f"dy_track_{track_id}.png")
    plt.savefig(output_path_dy)
    plt.close()
    print(f"Saved dy plot to {output_path_dy}")

def plot_displacements(df, track_ids, pixel_size, output_dir):
    """
    Build and save plots for displacement from start and from previous position over time.
    
    Parameters:
    - df: DataFrame containing trajectory data.
    - track_ids: List of track IDs for which to plot displacements.
    - pixel_size: Size of one pixel in micrometers.
    - output_dir: Directory to save plots.
    """
    for track_id in track_ids:
        print(f"Processing track_id: {track_id}")
        
        # Calculate displacements for the given track_id
        track_displacements = calculate_displacements(df, track_id, pixel_size)
        
        # Plot displacement from start
        plot_displacement_from_start(track_displacements, track_id, output_dir)
        
        # Plot displacement from previous position
        plot_displacement_from_previous(track_displacements, track_id, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot displacement of trajectories from CSV data.")
    parser.add_argument("--csv_path", help="Path to the input CSV file containing trajectory data.")
    parser.add_argument("--track_ids", nargs='+', required=True, help="List of track IDs for which to make plots.")
    parser.add_argument("--pixel_size", type=float, required=True, help="Pixel size in micrometers.")
    parser.add_argument("--output_dir", required=True, help="Directory to save plots.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    df = pd.read_csv(args.csv_path)

    required_columns = {'track_id', 'x', 'y', 'frame_y'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"The input CSV must contain the following columns: {required_columns}")

    track_ids = [int(tid) for tid in args.track_ids]

    # Plot and save displacements
    plot_displacements(df, track_ids, args.pixel_size, args.output_dir)
