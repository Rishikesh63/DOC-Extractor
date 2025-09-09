# Document Extraction Tool

This project provides a Python script for extracting text, metadata, images, and tables from documents (PDF, DOCX) using open-source libraries.

## Features
- **Text & Metadata Extraction:** Uses Apache Tika for multi-format text and metadata extraction.
- **Image Extraction:** Extracts images from PDFs (using pdfplumber) and DOCX (using python-docx).
- **Table Extraction:** Extracts tables from PDFs using Camelot and saves them as CSV files.
- **Organized Output:** Results are saved in the `extracted` folder, with subfolders for images and tables, and a summary JSON file for each input document.
- **Metrics:** Each extraction includes metrics such as percent of information extracted, output format, and method used.

## Requirements
- Python 3.8–3.11
- Install dependencies with Poetry:
  ```
  pip install poetry
  poetry shell
  poetry install
  ```

## Usage
1. Place your document (PDF or DOCX) in the project folder.
2. Run the extraction script:
   ```
   poetry run python extractor.py <your_document.pdf>
   ```
3. Results will be saved in the `extracted` folder:
   - `<filename>.json`: Extraction summary and data
   - `<filename>_images/`: Extracted images
   - `<filename>_tables/`: Extracted tables (CSV)

## Supported Formats
- PDF: Text, metadata, images, tables
- DOCX: Text, metadata, images

## Method Used
- Open source tools: Apache Tika, pdfplumber, python-docx, Camelot
- No client permission needed for open source/local processing

## Notes
- For advanced table/image extraction from other formats, further tool integration may be required.
- For questions or improvements, please contact the author.
