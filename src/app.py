import random
import os
import requests
from itertools import chain
import tempfile
from flask import Flask, render_template, abort, request

# Import your Ingestor and MemeEngine classes
from PIL import Image
from quoteengine import QuoteModel, Ingestor
from memeengine import MemeGenerator

app = Flask(__name__)

meme = MemeGenerator('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes = list(chain(*[Ingestor.parse(f) for f in quote_files]))

    images_path = "./_data/photos/dog/"

    # Use the pythons standard library os class to find all
    # images within the images images_path directory
    imgs = [os.path.join(images_path, name) for name in os.listdir(images_path)]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    req_img = requests.get(request.form['image_url'])
    quote = QuoteModel(body=request.form['body'], author=request.form['author'])
    temp_path = f"./tmp/{random.randint(0, 100000)}.png"
    _ = open(temp_path, 'wb').write(req_img.content)
    path = meme.make_meme(temp_path, quote.body, quote.author)
    # 3. Remove the temporary saved image.
    os.remove(temp_path)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
