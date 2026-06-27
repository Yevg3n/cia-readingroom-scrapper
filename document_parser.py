from bs4 import BeautifulSoup
from dataclasses import dataclass

OUTPUT_DIR = "document"


@dataclass
class Document:
    title: str
    publication_date: str
    content_type: str
    pdf_url: str
    body: str


def _get_field(soup, field_class):
    tag = soup.select_one(f"div.{field_class} .field-item")
    if tag:
        return tag.get_text(strip=True)
    return "N/A"


def parse_document(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    title = soup.select_one("h1.documentFirstHeading").get_text(strip=True)
    pdf_url = soup.select_one("div.field-name-field-file a")["href"]
    body = soup.select_one("div.field-name-body .field-item").get_text(separator=" ", strip=True)

    return Document(
        title = title,
        publication_date = _get_field(soup, "field-name-field-pub-date"),
        content_type = _get_field(soup, "field-name-field-content-type"),
        pdf_url = pdf_url,
        body = body
    )
