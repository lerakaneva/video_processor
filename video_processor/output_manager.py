import os
import tifffile as tiff
import numpy as np

class OutputManager:
    def __init__(self, output_dir):
        """Initialize file manager with base output directory."""
        self.output_dir_with_masks = os.path.join(output_dir, "with_masks")
        self.output_dir_without_masks = os.path.join(output_dir, "without_masks")
        self._setup_output_directories()

    def _setup_output_directories(self):
        """Create output directories for with and without masks."""
        os.makedirs(self.output_dir_with_masks, exist_ok=True)
        os.makedirs(self.output_dir_without_masks, exist_ok=True)

    def save_frames(self, frames_with_masks, frames_without_masks, start_frame, end_frame):
        """Save processed frames with and without masks."""
        self._save_frame_chunk(frames_with_masks, start_frame, end_frame, masks=True)
        self._save_frame_chunk(frames_without_masks, start_frame, end_frame, masks=False)

    def _save_frame_chunk(self, frames, start_frame, end_frame, masks):
        """Helper method to save a chunk of frames, either with or without masks."""
        filename = os.path.join(
            self.output_dir_with_masks if masks else self.output_dir_without_masks,
            f'overlay_{"with" if masks else "without"}_masks_chunk_{start_frame}_{end_frame}.tiff'
        )
        print(f"Saving frames {start_frame} to {end_frame} {'with' if masks else 'without'} masks to {filename}")
        tiff.imwrite(filename, np.array(frames), imagej=True)
        file_size = os.path.getsize(filename) / (1024 * 1024)
        print(f"Saved file {filename} (size: {file_size:.2f} MB)")
