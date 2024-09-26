import numpy as np
import cv2

class BatchFrameProcessor:
    DEFAULT_ALPHA = 0.3
    DEFAULT_OUTPUT_FREQUENCY = 100
    
    def __init__(self, trajectory_data, mask_colors, alpha, output_frequency):
        self.trajectory_data = trajectory_data
        self.mask_colors = mask_colors
        self.alpha = alpha if alpha else self.DEFAULT_ALPHA
        self.output_frequency = output_frequency if output_frequency else self.DEFAULT_OUTPUT_FREQUENCY

    def process_batch(self, video, mask, start_frame, end_frame):
        """Process a batch of frames and return lists of frames with and without masks."""
        combined_frames_with_masks = []
        combined_frames_without_masks = []

        for i in range(start_frame, end_frame):
            frame = video[i]
            mask_frame = mask[i]

            if i % self.output_frequency == 0:
                print(f"Processing frame {i}")

            frame_rgb = self._convert_to_rgb(frame)
            combined_frame_with_masks = self._process_single_frame(frame_rgb, mask_frame)
            combined_frame_without_masks = frame_rgb.copy()

            self._draw_trajectories_on_frames(combined_frame_with_masks, combined_frame_without_masks, i)
            combined_frames_with_masks.append(combined_frame_with_masks)
            combined_frames_without_masks.append(combined_frame_without_masks)

        return combined_frames_with_masks, combined_frames_without_masks

    def _convert_to_rgb(self, frame):
        """Convert a grayscale frame to RGB if necessary."""
        return np.stack([frame] * 3, axis=-1) if len(frame.shape) == 2 else frame

    def _process_single_frame(self, frame, mask):
        """Applies the segmentation mask to a frame."""
        mask_colors = np.zeros_like(frame)
        for class_id, color in self.mask_colors.items():
            mask_colors[mask == int(class_id)] = color
        return np.uint8(frame * (1 - self.alpha) + mask_colors * self.alpha)

    def _draw_trajectories_on_frames(self, frame_with_masks, frame_without_masks, current_frame):
        """Draw trajectory points on both frames with and without masks."""
        for _, info in self.trajectory_data.items():
            points_in_frame = info['data'][info['data']['frame_y'] == current_frame]
            self._draw_trajectory_points(frame_with_masks, points_in_frame, info['color'])
            self._draw_trajectory_points(frame_without_masks, points_in_frame, info['color'])

    def _draw_trajectory_points(self, frame, points_in_frame, color):
        """Draw small circles at each point in the frame."""
        for _, row in points_in_frame.iterrows():
            x, y = int(row['x']), int(row['y'])
            cv2.circle(frame, (x, y), radius=3, color=color, thickness=-1)
