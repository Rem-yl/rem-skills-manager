#!/usr/bin/env python3
"""
Generate AI-powered reading notes from book file or extracted JSON.

Usage:
    generate_notes.py <book_file_or_json> --output <notes.md> [options]

Options:
    --points-per-chapter INT   Number of key points per chapter (default: 6)
    --detail low|medium|high   Detail level (default: medium)
    --focus STRING            Custom focus area for summarization
    --audience STRING         Target audience for notes
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.summarizer import build_chapter_prompt, parse_chapter_response, identify_cross_references, call_claude_api


def call_claude(prompt: str) -> str:
    """
    Call Claude API via subprocess.

    In production, this should use the Anthropic SDK.
    For now, use a simple approach with stdin.
    """
    # For now, return the prompt for testing
    # In actual use, this would call Claude
    return f"[Note: Claude API call would happen here]\n\nPrompt:\n{prompt[:200]}..."


def main():
    parser = argparse.ArgumentParser(
        description='Generate AI-powered reading notes from book file or extracted JSON'
    )
    parser.add_argument('input_file', help='Book file or extracted JSON')
    parser.add_argument('--output', required=True, help='Output markdown file')
    parser.add_argument('--points-per-chapter', type=int, default=6,
                       help='Key points per chapter (default: 6)')
    parser.add_argument('--detail', choices=['low', 'medium', 'high'],
                       default='medium', help='Detail level')
    parser.add_argument('--focus', help='Custom focus area')
    parser.add_argument('--audience', help='Target audience')
    args = parser.parse_args()

    input_path = Path(args.input_file)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1

    # Check if input is JSON or book file
    if input_path.suffix == '.json':
        # Pre-extracted
        print("Loading extracted content...")
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # Need to extract first
        print("Extracting content...")
        temp_json = input_path.with_suffix('.extracted.json')
        result = subprocess.run([
            sys.executable,
            str(Path(__file__).parent / 'extract_content.py'),
            str(input_path),
            '--output', str(temp_json)
        ])
        if result.returncode != 0:
            print("Extraction failed")
            return 1

        with open(temp_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

    # Build book context
    book_context = {
        'title': data['metadata']['title'],
        'author': data['metadata']['author'],
        'total_chapters': len(data['chapters']),
    }

    print(f"\nBook: {book_context['title']}")
    print(f"Author: {book_context['author']}")
    print(f"Chapters: {book_context['total_chapters']}")

    # Generate cross-references
    print("\nAnalyzing chapter relationships...")
    cross_refs = identify_cross_references(data['chapters'])

    # Generate notes for each chapter
    print(f"\nGenerating notes for {len(data['chapters'])} chapters...")
    print("Using Claude API to generate summaries...\n")

    chapter_notes = []
    for i, chapter in enumerate(data['chapters']):
        print(f"  [{i+1}/{len(data['chapters'])}] Processing: {chapter['title']}")

        # Build prompt
        options = {
            'points_per_chapter': args.points_per_chapter,
            'detail': args.detail,
            'focus': args.focus or 'general understanding',
            'audience': args.audience or 'general readers',
        }

        prompt = build_chapter_prompt(chapter, book_context, options)

        # Call Claude API to generate summary
        try:
            response = call_claude_api(prompt)
        except ValueError as e:
            print(f"\nError: {e}")
            print("\nTo use AI generation, set your API key:")
            print("  export ANTHROPIC_API_KEY='your-key-here'")
            return 1
        except Exception as e:
            print(f"\nWarning: API call failed for chapter {chapter['number']}: {e}")
            print("Continuing with next chapter...")
            continue

        parsed = parse_chapter_response(response, chapter['title'], chapter['number'])
        chapter_notes.append(parsed)

    # Write markdown output
    output_path = Path(args.output)
    print(f"\nWriting output to: {output_path}")

    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"# {data['metadata']['title']}\n\n")
        f.write(f"**Author:** {data['metadata']['author']}\n")
        f.write(f"**Language:** {data['metadata'].get('language', 'Unknown')}\n")
        if data['metadata'].get('publisher'):
            f.write(f"**Publisher:** {data['metadata']['publisher']}\n")
        f.write("\n---\n\n")

        # Generate and write book overview
        f.write("## 书籍概览\n\n")

        # Create overview prompt
        print("\nGenerating book overview...")
        overview_prompt = f"""请用中文简要介绍这本书（2-3段）：

书名：《{data['metadata']['title']}》
作者：{data['metadata']['author']}

章节标题：
{chr(10).join([f"- {ch['title']}" for ch in data['chapters'][:10]])}
{"..." if len(data['chapters']) > 10 else ""}

包括：主题、论点、涵盖领域。"""

        try:
            overview = call_claude_api(overview_prompt)
            f.write(overview)
            f.write("\n\n---\n\n")
        except Exception as e:
            print(f"Warning: Could not generate overview: {e}")
            f.write(f"This book contains {len(data['chapters'])} chapters.\n\n---\n\n")

        # Write chapter notes
        f.write("## 读书笔记\n\n")
        for note in chapter_notes:
            f.write(note['markdown'])
            f.write("\n---\n\n")

        # Write footer
        f.write(f"\n**Generated by book-notes-extractor**\n")
        f.write(f"**Source:** {data['source_file']}\n")
        f.write(f"**Settings:** {args.points_per_chapter} points per chapter, {args.detail} detail level\n")

    print(f"\nNotes generated successfully!")
    print(f"Output: {output_path}")
    print(f"Total chapters: {len(chapter_notes)}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
