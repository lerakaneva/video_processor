import cv2

class CellTrackingDrawer:
    """
    Draws cell labels and trajectories on video frames.

    This class handles the visualization of cell tracking data, including
    drawing cell labels (circles) with optional track IDs and drawing
    trajectories as lines connecting cell positions across frames.

    Attributes:
        cell_labels (dict): Dictionary where keys are cell label names (strings)
                            and values are dictionaries containing 'data' (DataFrame)
                            and 'color' (tuple).  The DataFrame should contain
                            'frame_y', 'x', 'y', and optionally 'track_id' columns.
        trajectories (dict): Dictionary where keys are track IDs (integers) and
                             values are dictionaries containing 'max_frame' (int),
                             'points' (list of (frame, x, y) tuples), and 'color' (tuple).
        track_id_color (tuple): RGB color for displaying track IDs. If None,
                                 track IDs are not drawn.

    """
    LABEL_RADIUS = 3
    LABEL_THICKNESS = -1
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.5
    FONT_THICKNESS = 1
    TEXT_LINE_TYPE = cv2.LINE_AA
    TEXT_OFFSET_X = 5
    TEXT_OFFSET_Y = -5
    TRAJECTORY_LINE_THICKNESS = 2

    def __init__(self, cell_labels_data, trajectory_data, track_id_color):
        self.cell_labels = {}
        for name in cell_labels_data:
            self.cell_labels[name] = cell_labels_data[name]
        self.trajectories = self._generate_trajectories(trajectory_data) if trajectory_data else {}
        self.track_id_color = tuple(track_id_color) if track_id_color else None

    def _generate_trajectories(self, trajectory_data):
        """
        Processes trajectory data into a format suitable for visualization.

        Groups trajectory points by track ID, sorts them by frame number,
        and finds the last frame each track appears in. This pre-processing
        improves the efficiency of drawing trajectories as continuous lines.

        Args:
            trajectory_data (dict): Dictionary with 'data' (DataFrame containing
                                      'track_id', 'frame_y', 'x', 'y' columns) and
                                      'color' (RGB color tuple).

        Returns:
            dict:  Processed trajectory data keyed by track ID. Each value is a
                   dictionary with 'max_frame', 'points', and 'color'.

        """
        trajectories = {}
        unique_track_ids = trajectory_data['data']['track_id'].unique()
        for track_id in unique_track_ids:
            track_data = trajectory_data['data'][trajectory_data['data']['track_id'] == track_id]
            
            # Sort by frame number to ensure chronological order
            track_data = track_data.sort_values('frame_y')
            
            trajectory_points = []  # Store points for the current track
            
            for _, row in track_data.iterrows():
                frame_y = int(row['frame_y'])
                x, y = int(row['x']), int(row['y'])
                trajectory_points.append((frame_y, x, y))

            trajectories[track_id] = {
                'max_frame': track_data['frame_y'].max(),
                'points': trajectory_points,
                'color': trajectory_data['color']
            }
            
        return trajectories


    def draw_cell_tracking(self, processed_frame, current_frame_idx):
        """
        Draws cell labels and trajectories on a single frame.

        Iterates through the provided cell label and trajectory data, filtering for
        entries relevant to the current frame. Labels are drawn as circles, and
        trajectories are drawn as lines connecting the cell positions in
        previous frames.

        Args:
            processed_frame (np.ndarray): The frame to draw on.
            current_frame_idx (int): The index of the current frame.
        """
        for _, info in self.trajectories.items():
            if info['max_frame'] < current_frame_idx:
                continue
            # Extract points for the current track and previous frames
            points_to_draw = [
                (x, y) for frame, x, y in info['points'] if frame <= current_frame_idx
            ]
            self._draw_trajectory(processed_frame, points_to_draw, info['color'])
        for _, info in self.cell_labels.items():
            points_in_frame = info['data'][info['data']['frame_y'] == current_frame_idx]
            self._draw_labels(processed_frame, points_in_frame, info['color'])


    def _draw_labels(self, frame, points_in_frame, color):
        """
        Draws cell labels with track IDs (if enabled) on the frame.

        Args:
            frame (np.ndarray): The image frame to draw on.
            points_in_frame (pd.DataFrame): DataFrame containing 'x', 'y',
                                            and optionally 'track_id' for the
                                            current frame.
            color (tuple): RGB color of the cell labels.
        """
        for _, row in points_in_frame.iterrows():
            x, y = int(row['x']), int(row['y'])
            track_id = row['track_id']
            cv2.circle(frame, (x, y), radius=self.LABEL_RADIUS, color=color, thickness=self.LABEL_THICKNESS)
            # Show track id if the color has been provided
            if self.track_id_color:
                text_position = (x + self.TEXT_OFFSET_X, y - self.TEXT_OFFSET_Y)
                cv2.putText(frame, str(int(track_id)), text_position, self.FONT, 
                            fontScale=self.FONT_SCALE, color=self.track_id_color,
                            thickness=self.FONT_THICKNESS, lineType=self.TEXT_LINE_TYPE)

    def _draw_trajectory(self, frame, points_to_draw, color):
        """
        Draws a trajectory line on the frame.

        Args:
            frame (np.ndarray): The image to draw on.
            points_to_draw (list): List of (x, y) tuples representing the
                                    trajectory points.
            color (tuple): RGB color of the trajectory.
        """
        if len(points_to_draw) > 1:
            for i in range(len(points_to_draw) - 1):
                cv2.line(frame, points_to_draw[i], points_to_draw[i+1], color, self.TRAJECTORY_LINE_THICKNESS)
