class InstructionsRenderer:
    def __init__(self, canvas, emoticons, canvas_width, double_click_callback=None):
        """
        Initialize the InstructionsRenderer.

        Args:
            canvas (tk.Canvas): The canvas where text and emoticons will be rendered.
            emoticons (dict): A dictionary mapping emoticon keys to their corresponding images.
            double_click_callback (callable): A function to call when the canvas is double-clicked.
        """
        self.canvas = canvas
        self.emoticons = emoticons
        self.canvas_width = canvas_width
        self.image_references = []  # To prevent garbage collection of images

        # Bind double-click event if a callback is provided
        if double_click_callback:
            self.canvas.bind("<Double-1>", double_click_callback)

    def render_text_with_emoticons(self, text, x_offset=5, y_offset=10):
        """
        Render text with embedded emoticons on the canvas.

        Args:
            text (str): The text to render, which may contain emoticon keys.
            x_offset (int): The starting x position for rendering.
            y_offset (int): The starting y position for rendering.
        """
        parts = text.split(" ")
        line_height = 0  # Tracks the height of the current line

        for part in parts:
            emoticon_key = f"{part}"
            if emoticon_key in self.emoticons:
                # Render an emoticon
                self._render_emoticon(emoticon_key, x_offset, y_offset)
                x_offset += 48 + 5  # Emoticon width + padding
                line_height = max(line_height, 48)  # Emoticon height
            else:
                # Render text
                x_offset, y_offset, line_height = self._render_text(
                    part, x_offset, y_offset, line_height)

    def _render_emoticon(self, emoticon_key, x_offset, y_offset):
        """
        Render an emoticon on the canvas.

        Args:
            emoticon_key (str): The key for the emoticon in the emoticons dictionary.
            x_offset (int): The x position for rendering.
            y_offset (int): The y position for rendering.
        """
        emote_image = self.emoticons[emoticon_key]
        self.image_references.append(emote_image)  # Prevent garbage collection
        self.canvas.create_image(
            x_offset, y_offset, image=emote_image, anchor="nw")

    def _render_text(self, text, x_offset, y_offset, line_height):
        def _draw_text(x, y):
            """Helper function to draw text and return its dimensions."""
            text_id = self.canvas.create_text(
                x, y, text=text, anchor="nw", font=("Sergoe UI Variable", 26))
            text_bbox = self.canvas.bbox(text_id)
            text_width = text_bbox[2] - text_bbox[0]
            return text_id, text_bbox, text_width

        # First attempt to draw the text
        text_id, text_bbox, text_width = _draw_text(x_offset, y_offset)

        # Check if the text exceeds the canvas width
        if x_offset + text_width > self.canvas_width:
            # Delete the initial text since it exceeds the canvas width
            self.canvas.delete(text_id)
            # Move to the next line
            x_offset = 5
            y_offset += line_height + 5
            line_height = 0
            # Redraw the text on the new line
            text_id, text_bbox, text_width = _draw_text(x_offset, y_offset)

        # Adjust offsets and line height
        x_offset += text_width + 5
        line_height = max(line_height, text_bbox[3] - text_bbox[1])
        return x_offset, y_offset, line_height
