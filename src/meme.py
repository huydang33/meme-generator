"""
Meme Generator Script.

This script allows for the generation of memes by adding quotes to images. The script
can either take a random image and quote or use a user-supplied image and quote. The
generated meme is saved to a temporary directory.

Modules used:
    - os: For interacting with the file system.
    - random: For randomly selecting images and quotes.
    - argparse: For parsing command-line arguments.
    - quoteengine: For ingesting quotes from different file formats.
    - memeengine: For generating memes by overlaying text on images.

Functions:
    - generate_meme: Generates a meme using a random or user-provided image and quote.
    - parse_args: Parses command-line arguments to get image path, quote body, and author.
"""

import os
import random
import argparse
from quoteengine import Ingestor
from quoteengine.quote_model import QuoteModel
from memeengine import MemeGenerator


def generate_meme(path=None, body=None, author=None):
    """
    Generate a meme given a path and a quote.

    This function generates a meme by adding a quote to an image. The image can be randomly
    chosen from a predefined set of dog images or provided by the user through the `path` argument.
    Similarly, the quote can either be randomly selected from a set of quote files or provided
    through the `body` and `author` arguments.

    Parameters:
        path (str, optional): The path to the image file. If None, a random image is selected.
        body (str, optional): The body of the quote to overlay on the image. If None, a random quote is used.
        author (str, optional): The author of the quote. Required if `body` is provided.

    Raises:
        ValueError: If `body` is provided without `author`.

    Returns:
        str: The path to the generated meme image.
    """
    if path is None:
        images = "./_data/photos/dog/"
        imgs = [os.path.join(root, name) for root, _, files
                in os.walk(images) for name in files]
        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = [
            './_data/DogQuotes/DogQuotesTXT.txt',
            './_data/DogQuotes/DogQuotesDOCX.docx',
            './_data/DogQuotes/DogQuotesPDF.pdf',
            './_data/DogQuotes/DogQuotesCSV.csv'
        ]
        quotes = [quote for f in quote_files for quote in Ingestor.parse(f)]
        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError('Author required if body is provided')
        quote = QuoteModel(body, author)

    meme = MemeGenerator('./tmp')
    return meme.make_meme(img, quote.body, quote.author)


def parse_args():
    """
    Parse command-line arguments.

    This function uses the argparse module to parse command-line arguments passed
    to the script. It allows the user to specify a custom image path, quote body, and author
    to generate a meme. If no arguments are provided, default behavior is to use random images
    and quotes.

    Returns:
        Namespace: The parsed arguments as a Namespace object containing:
            - path: The path to the image file (str).
            - body: The body of the quote (str).
            - author: The author of the quote (str).
    """
    parser = argparse.ArgumentParser(description='Generate a meme')
    parser.add_argument('--path', type=str, default=None,
                        help='Path to an image file')
    parser.add_argument('--body', type=str, default=None,
                        help='Quote body to add to the image')
    parser.add_argument('--author', type=str, default=None,
                        help='Quote author to add to the image')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(generate_meme(args.path, args.body, args.author))
