"""
This module provides access to the QuoteModel class and the Ingestor class.

The QuoteModel is used to represent a quote and its author,
while the Ingestor class is responsible for parsing various file formats (such
as TXT, DOCX, PDF, CSV) to extract and return a list of quotes.

Usage:
    Import this module to use the QuoteModel for quote data storage or
    Ingestor for parsing quotes from different file formats.

Classes:
    QuoteModel: A class that encapsulates a quote's body and the author's name.
    Ingestor: A class that handles the ingestion and parsing of quote data from
              different file formats.

Functions:
    None.
"""

from .quote_model import QuoteModel
from .ingestor import Ingestor
