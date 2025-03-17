import tempfile
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class MemeGenerator:
    """MemeGenerator generates a meme from an image and text.

    Generates a meme from either (1) initialized arguments or (2)
    by setting output_dir only during construction then
    calling make_meme to get back a path of the processed meme image.
    """
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)

    def load_image(self, img_path: str) -> None:
        """Load image from path.

        :param img_path: Path to image
        """
        self.image = Image.open(img_path)

    def __save_image(self) -> str:
        """Return path of saved image file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        full_output_path = tempfile.NamedTemporaryFile(
            dir=self.output_dir, prefix='meme-generator-',
            suffix='.jpg', delete=False
        ).name
        self.image.save(full_output_path)
        return str(full_output_path)

    def make_meme(self, img_path: str, text: str, author: str,
                  width: int = 500) -> str:
        """Generate a meme image with the given text and author.

        :param img_path: Path to the image file
        :param text: Text to overlay on the image
        :param author: Author of the quote
        :param width: Desired width of the meme image (default: 500)
        :return: Path of the saved meme image
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
        draw.text((140, new_h - 35), f"- {author}",
                  font=font_author, fill="black")

        return self.__save_image()
