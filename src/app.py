"""
Flask web application for generating memes.

This application allows users to generate memes using
random dog images and quotes, or to create custom memes
by providing an image URL and quote. The quotes are ingested
from various file formats, and the memes are generated
with text overlays.

Modules used:
    Flask: Web framework for creating the web application.
    requests: For fetching images from URLs.
    tempfile: For creating temporary file paths for storing images.
    os: For interacting with the file system.
    random: For generating random selections.
    quoteengine: Handles parsing of quotes from various file formats.
    memeengine: Handles meme generation with images and text.

Routes:
    - `/`: Displays a random meme generated from random images and quotes.
    - `/create` (GET): Displays a form for user input to create a custom meme.
    - `/create` (POST): Accepts user input, generates a meme,
                        and returns the result.
"""

import os
import random
import requests
import tempfile
from itertools import chain
from flask import Flask, render_template, request
from quoteengine import QuoteModel, Ingestor
from memeengine import MemeGenerator

app = Flask(__name__)

meme = MemeGenerator("./static")


def setup():
    """
    Load all resources.

    This function loads quotes from various file formats
    (TXT, DOCX, PDF, CSV) and images from a specified directory.
    It prepares the resources needed for meme generation.

    Returns:
        tuple: A tuple containing two elements:
            - List of QuoteModel instances (quotes).
            - List of image file paths (imgs).
    """
    quote_files = [
        "./_data/DogQuotes/DogQuotesTXT.txt",
        "./_data/DogQuotes/DogQuotesDOCX.docx",
        "./_data/DogQuotes/DogQuotesPDF.pdf",
        "./_data/DogQuotes/DogQuotesCSV.csv",
    ]

    quotes = list(chain(*[Ingestor.parse(f) for f in quote_files]))
    images_path = "./_data/photos/dog/"
    imgs = [os.path.join(images_path, name)
            for name in os.listdir(images_path)]

    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand():
    """
    Generate a random meme with a random image and quote.

    This function selects a random image and a random quote,
    creates a meme with them, and renders the meme on a webpage.

    Returns:
        render_template: Renders the meme.html template
                        with the generated meme's path.
    """
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template("meme.html", path=path)


@app.route("/create", methods=["GET"])
def meme_form():
    """
    Render the form for creating a custom meme.

    This function renders the meme creation form where users
    can input their custom quote and image URL.

    Returns:
        render_template: Renders the meme_form.html template with the form.
    """
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """
    Generate a custom meme based on user input.

    This function accepts user input via a POST request, downloads
    the image from the provided URL, and generates a meme
    with the given quote. The generated meme is then displayed.

    Returns:
        render_template: Renders the meme.html template
                         with the generated meme's path.
    """
    req_img = requests.get(request.form["image_url"])
    quote = QuoteModel(body=request.form["body"],
                       author=request.form["author"])

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"{random.randint(0, 100000)}.png")

    with open(temp_path, "wb") as temp_file:
        temp_file.write(req_img.content)

    path = meme.make_meme(temp_path, quote.body, quote.author)
    os.remove(temp_path)

    return render_template("meme.html", path=path)


if __name__ == "__main__":
    app.run()
