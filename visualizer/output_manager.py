import os
import tifffile as tiff
import numpy as np
import cv2
class OutputManager:
    """
    Manages the output of processed video frames, saving them to TIFF and AVI files.

    This class handles the creation of output directories and the saving of processed
    video frames in both TIFF and AVI formats. It provides flexibility in specifying
    the output directory and handles file naming conventions based on frame ranges.

    Attributes:
        output_dir (str): The base output directory.
        output_dir_with_masks (str): Directory for TIFF files with masks.
        output_dir_without_masks (str): Directory for TIFF files without masks. (Not currently used)

    """
    def __init__(self, output_dir, fps, save_as_tiff):
        """Initialize file manager with base output directory."""
        self.output_dir_tiff = os.path.join(output_dir, "tiff_format")
        self.output_dir_avi = os.path.join(output_dir, "avi_format")
        self.fps = fps
        self.as_tiff = save_as_tiff
        self._setup_output_directories()

    def _setup_output_directories(self):
        """Create output directories for with and without masks."""
        if self.as_tiff:
            os.makedirs(self.output_dir_tiff, exist_ok=True)
        os.makedirs(self.output_dir_avi, exist_ok=True)

    def save_frames(self, frames, start_frame, end_frame, width, height):
        """
        Saves the processed frames to TIFF and AVI files.

        Args:
            frames (list): A list of processed video frames (NumPy arrays).
            start_frame (int): The starting frame index of the chunk.
            end_frame (int): The ending frame index of the chunk.
            width (int): Width of the frames in pixels.
            height (int): Height of the frames in pixels.
        """
        if self.as_tiff:
            self._save_tiff_chunk(frames, start_frame, end_frame)
        self._save_avi_chunk(frames, start_frame, end_frame, width, height)

    def _save_tiff_chunk(self, frames, start_frame, end_frame):
        """Saves a chunk of frames as a multi-page TIFF file."""
        filename = os.path.join(
            self.output_dir_tiff,
            f'chunk_{start_frame}_{end_frame}.tiff'
        )
        print(f"Saving frames {start_frame} to {end_frame} to {filename}")
        tiff.imwrite(filename, np.array(frames), imagej=True)
        file_size = os.path.getsize(filename) / (1024 * 1024)
        print(f"Saved file {filename} (size: {file_size:.2f} MB)")

    def _save_avi_chunk(self, frames, start_frame, end_frame, width, height):
        """Saves a chunk of frames as an AVI video file."""
        filename = os.path.join(
            self.output_dir_avi,
            f'chunk_{start_frame}_{end_frame}.avi'
        )
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(filename, fourcc, self.fps, (width, height))

        for frame in frames:
            bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(bgr_frame)
        out.release()

        file_size = os.path.getsize(filename) / (1024 * 1024)
        print(f"Saved AVI to: {filename} (size: {file_size:.2f} MB)")