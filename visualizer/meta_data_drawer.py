import cv2

class MetaDataDrawer:
    """
    Draws metadata like timestamps and scale bars on video frames.

    This class takes metadata information (pixel size, time between frames)
    and uses it to draw timestamps and scale bars onto each frame.
    The appearance of the metadata (color, font, offsets) is customizable.

    Attributes:
        pixel_size (float): Size of a pixel in micrometers (µm). Used for
                            drawing the scale bar. If None, the scale bar
                            is not drawn.
        time_between_frames (float): Time interval between frames in seconds.
                                     Used to calculate and display timestamps.
                                     If None, timestamps are not drawn.
        scale_color (list): RGB color for the scale bar and timestamp text.


    """
    DEFAULT_COLOR = [255, 255, 255]
    TIME_LABEL_OFFSET_PX_X = 10
    TIME_LABEL_OFFSET_PX_Y = 30
    SCALE_OFFSET_X = 60
    SCALE_OFFSET_Y = 20
    SCALE_TEXT_EXTRA_OFFSET_Y = 5
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.5
    FONT_THICKNESS = 1
    TEXT_LINE_TYPE = cv2.LINE_AA
    SCALE_LINE_THICKNESS = 2
    SCALE_LENGTH_UM = 5
    
    def __init__(self, metadata):
        """
        Initializes MetaDataDrawer with metadata.

        Args:
            metadata (dict): Dictionary containing metadata:
                            - 'pixel_size' (float): Pixel size in µm.
                            - 'time_between_frames' (float): Time between frames in seconds.
                            - 'color' (list, optional): RGB color for text and scale bar.
                              Defaults to DEFAULT_COLOR.
        """
        self.pixel_size = metadata.get("pixel_size")
        self.time_between_frames = metadata.get("time_between_frames")
        self.scale_color = metadata.get("color", self.DEFAULT_COLOR)

    def draw(self, processed_frame, current_frame_idx):
        """
        Draws timestamp and scale bar on a frame.

        Args:
            processed_frame (np.ndarray): The frame (image) to draw on.
            current_frame_idx (int): The index of the current frame.  Used for
                                       timestamp calculation.

        """
        self._draw_time(processed_frame, current_frame_idx)
        self._draw_scale(processed_frame)
    
    def _draw_time(self, processed_frame, current_frame_idx):
        """
        Draws the timestamp on the frame.

        Args:
            processed_frame (np.ndarray): Frame to draw on.
            current_frame_idx (int):  Current frame index.
        """
        if self.time_between_frames is not None:
            time_str = f"{int(current_frame_idx * self.time_between_frames)} s"

            text_size, _ = cv2.getTextSize(time_str, self.FONT, self.FONT_SCALE, self.FONT_THICKNESS)
            text_x = processed_frame.shape[1] - text_size[0] - self.TIME_LABEL_OFFSET_PX_X
            text_y = self.TIME_LABEL_OFFSET_PX_Y

            cv2.putText(processed_frame, time_str, (text_x, text_y + text_size[1]),
                    self.FONT, self.FONT_SCALE, self.scale_color, self.FONT_THICKNESS, self.TEXT_LINE_TYPE)

    def _draw_scale(self, processed_frame):
        """
        Draws the scale bar on the frame.

        Args:
            processed_frame (np.ndarray): Frame to draw on.
        """
        if self.pixel_size is not None:
            # Define scale parameters
            scale_length_pixels = self.SCALE_LENGTH_UM / self.pixel_size 

            # Calculate scale line start and end points
            scale_x_start = processed_frame.shape[1] - int(scale_length_pixels) - self.SCALE_OFFSET_X
            scale_y = self.SCALE_OFFSET_Y
            scale_x_end = processed_frame.shape[1] - self.SCALE_OFFSET_X
            
            # Ensure that scale lines are greater than 0.1 of the length of video
            if scale_x_end - scale_x_start < processed_frame.shape[1]/10:
                scale_x_end = scale_x_start + int(processed_frame.shape[1]/10)


            # Draw the scale line
            cv2.line(processed_frame, (scale_x_start, scale_y), (scale_x_end, scale_y), self.scale_color, self.SCALE_LINE_THICKNESS)


            # Add scale text
            scale_text = f"{self.SCALE_LENGTH_UM} um"
            text_size, _ = cv2.getTextSize(scale_text, self.FONT, self.FONT_SCALE, self.FONT_THICKNESS)
            text_x = scale_x_end - text_size[0] // 2
            
            # Avoid overlapping the edges of the image
            text_x = min(max(0, text_x), processed_frame.shape[1] - text_size[0])

            cv2.putText(processed_frame, scale_text, (text_x, scale_y - self.SCALE_TEXT_EXTRA_OFFSET_Y),
                        self.FONT, self.FONT_SCALE, self.scale_color, self.FONT_THICKNESS, self.TEXT_LINE_TYPE)