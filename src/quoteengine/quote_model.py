"""
Module for encapsulating a quote with its body and author.

This module defines the `QuoteModel` class, which is used to represent a quote
with two main attributes: the body (content) of the quote and the author. It
provides a simple structure for storing and representing quotes.

Classes:
    QuoteModel: A class that encapsulates a quote with its body and author.

Usage:
    You can create a `QuoteModel` instance by passing a quote's body and author
    to the constructor and then use its string representation method to print
    or display the quote in a formatted way.
"""

class QuoteModel:
    """A class to encapsulate a quote with its body and author.

    This class represents a quote with two attributes:
    - body: the content of the quote.
    - author: the author of the quote.

    Attributes:
        body (str): The content of the quote.
        author (str): The author of the quote.

    Methods:
        __repr__: Returns a string representation of the quote in the format:
                  '"body" - author'.
    """

    def __init__(self, body: str, author: str):
        """
        Initialize a QuoteModel instance with the given body and author.

        :param body: The content of the quote.
        :param author: The author of the quote.
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Return a string representation of the quote."""
        return f'"{self.body}" - {self.author}'
