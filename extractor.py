import sys
import json
import os
from datetime import datetime
from tika import parser as tika_parser

def extract_tika(file_path):
    parsed = tika_parser.from_file(file_path)
    result = {
        'text': parsed.get('content', ''),
        'metadata': parsed.get('metadata', {}),
        'output_format': {'text': 'str', 'metadata': 'dict'}
    }
    return result

def summarize_extraction(result):
    summary = {}
    summary['text_extracted'] = bool(result['text'])
    summary['output_format'] = result['output_format']
    summary['metadata_extracted'] = bool(result.get('metadata'))
    summary['percent_info_extracted'] = int(summary['text_extracted']) * 100
    return summary

def get_metrics(summary, result, file_path):
    metrics = {}
    metrics['file'] = file_path
    metrics['extraction_time'] = datetime.now().isoformat()
    metrics['extracted_text'] = bool(result.get('text'))
    metrics['extracted_images'] = False
    metrics['extracted_tables'] = False
    metrics['percent_info_extracted'] = summary.get('percent_info_extracted', 0)
    metrics['percent_relevant_info'] = summary.get('percent_info_extracted', 0)
    metrics['output_format'] = summary.get('output_format')
    metrics['method_used'] = 'open source (Apache Tika)'
    metrics['permission_needed'] = 'No (open source, local processing)'
    metrics['notes'] = 'Text and metadata via Tika.'
    return metrics

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python extractor.py <file_path>')
        sys.exit(1)
    file_path = sys.argv[1]
    result = extract_tika(file_path)
    summary = summarize_extraction(result)
    metrics = get_metrics(summary, result, file_path)
    print('Extraction Summary:')
    print(json.dumps(metrics, indent=2))
    print('\nExtracted Data:')
    print(json.dumps(result, indent=2))

    output_folder = 'extracted'
    os.makedirs(output_folder, exist_ok=True)
    input_base = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_folder, f'{input_base}_tika.json')

    output = {
        'metrics': metrics,
        'summary': summary,
        'extracted_data': result
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f'\nExtraction results saved to {output_path}')
