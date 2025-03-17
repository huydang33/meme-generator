"""
Ingestor for file formats.

This module defines the interface and concrete classes responsible for 
ingesting quotes from various file formats including CSV, DOCX, PDF, and TXT.

The main class, Ingestor, selects the appropriate ingestor based on the file 
type and uses it to parse quotes into QuoteModel instances.

Classes:
    IngestorInterface: An abstract base class that defines the interface for 
                        all ingestor classes.
    IngestorCSV: A class to ingest quotes from CSV files.
    IngestorDOCX: A class to ingest quotes from DOCX files.
    IngestorPDF: A class to ingest quotes from PDF files using the `pdftotext` 
                 tool.
    IngestorTXT: A class to ingest quotes from TXT files.
    Ingestor: A class that selects the appropriate ingestor based on the file 
              type and parses the quotes.

Functions:
    None.
"""

from typing import List
from .quote_model import QuoteModel
from abc import ABC, abstractmethod
import subprocess
import csv
import docx


class IngestorInterface:
    """An abstract base class that defines the interface for all ingestor classes."""

    def can_ingest(self, path: str) -> bool:
        """Determine if the given file can be ingested by this class."""
        raise NotImplementedError

    def parse(self, path: str) -> [QuoteModel]:
        """Parse the given file and returns a list of QuoteModel instances."""
        raise NotImplementedError


class IngestorCSV(IngestorInterface):
    """A class to ingest quotes from CSV files."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True if the file is a CSV file, False otherwise."""
        return path.endswith('.csv')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the CSV file at the given path and returns a list of QuoteModel instances."""
        if not cls.can_ingest(path):
            raise ValueError(f"Unsupported file type: {path}")

        quotes = []
        with open(path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'body' in row and 'author' in row:
                    quotes.append(QuoteModel(row['body'], row['author']))
        return quotes


class IngestorDOCX(IngestorInterface):
    """A class to ingest quotes from DOCX files."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True if the file is a DOCX file, False otherwise."""
        return path.endswith('.docx')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the DOCX file at the given path and returns a list of QuoteModel instances."""
        if not cls.can_ingest(path):
            raise ValueError(f"Unsupported file type: {path}")

        quotes = []
        doc = docx.Document(path)
        for para in doc.paragraphs:
            if ' - ' in para.text:
                parts = para.text.rsplit(' - ', 1)
                if len(parts) == 2:
                    quotes.append(QuoteModel(parts[0].strip(),
                                             parts[1].strip()))
        return quotes


class IngestorPDF(IngestorInterface):
    """A class to ingest quotes from PDF files using the `pdftotext` tool."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True if the file is a PDF file, False otherwise."""
        return path.endswith('.pdf')

    @staticmethod
    def __extract_text(pdf_path: str) -> List[str]:
        """Return True if the file is a PDF file, False otherwise."""
        result = subprocess.run(["pdftotext", pdf_path, "-"],
                                capture_output=True, text=True)
        return result.stdout.strip().split('\n')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the PDF file at the given path and returns a list of QuoteModel instances."""
        if not cls.can_ingest(path):
            raise ValueError(f"Unsupported file type: {path}")

        quotes = []
        lines = cls.__extract_text(path)
        for line in lines:
            parts = line.rsplit(' - ', 1)
            if len(parts) == 2:
                quotes.append(QuoteModel(parts[0].strip(), parts[1].strip()))
        return quotes


class IngestorTXT(IngestorInterface):
    """A class to ingest quotes from TXT files."""

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True if the file is a TXT file, False otherwise."""
        return path.endswith('.txt')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the TXT file at the given path and returns a list of QuoteModel instances."""
        if not cls.can_ingest(path):
            raise ValueError(f"Unsupported file type: {path}")

        quotes = []
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().rsplit(' - ', 1)
                if len(parts) == 2:
                    quotes.append(QuoteModel(parts[0].strip(),
                                             parts[1].strip()))
        return quotes


class Ingestor:
    """Select the appropriate ingestor based on the file type."""

    ingestors = [IngestorCSV, IngestorDOCX, IngestorPDF, IngestorTXT]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Select the appropriate ingestor based on file type and returns the parsed quotes."""
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"Unsupported file type: {path}")
