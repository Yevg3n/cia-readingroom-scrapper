from dataclasses import dataclass


@dataclass
class Document:
    id: str
    title: str
    publication_date: str
    content_type: str
    pdf_url: str
    body: str