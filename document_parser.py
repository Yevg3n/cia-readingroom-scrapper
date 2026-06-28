from bs4 import BeautifulSoup
from repo.models.document import Document


def extract_doc_id(url):
    """Extract the CIA document slug from a reading room URL, e.g.
    https://www.cia.gov/readingroom/document/cia-rdp96-00789r002900010002-8
    -> cia-rdp96-00789r002900010002-8
    """
    return url.rstrip("/").rsplit("/", 1)[-1]


def _get_field(soup, field_class):
    tag = soup.select_one(f"div.{field_class} .field-item")
    if tag:
        return tag.get_text(strip=True)
    return "N/A"


def parse_document(page_source, doc_url):
    soup = BeautifulSoup(page_source, "html.parser")
    title = soup.select_one("h1.documentFirstHeading").get_text(strip=True)
    pdf_url = soup.select_one("div.field-name-field-file a")["href"]
    body = soup.select_one("div.field-name-body .field-item").get_text(separator=" ", strip=True)

    return Document(
        id = extract_doc_id(doc_url),
        title = title,
        publication_date = _get_field(soup, "field-name-field-pub-date"),
        content_type = _get_field(soup, "field-name-field-content-type"),
        pdf_url = pdf_url,
        body = body
    )
