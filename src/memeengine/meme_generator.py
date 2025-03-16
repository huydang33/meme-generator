import tempfile
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

class MemeGenerator:
    """MemeGenerator generates a meme from an image and text.

    Generates a meme from either (1) initialized arguments or (2) by setting output_dir only during construction then
    calling make_make to get back a path of the processed meme image.
    """
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)

    def load_image(self, img_path: str) -> None:
        """Load image from path.

        :param img_path: Path to image
        """
        self.image = Image.open(img_path)

    def __save_image(self):
        """Return path of saved image file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        full_output_path = tempfile.NamedTemporaryFile(dir=self.output_dir.name, prefix='meme-generator-',
                                                       suffix='.jpg', delete=False).name
        self.image.save(full_output_path)
        return str(self.output_dir) + "/" + str(Path(full_output_path).name)

    def make_meme(self, img_path, text, author, width=500) -> str:
        """Override previously supplied params and saves image.

        Created for a specific use case:
            meme = MemeGenerator('./tmp')
            path = meme.make_meme(img, quote.body, quote.author)

        :param img_path: Loads image from path, overriding and previously stored image
        :param text: Input text to overlay on image
        :param author: Input author to overlay on image
        :param width: Scaled image keeping
        :return: location of saved file as a str
        """

        # Load image 
        self.load_image(img_path)

        # Resizing the image to width 500 and height scaled proportionally
        aspect_ratio = width / self.image.width
        new_w = int(self.image.width * aspect_ratio)
        new_h = int(self.image.height * aspect_ratio)
        self.image = self.image.resize((int(new_w), int(new_h)), Image.NEAREST)

        wrapper = textwrap.TextWrapper(width=25)
        words = wrapper.wrap(text=text)
        new_quote = ""
        for w in words[:-1]:
            new_quote = new_quote + w + '\n'
        new_quote += words[-1]

        # Load fonts
        font_body = ImageFont.truetype("memeengine/arial.ttf", 20)
        font_author = ImageFont.truetype("memeengine/arial.ttf", 25)

        # Prepare text and author
        d1 = ImageDraw.Draw(self.image)
        d1.text((140, 30), new_quote, font=font_body, fill="black")
        d1.text(
            (140,
            new_h - 35),
            f" - {author}",
            font=font_author,
            fill="black")

        return self.__save_image()