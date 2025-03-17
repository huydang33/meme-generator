"""
Meme Generator Module.

This module defines the MemeGenerator class that is responsible for generating 
memes from images by overlaying text and author information.

The MemeGenerator class provides methods for loading an image, resizing it, adding the quote text 
and author to the image, and saving the generated meme.

Usage:
    To generate a meme, instantiate the MemeGenerator class with an output 
    directory, then call the make_meme method with the path to an image, 
    a quote, and the author's name.

Classes:
    MemeGenerator: A class that provides functionality for creating memes by 
                  adding text and author information to an image.

Functions:
    None.
"""

import tempfile
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class MemeGenerator:
    """
    MemeGenerator generates a meme from an image and text.

    This class provides functionality to generate memes by overlaying text 
    and author information on an image. It can either generate a meme from 
    initialized arguments or by setting the output directory and calling the 
    make_meme method to get back the processed meme image.

    Attributes:
        output_dir (Path): The directory where the meme will be saved.
    """

    def __init__(self, output_dir: str):
        """
        Initialize the MemeGenerator with the specified output directory.

        :param output_dir: Directory where the generated meme images will be saved.
        """
        self.output_dir = Path(output_dir)

    def load_image(self, img_path: str) -> None:
        """
        Load an image from the specified path.

        :param img_path: Path to the image file to be loaded.
        """
        self.image = Image.open(img_path)

    def __save_image(self) -> str:
        """
        Save the generated meme image to a file and returns the file path.

        Create a temporary file in the specified output directory and saves
        the image. Returns the path of the saved file.

        :return: The path of the saved meme image.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        full_output_path = tempfile.NamedTemporaryFile(
            dir=self.output_dir, prefix='meme-generator-',
            suffix='.jpg', delete=False
        ).name
        self.image.save(full_output_path)
        return str(full_output_path)

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        """
        Generate a meme by overlaying the given text and author on the image.

        Resize the image to the specified width while maintaining the aspect 
        ratio. Text is wrapped to fit within the image, and both the text and 
        author are drawn on the image.

        :param img_path: Path to the image file.
        :param text: Text to be overlayed on the image.
        :param author: Author of the quote to be overlayed on the image.
        :param width: Desired width of the output meme image (default: 500).
        
        :return: The path of the saved meme image.
        """
        self.load_image(img_path)

        # Resize the image while maintaining the aspect ratio
        aspect_ratio = width / self.image.width
        new_w = width
        new_h = int(self.image.height * aspect_ratio)
        self.image = self.image.resize((new_w, new_h), Image.NEAREST)

        # Wrap text to fit within the image
        wrapper = textwrap.TextWrapper(width=25)
        wrapped_text = "\n".join(wrapper.wrap(text))

        # Load fonts
        font_body = ImageFont.truetype("memeengine/arial.ttf", 20)
        font_author = ImageFont.truetype("memeengine/arial.ttf", 25)

        # Draw text on the image
        draw = ImageDraw.Draw(self.image)
        draw.text((140, 30), wrapped_text, font=font_body, fill="black")
        draw.text((140, new_h - 35), f"- {author}", font=font_author, fill="black")

        return self.__save_image()
