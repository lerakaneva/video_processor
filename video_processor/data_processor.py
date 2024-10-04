import tifffile as tiff
import os
import pandas as pd
from video_processor.config_loader import ConfigLoader
from video_processor.output_manager import OutputManager
from video_processor.frame_processor import BatchFrameProcessor

class DataProcessor:
    DEFAULT_CHUNK_SIZE = 1000
    
    def __init__(self, config_path: str):
        """Initialize the processor with a config file."""
        self.config_loader = ConfigLoader(config_path)
        self.output_manager = OutputManager(self.config_loader.get('output_dir'))
        self._load_data()

        self.batch_frame_processor = BatchFrameProcessor(
            self.trajectory_data,
            self.config_loader.get('mask_colors', {}),
            tuple(self.config_loader.get('text_color', [])),
            self.config_loader.get('alpha'),
            self.config_loader.get('output_frequency')
        )
        
        self.chunk_size = self.config_loader.get('chunk_size', self.DEFAULT_CHUNK_SIZE)

    def _load_data(self):
        """Load microscopy video, segmentation mask, and trajectory data."""
        self.microscopy_video = tiff.imread(self.config_loader.get('microscopy_video_path'))
        self.segmentation_mask = tiff.imread(self.config_loader.get('segmentation_mask_path'))

        if self.microscopy_video.shape != self.segmentation_mask.shape:
            raise ValueError("The video and mask dimensions do not match")

        self.trajectory_data = {}
        for trajectory in self.config_loader.get('trajectories'):
            trajectory_name = trajectory['name']
            trajectory_file = os.path.join(self.config_loader.get('csv_folder'), trajectory['file'])
            color = tuple(trajectory['color'])
            self.trajectory_data[trajectory_name] = {
                'data': pd.read_csv(trajectory_file),
                'color': color
            }

        print('Loaded all data: microscopy video, segmentation mask, and trajectory files.')

    def process_data(self):
        """Process the video and trajectories, saving output with and without masks."""
        num_frames = len(self.microscopy_video)
        for start_frame in range(0, num_frames, self.chunk_size):
            end_frame = min(start_frame + self.chunk_size, num_frames)
            print(f"Processing frames {start_frame} to {end_frame}")

            frames_with_masks, frames_without_masks = self.batch_frame_processor.process_batch(
                self.microscopy_video, self.segmentation_mask, start_frame, end_frame)

            self.output_manager.save_frames(frames_with_masks, frames_without_masks, start_frame, end_frame)
