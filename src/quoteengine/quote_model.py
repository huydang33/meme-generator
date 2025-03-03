class QuoteModel:
    """Class to encapsulate "body" and "author"."""

    def __init__(self, body: str, author: str):
        """
        :param body: Content of the quote.
        :param author: Author name.
        """
        self.body = body
        self.author = author
    
    def __repr__(self):
        """Retun a string representation of the quote."""
        return f'"{self.body}" - {self.author}'