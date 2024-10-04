# Visualize trajectories and masks

The projects helps to visualize trajectories trajectories and masks for easier analysis.

## Requirements

The following Python packages are required to run the project:

- `numpy`: For numerical operations.
- `opencv-python`: For image processing and drawing trajectories.
- `tifffile`: For reading and writing TIFF image files.
- `pandas`: For handling CSV data (trajectories).
- `matplotlib`: For plotting coordinates and displacements using script
You can install these dependencies by running:

```bash
pip install -r requirements.txt
```

## Running Tests

The project uses `unittest` for testing. To run all tests, execute the following command from the root of the project:

```bash
python -m unittest discover -s tests
```

## How to Run

1. **Prepare the Configuration**:
   - Create a configuration file (e.g., `config.json`) that defines paths, colors, and processing parameters. You can use the following as a template:

   ```json
   {
     "microscopy_video_path": "/path/to/video.tif",
     "segmentation_mask_path": "/path/to/mask.tif",
     "output_dir": "/path/to/output",
     "csv_folder": "/path/to/csvs",
     "trajectories": [
       {
         "name": "rolling",
         "file": "rolling.csv",
         "color": [255, 165, 0]
       },
       {
         "name": "motionless",
         "file": "motionless.csv",
         "color": [0, 128, 255]
       }
     ],
     "mask_colors": {
       "1": [255, 0, 127],
       "2": [0, 128, 0]
     },
     "text_color": [225, 225, 0],
     "alpha": 0.3,
     "chunk_size": 1000,
     "output_frequency": 100
   }
    ```
2. **Run the processor**:
```bash
python main.py --config /path/to/config.json
```

## Configuration Parameters

The `config.json` file contains various settings to control how the video is processed. Below is a description of each parameter:

- **`microscopy_video_path`** (`str`): 
  - The file path to the input microscopy video (in `.tif` format).
  
- **`segmentation_mask_path`** (`str`): 
  - The file path to the segmentation mask file (in `.tif` format) corresponding to the microscopy video. Each pixel in this mask file represents a segmentation class.

- **`output_dir`** (`str`): 
  - The directory where the processed video frames will be saved. Two subdirectories, `with_masks` and `without_masks`, will be created for saving frames with and without segmentation masks, respectively.

- **`csv_folder`** (`str`): 
  - The directory containing the trajectory CSV files. The CSV file should contain `x`, `y`, and `frame_y` columns representing the position and frame number.

- **`trajectories`** (`list` of `dict`): 
  - A list of trajectory definitions. Each trajectory is a dictionary with the following fields:
    - **`name`** (`str`): Name of the trajectory type (e.g., "rolling", "motionless").
    - **`file`** (`str`): The filename of the CSV file containing trajectory data (e.g., "rolling.csv"). The CSV file should contain `x`, `y`, and `frame_y` columns representing the position and frame number.
    - **`color`** (`list` of `int`): RGB color values for displaying the trajectory on the video frames (e.g., `[255, 165, 0]` for orange).


- **`mask_colors`** (`dict` of `list` of `int`): 
  - A dictionary mapping segmentation class IDs to RGB color values for displaying the segmentation mask on the video frames. Example:
  
    ```json
    {
      "1": [255, 0, 127],
      "2": [0, 128, 0]
    }
    ```

    In this example, class `1` will be displayed as pink and class `2` as green.

- **`alpha`** (`float`): 
  - The transparency level for blending the segmentation mask with the original video. A value between `0.0` (completely transparent) and `1.0` (completely opaque). Default is `0.3`.
- **`text_color`** (`list` of `int`):
  - Color for displaying track IDs
- **`chunk_size`** (`int`): 
  - The number of frames to process in each batch. This helps manage memory usage for large videos. Default is `1000`.

- **`output_frequency`** (`int`): 
  - The frequency at which progress messages will be logged, measured in number of frames processed. For example, setting this to `100` will log every 100 frames. Default is `100`.


## Helpful scripts
You might find scripts from /scripts helpful

### Track ID Comparison Script

This script identifies and extracts rows based on `track_id`s from two input CSV files. The script can:

1. **Find Common `track_id`s**: Extract rows from the first file that have `track_id`s present in both files.
2. **Find Unique `track_id`s in the First File**: Extract rows from the first file with `track_id`s not found in the second file.
3. **Find Unique `track_id`s in the Second File**: Extract rows from the second file with `track_id`s not found in the first file.

#### Usage

- **`--csv_path_1`**: Path to the first CSV file.
- **`--csv_path_2`**: Path to the second CSV file.
- **`--common_output_path`**: (Optional) Path to save rows from the first file with `track_id`s common to both files.
- **`--diff_output_path_1`**: (Optional) Path to save rows from the first file with `track_id`s not present in the second file.
- **`--diff_output_path_2`**: (Optional) Path to save rows from the second file with `track_id`s not present in the first file.

#### Example

```bash
python python find_track_ids.py /path/to/first.csv /path/to/second.csv --common_output_path /path/to/output/common_output.csv --diff_output_path_1 /path/to/output/diff_output_1.csv --diff_output_path_2 /path/to/output/diff_output_2.csv

```
### Displacement Plotter for Trajectory Data

This script generates displacement plots for given `track_id`s from a CSV file containing trajectory data. Three types of plots are created for each specified track:

1. **Displacement from Start**: Distance from the start of the trajectory over time.
2. **Displacement from Previous Position**: Distance from the previous position in the trajectory over time.
3. **Displacement Components (`dx`, `dy`)**: Separate plots for the changes in `x` and `y` coordinates between frames.


#### Usage

- **`--csv_path`**: Path to the input CSV file containing trajectory data with `track_id`, `x`, `y`, and `frame_y` columns.
- **`--track_ids`**: List of track IDs for which to create plots (space-separated).
- **`--pixel_size`**: Size of one pixel in micrometers, used to calculate displacements.
- **`--output_dir`**: Directory where plots will be saved.

#### Example

```bash
python plot_displacements.py /path/to/trajectory.csv --track_ids 1 2 3 --pixel_size 0.1 --output_dir /path/to/output
```
