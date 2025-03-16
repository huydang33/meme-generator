import tempfile
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
        new_w = self.image.width * aspect_ratio
        new_h = self.image.height * aspect_ratio
        self.image = self.image.resize((int(new_w), int(new_h)))

        # Load fonts
        font_body = ImageFont.truetype("memeengine/arial.ttf", 20)
        font_author = ImageFont.truetype("memeengine/arial.ttf", 25)

        # Prepare text and author
        d1 = ImageDraw.Draw(self.image)

        # Calculate position for body text (center vertically with 30px from the bottom)
        text_width, text_height = d1.textsize(text, font=font_body)
        position_body = ((self.image.width - text_width) / 2, self.image.height - text_height - 30)

        # Calculate position for author text (30px above body)
        author_width, author_height = d1.textsize(author, font=font_author)
        position_author = ((self.image.width - author_width) / 2, position_body[1] - author_height - 30)

        # Draw quote text on image
        d1.text(position_body, text, anchor='rb', font=font_body, fill=(255, 255, 255))
        d1.text(position_author, author, anchor='rb', font=font_author, fill=(255, 255, 255))

        return self.__save_image()