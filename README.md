# Meme Generator
A simple meme generator was created for the Udacity Intermediate Python Nanodegree program.

## Getting started

This project uses the Python virtual environment.

### Prerequisites

**poppler-utils** is installed from Ubuntu to use the **pdftotext**

```bash
sudo apt install poppler-utils
```

### Installation 

1. Clone the repo
```bash
git clone https://github.com/huydang33/meme-generator.git
```

2. Setup virtual environment
```bash
cd meme-generator
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies
```bash
pip install -r requirements.txt
```

4. Run by Command Line 

This will generate a random meme using a random image from *./_data/photos/dog/* and a random quote from one of the files in ./_data/DogQuotes/.
Quotes and images may be edited/added in the relevant folders, and memes will be randomly generated accordingly.

```bash
cd src
python3 meme.py
```

Running python meme.py with these optional parameters will allow for further customization.

- Using --path <path/to/image> will allow for a specific image to be used.

- Using --body "Insert quote here" --author "Name" will allow for a custom quote and author to be added to the image.

Note: --body and --author are required together. Inserting only one of these parameters will result in an error.

Example: 

```bash
python meme.py --path ./_data/photos/dog/corgi.jpg --body "Python is fun!" --author "Jonathan Hing".
```

5. Run by Flash

```bash
export FLASK_APP=app.py
flask run --host localhost --port 3000 --reload
```

# Modules and Sub-Modules

##### meme.py
- This is the CLI engine for generating random or custom memes.

##### app.py
- This contains the code for web app, run with Flask, to interact with the meme generator. 

##### Ingestors
- The sub-modules found here contain the code to ingest and parse the quotes, along with their authors. The allowed extensions for files which can contain this information can be found in [ingest-interface.py](./src/QuoteEngine/ingest_interface.py).
  - The currently allowed file extensions are `'csv', 'docx', 'pdf', 'txt'`.

##### QuoteEngine
- These sub-modules contain the classes and functions to handle the quotes and images.
  - [meme_engine.py](./src/QuoteEngine/meme_engine.py) apply font and character size

_____

# Authors
##### :bust_in_silhouette: Jonathan Hing
- Github: [@HuyDang](https://github.com/huydang33)

_____

# Contributors :sparkles:

- Sample [data](./_data) for quotes and images, as well as [html templates](./templates) provided by Udacity.