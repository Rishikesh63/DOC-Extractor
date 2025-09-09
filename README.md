
# Document Extraction Tool (Tika Only)

This project provides a Python script for extracting text and metadata from documents (PDF, DOCX, and more) using Apache Tika.

## Features
- **Text & Metadata Extraction:** Uses Apache Tika for multi-format text and metadata extraction.
- **Organized Output:** Results are saved in the `extracted` folder, with a summary JSON file for each input document.
- **Metrics:** Each extraction includes metrics such as percent of information extracted, output format, and method used.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Rishikesh63/DOC-Extractor
   ```
2. Install Poetry (if not already installed):
   ```
   pip install poetry
   ```
3. Activate the Poetry shell for an isolated environment:
   ```
   poetry shell
   ```
4. Install dependencies with Poetry:
   ```
   poetry install
   ```

## Usage
2. Run the extraction script:
   ```
    python extractor.py <path of your file>
   ```
3. Results will be saved in the `extracted` folder:
   - `<filename>_tika.json`: Extraction summary and data

## Supported Formats
- PDF, DOCX, TXT, HTML, and many other common document types

## Method Used
- Open source tool: Apache Tika
- No client permission needed for open source/local processing

## Notes
- Only text and metadata extraction is supported in this version.
- For advanced image or table extraction, use specialized tools.
