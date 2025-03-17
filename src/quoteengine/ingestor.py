from typing import List
from .quote_model import QuoteModel
from abc import ABC, abstractmethod
import subprocess
import csv
import docx


# Abstract base class for different ingestors
class IngestorInterface(ABC):
    @classmethod
    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the file type can be ingested."""
        pass

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse file and return a list of QuoteModel instances."""
        pass


class IngestorCSV(IngestorInterface):
    """Ingest quotes from CSV files."""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.endswith('.csv')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
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
    """Ingest quotes from DOCX files."""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.endswith('.docx')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
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
    """Ingest quotes from PDF files using `pdftotext`."""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.endswith('.pdf')

    @staticmethod
    def __extract_text(pdf_path: str) -> List[str]:
        """Extract text from PDF using `pdftotext`."""
        result = subprocess.run(["pdftotext", pdf_path, "-"],
                                capture_output=True, text=True)
        return result.stdout.strip().split('\n')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
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
    """Ingest quotes from TXT files."""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.endswith('.txt')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
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
    """Main ingestor class that selects the appropriate ingestor."""
    ingestors = [IngestorCSV, IngestorDOCX, IngestorPDF, IngestorTXT]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"Unsupported file type: {path}")
