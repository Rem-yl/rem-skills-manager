#!/usr/bin/env python3
"""
Extract content from EPUB, PDF, or Markdown book files.

Usage:
    extract_content.py <book_file> --output <output.json> [--format epub|pdf|markdown]

Output:
    JSON file with metadata, chapters, and structure
"""

import argparse
import json
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.epub_parser import extract_epub
from utils.pdf_parser import extract_pdf
from utils.markdown_parser import extract_markdown


def detect_format(file_path: Path) -> str:
    """Auto-detect file format from extension."""
    suffix = file_path.suffix.lower()
    if suffix == '.epub':
        return 'epub'
    elif suffix == '.pdf':
        return 'pdf'
    elif suffix in ['.md', '.markdown']:
        return 'markdown'
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract content from EPUB, PDF, or Markdown book files'
    )
    parser.add_argument('book_file', help='Path to book file')
    parser.add_argument('--output', required=True, help='Output JSON file')
    parser.add_argument('--format', choices=['epub', 'pdf', 'markdown'],
                       help='Force format (auto-detected if omitted)')
    args = parser.parse_args()

    book_path = Path(args.book_file)
    if not book_path.exists():
        print(f"Error: File not found: {book_path}")
        return 1

    # Detect format
    try:
        format_type = args.format or detect_format(book_path)
        print(f"Detected format: {format_type}")
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    # Extract content
    try:
        if format_type == 'epub':
            data = extract_epub(str(book_path))
        elif format_type == 'pdf':
            data = extract_pdf(str(book_path))
        elif format_type == 'markdown':
            data = extract_markdown(str(book_path))
        else:
            print(f"Error: Unknown format: {format_type}")
            return 1
    except Exception as e:
        print(f"Error extracting content: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Add metadata
    data['source_file'] = str(book_path)
    data['format'] = format_type

    # Save JSON
    output_path = Path(args.output)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing output: {e}")
        return 1

    print(f"\nExtraction complete!")
    print(f"  Chapters: {len(data['chapters'])}")
    print(f"  Total words: {sum(ch['word_count'] for ch in data['chapters'])}")
    print(f"  Saved to: {output_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
