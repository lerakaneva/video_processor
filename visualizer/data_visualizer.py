import tifffile as tiff
import os
import pandas as pd
from visualizer.config_loader import ConfigLoader
from visualizer.output_manager import OutputManager
from visualizer.frame_visualizer import FrameVisualizer

class DataVisualizer:
    """
    Loads, processes, and visualizes microscopy data.

    This class orchestrates the loading of microscopy video, segmentation masks,
    cell labels, and trajectory data. It then uses the `FrameVisualizer` to
    overlay visualizations onto the video frames and the `OutputManager` to save
    the processed frames as TIFF and AVI files.  Configuration is managed via a
    JSON config file.

    Attributes:
        config_loader (ConfigLoader): Object for loading configuration parameters.
        output_manager (OutputManager): Object for managing output file saving.
        original (np.ndarray): Loaded original video frames.
        segmentation_mask (np.ndarray): Loaded segmentation masks.
        cell_labels_data (dict): Loaded cell label data (see CellTrackingDrawer for format).
        trajectory_data (dict): Loaded trajectory data (see CellTrackingDrawer for format).
        batch_frame_processor (FrameVisualizer): Object for processing and visualizing frames.
        chunk_size (int): Number of frames to process in each batch.
        width (int): Width of the video frames.
        height (int): Height of the video frames.

    """
    DEFAULT_CHUNK_SIZE = 1000
    
    def __init__(self, config_path: str):
        """
        Initializes the DataVisualizer with a configuration file.

        Args:
            config_path (str): Path to the JSON configuration file.
        """
        """Initialize the processor with a config file."""
        self.config_loader = ConfigLoader(config_path)
        self.output_manager = OutputManager(self.config_loader.get('output_dir'), self.config_loader.get('output_fps'), self.config_loader.get('save_as_tiff', False))
        self._load_data()

        self.batch_frame_processor = FrameVisualizer(
            self.cell_labels_data,
            self.trajectory_data,
            self.config_loader.get('mask_colors', {}),
            self.config_loader.get('track_id_color', None),
            self.config_loader.get('alpha'),
            self.config_loader.get('output_frequency'),
            self.config_loader.get('metadata', {}),
        )
        
        self.chunk_size = self.config_loader.get('chunk_size', self.DEFAULT_CHUNK_SIZE)

    def _load_data(self):
        """
        Loads microscopy video, segmentation mask, cell labels, and trajectory data.

        Reads the original video frames, segmentation masks, cell labels (from CSV),
        and trajectories (from CSV) from the paths specified in the configuration file.
        Stores the loaded data in the respective attributes of the class.
        """
        try:
            self.original = tiff.imread(self.config_loader.get('originals_path'))
            self.height, self.width = self.original[0].shape # Get dimensions here
            self.segmentation_mask = tiff.imread(self.config_loader.get('segmentation_masks_path'))

            if self.original.shape != self.segmentation_mask.shape:
                raise ValueError("The video and mask dimensions do not match")

            self.cell_labels_data = {}
            for label in self.config_loader.get('cell_labels'):
                name = label['name']
                file_path = os.path.join(self.config_loader.get('csv_folder_cell_labels'), label['file'])
                color = tuple(label['color'])
                try:
                    data = pd.read_csv(file_path)
                    self.cell_labels_data[name] = {
                        'data': data,
                        'color': color
                    }
                except (FileNotFoundError, pd.errors.ParserError) as e:
                    print(f"Error reading cell labels file {file_path}: {e}")
                    exit(1)  # Exit with an error code

            trajectories = self.config_loader.get('cell_trajectories')
            self.trajectory_data = {}
            if trajectories:
                file_path = trajectories['file']
                color = tuple(trajectories['color'])
                try:
                    data = pd.read_csv(file_path)
                    self.trajectory_data  = {
                        'data': data,
                        'color': color
                    }
                except (FileNotFoundError, pd.errors.ParserError) as e:
                    print(f"Error reading trajectories file {file_path}: {e}")
                    exit(1)  # Exit with an error code
                
            print('Loaded all data: microscopy video, segmentation mask, cell labels, trajectories')
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading data: {e}")
            exit(1)

    def process_data(self):
        """
        Processes and visualizes the loaded data.

        Iterates through the video frames in chunks (specified by `chunk_size`),
        processes each chunk by overlaying masks, labels, and trajectories using
        the `FrameVisualizer`, and saves the processed frames to output files
        (TIFF and/or AVI) using the `OutputManager`. Prints progress messages to
        the console during processing.
        """
        num_frames = len(self.original)
        for start_frame in range(0, num_frames, self.chunk_size):
            end_frame = min(start_frame + self.chunk_size, num_frames)
            print(f"Processing frames {start_frame} to {end_frame}")

            frames = self.batch_frame_processor.process_batch(
                self.original, self.segmentation_mask, start_frame, end_frame)

            self.output_manager.save_frames(frames, start_frame, end_frame, self.width, self.height)
