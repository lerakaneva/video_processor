# Visualize trajectories and masks

This project helps visualize trajectories and masks on microscopy videos for easier visual analysis. It supports drawing cell labels, trajectories, timestamp, and scale bar, and can output processed frames as TIFF and AVI files.

## Requirements

The following Python packages are required to run the project:

- `numpy`: For numerical operations.
- `opencv-python`: For image processing and drawing trajectories.
- `tifffile`: For reading and writing TIFF image files.
- `pandas`: For handling CSV data (trajectories).
You can install these dependencies by running:

```bash
pip install -r requirements.txt
```

## Running Tests

Run tests from the project root:

```bash
python -m unittest discover tests
```

## How to Run

1. **Prepare the Configuration**:
   - Create a configuration file (e.g., `config.json`) that defines paths, colors, and processing parameters. You can use the following as a template:

   ```json
  {
    "originals_path": "/path/to/video.tif",
    "segmentation_masks_path": "/path/to/mask.tif",
    "output_dir": "path/to/output/directory",
    "output_fps": 20,
    "save_as_tiff": true,
    "cell_trajectories": { 
      "file": "trajectories.csv",
      "color": [15, 32, 128]
    },
    "csv_folder_cell_labels": "folder/with/csv/labels",
    "cell_labels": [
      {
        "name": "moving",
        "file": "labels_moving.csv",
        "color": [255, 0, 0]
      },
      {
        "name": "filtered",
        "file": "labels_filtered.csv",
        "color": [0, 0, 0]
      },
      {
        "name": "stationary",
        "file": "labels_stationary.csv",
        "color": [0, 0, 0]
      }
    ],
    "track_id_color": [255, 255, 0],
    "mask_colors": {
      "1": [0, 255, 0],
      "2": [255, 0, 255]
    },
    "alpha": 0.3,
    "chunk_size": 2000,
    "output_frequency": 1000,
    "metadata": {
      "pixel_size": 0.431,
      "time_between_frames": 0.05,
      "color": [255, 255, 0]
    }
  }

    ```
2. **Run**:
```bash
python main.py --config /path/to/config.json
```

## Configuration Parameters

The `config.json` file contains various settings to control how the video is processed. Below is a description of each parameter:

- **`originals_path`** (`str`): Path to the microscopy video in `.tif` format.
- **`segmentation_masks_path`** (`str`): Path to the segmentation mask file (`.tif`) corresponding to the microscopy video. Each pixel in this mask represents a segmentation class.
- **`output_dir`** (`str`): The directory where processed video frames will be saved.
- **`output_fps`** (`int`): Frames per second for the output AVI video. Default is 7.
- **`save_as_tiff`** (`bool`): Whether to save processed frames as TIFF stack. Default is `false`.
- **`cell_trajectories`** (`dict`): Defines trajectory visualization:
    - **`file`** (`str`): Path to the CSV file containing trajectory data (`x`, `y`, `frame_y` columns).
    - **`color`** (`list` of `int`): RGB color for the trajectories.
- **`csv_folder_cell_labels`** (`str`):  The directory containing the CSV files for cell labels.
- **`cell_labels`** (`list` of `dict`): List of cell label definitions. Each dictionary contains:
    - **`name`** (`str`): Name of the cell label group (e.g., "moving", "stationary").
    - **`file`** (`str`): Filename of the CSV containing cell label data (`x`, `y`, `frame_y` and `track_id` columns).  For each entry in this CSV, a circle of the specified color will be drawn at the (x, y) coordinates on the corresponding frame. This allows you to label and color-code different groups of cells or objects in your video. If the `track_id_color` is provided in the configuration, the `track_id` will also be drawn next to the circle, enabling visualization of cell tracks for this group.
    - **`color`** (`list` of `int`): RGB color for the cell labels.
- **`track_id_color`** (`list` of `int`): RGB color for displaying track IDs next to cell labels. If `None`, track IDs will not be displayed.  This allows for the visualization of cell lineages or tracking of individual cells across frames.
- **`mask_colors`** (`dict`): Maps mask class IDs (integers) to RGB colors (list of integers).  For example: `{"1": [255, 0, 0], "2": [0, 255, 0]}` would color mask pixels with ID 1 as red and ID 2 as green.
- **`alpha`** (`float`): Transparency of the segmentation mask overlay (0.0-1.0).  0.0 is fully transparent, 1.0 is fully opaque.  Default is 0.3.
- **`chunk_size`** (`int`): Number of frames to process in each batch. Useful for managing memory usage for very large videos. Default is 1000.
- **`output_frequency`** (`int`): How often (in frames) to print progress updates to the console. Default is 100.
- **`metadata`** (`dict`):  Configuration for the display of metadata on the frames.  Contains the following:
    - **`pixel_size`** (`float`): Pixel size in micrometers.  This value is used to draw a correctly scaled scale bar on the video.
    - **`time_between_frames`** (`float`): Time interval between frames in seconds.  Used to calculate and display the timestamp on each frame.
    - **`color`** (`list` of `int`):  RGB color for the timestamp and scalebar text.
