import camelot
import sys
import json
import os
from datetime import datetime
from tika import parser as tika_parser
import pdfplumber
import docx

def extract_tika(file_path):
    parsed = tika_parser.from_file(file_path)
    result = {
        'text': parsed.get('content', ''),
        'metadata': parsed.get('metadata', {}),
        'output_format': {'text': 'str', 'metadata': 'dict'}
    }
    return result

def extract_images_pdf(file_path, image_folder):
    images = []
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            for img_num, img in enumerate(page.images):
                bbox = (img['x0'], img['top'], img['x1'], img['bottom'])
                cropped = page.crop(bbox).to_image(resolution=300)
                img_path = os.path.join(image_folder, f'pdf_page{page_num+1}_img{img_num+1}.png')
                cropped.save(img_path, format='PNG')
                images.append(img_path)
    return images

def extract_images_docx(file_path, image_folder):
    images = []
    doc = docx.Document(file_path)
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            img_data = rel.target_part.blob
            img_name = os.path.basename(rel.target_ref)
            img_path = os.path.join(image_folder, img_name)
            with open(img_path, 'wb') as f:
                f.write(img_data)
            images.append(img_path)
    return images

def summarize_extraction(result):
    summary = {}
    summary['text_extracted'] = bool(result['text'])
    summary['output_format'] = result['output_format']
    summary['metadata_extracted'] = bool(result.get('metadata'))
    # Estimate % info extracted (simple heuristic)
    summary['percent_info_extracted'] = int(summary['text_extracted']) * 100
    return summary


def extract_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    result = extract_tika(file_path)
    images = []
    tables = []
    # Prepare output folders
    input_base = os.path.splitext(os.path.basename(file_path))[0]
    image_folder = os.path.join('extracted', f'{input_base}_images')
    table_folder = os.path.join('extracted', f'{input_base}_tables')
    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(table_folder, exist_ok=True)
    if ext == '.pdf':
        images = extract_images_pdf(file_path, image_folder)
        # Table extraction with Camelot
        try:
            camelot_tables = camelot.read_pdf(file_path, pages='all')
            for idx, table in enumerate(camelot_tables):
                table_path = os.path.join(table_folder, f'table_{idx+1}.csv')
                table.to_csv(table_path)
                tables.append(table_path)
        except Exception as e:
            print(f"Camelot table extraction error: {e}")
    elif ext == '.docx':
        images = extract_images_docx(file_path, image_folder)
    result['images'] = images
    result['tables'] = tables
    summary = summarize_extraction(result)
    return summary, result

def get_metrics(summary, result, file_path):
    metrics = {}
    metrics['file'] = file_path
    metrics['extraction_time'] = datetime.now().isoformat()
    metrics['extracted_text'] = bool(result.get('text'))
    metrics['extracted_images'] = bool(result.get('images')) and len(result.get('images', [])) > 0
    metrics['extracted_tables'] = bool(result.get('tables')) and len(result.get('tables', [])) > 0
    metrics['percent_info_extracted'] = summary.get('percent_info_extracted', 0)
    metrics['percent_relevant_info'] = summary.get('percent_info_extracted', 0)  # Heuristic, same as extracted
    metrics['output_format'] = summary.get('output_format')
    metrics['method_used'] = 'open source (Apache Tika + pdfplumber/python-docx for images + Camelot for tables)'
    metrics['permission_needed'] = 'No (open source, local processing)'
    metrics['notes'] = 'Text/metadata via Tika; images via pdfplumber/python-docx; tables via Camelot.'
    return metrics



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python extractor.py <file_path>')
        sys.exit(1)
    file_path = sys.argv[1]
    summary, result = extract_document(file_path)
    metrics = get_metrics(summary, result, file_path)
    print('Extraction Summary:')
    print(json.dumps(metrics, indent=2))
    print('\nExtracted Data:')
    print(json.dumps(result, indent=2))

    # Organize output folder and filename
    output_folder = 'extracted'
    os.makedirs(output_folder, exist_ok=True)
    input_base = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_folder, f'{input_base}.json')

    # Save to file
    output = {
        'metrics': metrics,
        'summary': summary,
        'extracted_data': result
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f'\nExtraction results saved to {output_path}')
