import os
import random
import requests
import tempfile
from itertools import chain
from flask import Flask, render_template, request
from quoteengine import QuoteModel, Ingestor
from memeengine import MemeGenerator

app = Flask(__name__)

meme = MemeGenerator('./static')


def setup():
    """Load all resources."""
    quote_files = [
        './_data/DogQuotes/DogQuotesTXT.txt',
        './_data/DogQuotes/DogQuotesDOCX.docx',
        './_data/DogQuotes/DogQuotesPDF.pdf',
        './_data/DogQuotes/DogQuotesCSV.csv'
    ]

    quotes = list(chain(*[Ingestor.parse(f) for f in quote_files]))
    images_path = "./_data/photos/dog/"
    imgs = [os.path.join(images_path, name)
            for name in os.listdir(images_path)]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user-defined meme."""
    req_img = requests.get(request.form['image_url'])
    quote = QuoteModel(body=request.form['body'],
                       author=request.form['author'])

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"{random.randint(0, 100000)}.png")

    with open(temp_path, 'wb') as temp_file:
        temp_file.write(req_img.content)

    path = meme.make_meme(temp_path, quote.body, quote.author)
    os.remove(temp_path)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
