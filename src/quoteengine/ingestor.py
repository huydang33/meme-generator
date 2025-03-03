from typing import List
from .quote_model import QuoteModel
from abc import ABC, abstractmethod

import subprocess

import csv
import docx

# The IngestorInterface class is an abstract base class that defines two class methods: can_ingest and parse.
class IngestorInterface(ABC):
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass

class Ingestor_csv(IngestorInterface):
    """Import quotes from csv files"""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True if the file is a csv file."""
        if path.endswith('.csv'):
            return True
        return False

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Return a list of QuoteModel objects from a csv file."""
        if not cls.can_ingest(path):
            raise ValueError(f"File Type not supported for {path}")
        
        file = csv.reader(open(path, 'r'))
        return [QuoteModel(row[0], row[1]) for row in file]


class Ingestor_docx(IngestorInterface):
    """Import quotes from docx files"""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True if the file is a docx file."""
        if path.endswith('.docx'):
            return True
        return False

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f"File Type not supported for {path}")

        file = docx.Document(path)
        return [QuoteModel(paragraph.text.split(' - ')[0], paragraph.text.split(' - ')[1]) for paragraph in file.paragraphs]

class Ingestor_pdf(IngestorInterface):
    """Import quotes from pdf files"""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True if the file is a pdf file."""
        if path.endswith('.pdf'):
            return True
        return False
    
    def __extract_text(self, pdf_path):
        result = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True)
        return result.stdout

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f"File Type not supported for {path}")
        
        file = cls.__extract_text(path)
        return [QuoteModel(row[0], row[1]) for row in file]

class Ingestor_txt(IngestorInterface):
    """Import quotes from txt files"""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True if the file is a txt file."""
        if path.endswith('.txt'):
            return True
        return False

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f"File Type not supported for {path}")
        
        file = open(path, 'r')
        return [QuoteModel(row[0], row[1]) for row in file]
    
class Ingestor:
    """Ingestor class that imports quotes from different file types."""
    ingestors = [Ingestor_csv, Ingestor_docx, Ingestor_pdf, Ingestor_txt]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"File Type not supported for {path}")