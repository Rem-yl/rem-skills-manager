#!/usr/bin/env python3
"""
PDF parsing utility for extracting book content.

Note: Only supports text-based PDFs. Scanned PDFs require OCR preprocessing.
"""

import re
from typing import Dict, List
import fitz  # PyMuPDF


def detect_chapters_with_regex(text: str) -> List[Dict]:
    """
    Detect chapter boundaries using common patterns.

    Looks for patterns like:
    - "Chapter 1: Title"
    - "CHAPTER ONE"
    - "第一章 标题" (Chinese)
    - "1. Title" at start of line
    """
    chapters = []

    # Patterns for chapter detection
    patterns = [
        r'^Chapter\s+(\d+|[IVX]+)[:\s]+(.*?)$',  # Chapter 1: Title
        r'^CHAPTER\s+(\d+|[IVX]+)[:\s]*(.*?)$',  # CHAPTER 1
        r'^第([一二三四五六七八九十百千万\d]+)章[：:\s]+(.*?)$',  # 第一章: 标题
        r'^(\d+)\.\s+([A-Z].*?)$',  # 1. Title (capitalized)
    ]

    lines = text.split('\n')
    current_chapter = None
    chapter_num = 0

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Check each pattern
        for pattern in patterns:
            match = re.match(pattern, line_stripped, re.IGNORECASE)
            if match:
                # Save previous chapter if exists
                if current_chapter:
                    chapters.append(current_chapter)

                # Start new chapter
                chapter_num += 1
                groups = match.groups()

                if len(groups) >= 2:
                    title = groups[1].strip() or f'Chapter {chapter_num}'
                else:
                    title = f'Chapter {chapter_num}'

                current_chapter = {
                    'id': f'chapter_{chapter_num}',
                    'number': chapter_num,
                    'title': title,
                    'level': 1,
                    'content': '',
                    'images': [],
                    'formulas': [],
                    'word_count': 0,
                }
                break
        else:
            # No match - add to current chapter content
            if current_chapter:
                current_chapter['content'] += line + '\n'

    # Add final chapter
    if current_chapter:
        current_chapter['content'] = current_chapter['content'].strip()
        current_chapter['word_count'] = len(current_chapter['content'].split())
        chapters.append(current_chapter)

    return chapters


def extract_pdf(file_path: str) -> Dict:
    """
    Extract content from text-based PDF.

    Args:
        file_path: Path to PDF file

    Returns:
        Dictionary with metadata and chapters
    """
    doc = fitz.open(file_path)

    # Extract metadata
    metadata = {
        'title': doc.metadata.get('title', 'Unknown'),
        'author': doc.metadata.get('author', 'Unknown'),
        'language': 'en',  # No language in PDF metadata usually
        'publisher': '',
        'isbn': '',
        'page_count': doc.page_count,
    }

    # Extract full text
    full_text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        full_text += page.get_text()

    # Detect chapters
    chapters = detect_chapters_with_regex(full_text)

    # If no chapters detected, treat entire document as one chapter
    if not chapters:
        chapters = [{
            'id': 'full_document',
            'number': 1,
            'title': metadata['title'],
            'level': 1,
            'content': full_text.strip(),
            'images': [],
            'formulas': [],
            'word_count': len(full_text.split()),
        }]

    doc.close()

    return {
        'metadata': metadata,
        'chapters': chapters,
        'toc': [],  # PDF TOC extraction is complex, skip for now
    }
