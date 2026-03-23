#!/usr/bin/env python3
"""
EPUB parsing utility for extracting book content.

Extracts metadata, chapter structure, text content, images, and LaTeX formulas.
"""

import re
from typing import Dict, List, Optional
from ebooklib import epub
import bs4


def extract_formulas(text: str) -> List[str]:
    """Extract LaTeX formulas from text."""
    formulas = []

    # Match $$...$$ (display math)
    display_math = re.findall(r'\$\$(.+?)\$\$', text, re.DOTALL)
    formulas.extend([f'$${f}$$' for f in display_math])

    # Match $...$ (inline math)
    inline_math = re.findall(r'(?<!\$)\$(?!\$)(.+?)\$(?!\$)', text)
    formulas.extend([f'${f}$' for f in inline_math])

    return formulas


def extract_title_from_html(soup: bs4.BeautifulSoup) -> str:
    """Extract chapter title from HTML content."""
    # Try common heading tags
    for tag in ['h1', 'h2', 'h3', 'title']:
        heading = soup.find(tag)
        if heading:
            return heading.get_text().strip()

    # Fallback to first paragraph if no heading found
    first_p = soup.find('p')
    if first_p:
        text = first_p.get_text().strip()
        # Use first line/sentence as title
        return text.split('\n')[0][:100]

    return 'Untitled Chapter'


def extract_epub(file_path: str) -> Dict:
    """
    Extract content from EPUB file.

    Args:
        file_path: Path to EPUB file

    Returns:
        Dictionary with:
        - metadata: book metadata (title, author, language, etc.)
        - chapters: list of chapter dictionaries
        - toc: table of contents structure
    """
    book = epub.read_epub(file_path)

    # Extract metadata
    metadata = {
        'title': book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else 'Unknown',
        'author': book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else 'Unknown',
        'language': book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else 'en',
        'publisher': book.get_metadata('DC', 'publisher')[0][0] if book.get_metadata('DC', 'publisher') else '',
        'isbn': book.get_metadata('DC', 'identifier')[0][0] if book.get_metadata('DC', 'identifier') else '',
    }

    # Extract chapters
    chapters = []
    chapter_num = 0

    for item in book.get_items_of_type(9):  # ITEM_DOCUMENT (HTML documents)
        try:
            content_bytes = item.get_content()
            html = content_bytes.decode('utf-8', errors='ignore')
            soup = bs4.BeautifulSoup(html, 'html.parser')

            # Get text content
            text = soup.get_text()

            # Skip empty or very short chapters (likely cover/title pages)
            if len(text.strip()) < 100:
                continue

            # Extract title
            title = extract_title_from_html(soup)

            # Detect formulas
            formulas = extract_formulas(text)

            # Extract images
            images = []
            for img in soup.find_all('img'):
                images.append({
                    'src': img.get('src', ''),
                    'alt': img.get('alt', ''),
                })

            chapter_num += 1
            chapters.append({
                'id': item.get_name(),
                'number': chapter_num,
                'title': title,
                'level': 1,  # Default level, can be refined with TOC
                'content': text.strip(),
                'images': images,
                'formulas': formulas,
                'word_count': len(text.split()),
            })

        except Exception as e:
            print(f"Warning: Failed to parse chapter {item.get_name()}: {e}")
            continue

    # Extract table of contents
    toc = []
    try:
        for toc_item in book.toc:
            if isinstance(toc_item, tuple):
                # Nested TOC structure
                section, children = toc_item
                toc.append({
                    'title': section.title,
                    'href': section.href,
                    'children': [{'title': c.title, 'href': c.href} for c in children]
                })
            else:
                # Flat TOC
                toc.append({
                    'title': toc_item.title,
                    'href': toc_item.href,
                })
    except Exception as e:
        print(f"Warning: Failed to parse TOC: {e}")

    return {
        'metadata': metadata,
        'chapters': chapters,
        'toc': toc,
    }
