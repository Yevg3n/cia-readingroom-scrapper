# cia-readingroom-scrapper

## Description
cia-readingroom-scrapper is a web scraping tool to collect declassified documents from the
CIA's FOIA Electronic Reading Room (https://www.cia.gov/readingroom/)

## The Problem It Solves
The CIA Reading Room hosts tens of thousands of declassified documents that are technically 
public — but practically difficult to access in bulk. 

The webpage features:
- no public API
- no bulk download option 
- intentionally built on outdated infrastructure (Drupal 7) that discourages automated access
- employs redirect-based bot protection and JavaScript challenges that block standard HTTP scraping tools

For individuals, finding documents of genuine interest means manually clicking through thousands of pages 
of search results — mixed heavily with bureaucratic paperwork, budget memos, and administrative forms 
that bury the truly remarkable 'peculiar' content.

## Requirements
- Python 3.12
- See `requirements.txt` for dependencies

## Usage
```bash
python main.py
```

## License
This project is for educational and research purposes only. 
Please respect the CIA Reading Room's terms of service when using this tool.
