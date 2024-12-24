import numpy as np

from visualizer.cell_tracker import CellTrackingDrawer
from visualizer.meta_data_drawer import MetaDataDrawer

class FrameVisualizer:
    """
    Overlays segmentation masks, cell labels, and trajectories onto video frames.

    This class takes pre-loaded data (masks, cell labels, trajectory information)
    and applies them visually to each frame of a video. It supports customizable
    colors, alpha blending for masks, and drawing of trajectories as continuous
    lines across frames.  It also integrates metadata display, such as timestamps
    and scale bars.

    Attributes:
        mask_colors (dict): Dictionary mapping mask class IDs (int) to RGB colors (tuple).
        track_id_color (tuple): RGB color for displaying track IDs.  If None, track IDs
                                 are not drawn.
        alpha (float): Alpha blending factor for masks (0.0 to 1.0).  A higher alpha
                       makes the masks more opaque.
        output_frequency (int): Frequency (in frames) at which processing progress is printed
                                 to the console.
        cell_tracking_drawer (CellTrackingDrawer): Object responsible for drawing cell labels
                                                    and trajectories.
        metadata_drawer (MetaDataDrawer): Object responsible for drawing metadata (scale bar,
                                            timestamp).
    """
    DEFAULT_ALPHA = 0.3
    DEFAULT_OUTPUT_FREQUENCY = 100
    LABEL_RADIUS = 3

    def __init__(self, cell_labels_data, trajectory_data, mask_colors, track_id_color, alpha, output_frequency, metadata):
        """
        Initializes the FrameVisualizer with visualization parameters and data.

        Args:
            cell_labels_data (dict): Cell label data (see CellTrackingDrawer for format).
            trajectory_data (dict): Trajectory data (see CellTrackingDrawer for format).
            mask_colors (dict): Mapping of mask class IDs to RGB colors.
            track_id_color (tuple): RGB color for track IDs.
            alpha (float): Mask blending factor.
            output_frequency (int): Frame processing output frequency.
            metadata (dict): Metadata for drawing (see MetaDataDrawer for format).
        """
        self.mask_colors = mask_colors
        self.track_id_color = tuple(track_id_color) if track_id_color else None
        self.alpha = alpha if alpha else self.DEFAULT_ALPHA
        self.output_frequency = output_frequency if output_frequency else self.DEFAULT_OUTPUT_FREQUENCY
        self.cell_tracking_drawer = CellTrackingDrawer(cell_labels_data, trajectory_data, track_id_color)
        self.metadata_drawer = MetaDataDrawer(metadata)

    def process_batch(self, original, mask, start_frame, end_frame):
        """
        Processes and visualizes a batch of video frames.

        Overlays masks, cell labels, and trajectories onto the original video frames
        within the specified frame range.

        Args:
            original (np.ndarray): The original video frames.
            mask (np.ndarray): The corresponding segmentation masks.
            start_frame (int): The starting frame index (inclusive).
            end_frame (int): The ending frame index (exclusive).

        Returns:
            list: A list of processed RGB frames with visualizations applied.
        """
        combined_frames = []

        for i in range(start_frame, end_frame):
            frame = original[i]
            mask_frame = mask[i]

            if i % self.output_frequency == 0:
                print(f"Processing frame {i}")

            frame_rgb = self._convert_to_rgb(frame)
            processed_frame = self._add_mask_to_frame(frame_rgb, mask_frame)

            self.cell_tracking_drawer.draw_cell_tracking(processed_frame, i)
            self.metadata_drawer.draw(processed_frame, i)
            combined_frames.append(processed_frame)

        return combined_frames

    def _convert_to_rgb(self, frame):
        """
        Converts a grayscale frame to RGB if necessary.

        Args:
            frame (np.ndarray): The input frame (grayscale or RGB).

        Returns:
            np.ndarray:  The frame converted to RGB.
        """
        if len(frame.shape) == 2:
            return np.stack([frame] * 3, axis=-1)
        else:
            return frame

    def _add_mask_to_frame(self, frame, mask):
        """
        Applies the segmentation mask to a frame using alpha blending.

        Args:
            frame (np.ndarray): The RGB frame to overlay the mask on.
            mask (np.ndarray): The segmentation mask.

        Returns:
            np.ndarray: The frame with the mask applied.
        """
        mask_colors = np.zeros_like(frame)
        for class_id, color in self.mask_colors.items():
            mask_colors[mask == int(class_id)] = color
        return np.uint8(frame * (1 - self.alpha * (mask_colors > 0)) + mask_colors * self.alpha)
