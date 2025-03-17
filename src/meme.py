import os
import random
import argparse
from quoteengine import Ingestor
from quoteengine.quote_model import QuoteModel
from memeengine import MemeGenerator


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given a path and a quote."""
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
    """Parse command-line arguments."""
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
