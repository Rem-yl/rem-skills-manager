#!/usr/bin/env python3
"""
Markdown parsing utility for extracting book content.

Uses headings (#, ##, ###) to detect chapter structure.
"""

import re
from typing import Dict, List
import yaml


def extract_markdown(file_path: str) -> Dict:
    """
    Extract content from Markdown file.

    Args:
        file_path: Path to Markdown file

    Returns:
        Dictionary with metadata and chapters
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse YAML frontmatter if present
    metadata = {}
    markdown_content = content

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
                markdown_content = parts[2]
            except yaml.YAMLError as e:
                print(f"Warning: Failed to parse YAML frontmatter: {e}")
                metadata = {}
        else:
            metadata = {}

    # Extract metadata
    final_metadata = {
        'title': metadata.get('title', 'Unknown'),
        'author': metadata.get('author', 'Unknown'),
        'language': metadata.get('language', 'en'),
        'publisher': metadata.get('publisher', ''),
        'isbn': metadata.get('isbn', ''),
    }

    # Parse markdown structure using headings
    chapters = []
    lines = markdown_content.split('\n')

    current_chapter = None
    chapter_num = 0

    for line in lines:
        # Check for headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)

        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()

            # Level 1 and 2 headings become chapters
            if level <= 2:
                # Save previous chapter
                if current_chapter:
                    current_chapter['content'] = current_chapter['content'].strip()
                    current_chapter['word_count'] = len(current_chapter['content'].split())
                    chapters.append(current_chapter)

                # Start new chapter
                chapter_num += 1
                current_chapter = {
                    'id': f'chapter_{chapter_num}',
                    'number': chapter_num,
                    'title': title,
                    'level': level,
                    'content': '',
                    'images': [],
                    'formulas': [],
                    'word_count': 0,
                }
            else:
                # Level 3+ headings are part of current chapter content
                if current_chapter:
                    current_chapter['content'] += line + '\n'
        else:
            # Regular content
            if current_chapter:
                current_chapter['content'] += line + '\n'

                # Detect images
                img_matches = re.findall(r'!\[([^\]]*)\]\(([^\)]+)\)', line)
                for alt, src in img_matches:
                    current_chapter['images'].append({
                        'src': src,
                        'alt': alt,
                    })

                # Detect formulas
                formula_matches = re.findall(r'\$\$(.+?)\$\$|\$(.+?)\$', line)
                for match in formula_matches:
                    formula = match[0] if match[0] else match[1]
                    if formula:
                        current_chapter['formulas'].append(formula)

    # Add final chapter
    if current_chapter:
        current_chapter['content'] = current_chapter['content'].strip()
        current_chapter['word_count'] = len(current_chapter['content'].split())
        chapters.append(current_chapter)

    return {
        'metadata': final_metadata,
        'chapters': chapters,
        'toc': [],  # Could build from heading structure if needed
    }
