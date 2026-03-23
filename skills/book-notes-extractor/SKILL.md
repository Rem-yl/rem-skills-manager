---
name: book-notes-extractor
description: Extract structured reading notes from books (EPUB, PDF, Markdown). Generates chapter-organized summaries with 5-8 key points per chapter, theme-based organization, cross-references, and importance ratings. Use when users want to "summarize this book", "create reading notes", "extract key insights from [book file]", or provide .epub/.pdf/.md book files. Automatically handles Chinese and English text.
metadata:
  openclaw:
    emoji: "📚"
    requires:
      python_packages:
        - ebooklib
        - beautifulsoup4
        - lxml
        - PyMuPDF
        - markdown-it-py
        - pyyaml
        - anthropic[vertex]
---

# Book Notes Extractor

Extract AI-powered reading notes from EPUB, PDF, and Markdown books.

## When to use

- User asks to "summarize this book" or "create reading notes from [file]"
- User provides EPUB, PDF, or Markdown book files
- User wants structured notes organized by chapters and themes
- User mentions "reading notes", "book summary", "extract insights"

## Quick start

Basic usage:
```bash
python {baseDir}/scripts/generate_notes.py /path/to/book.epub --output notes.md
```

## Workflow

1. **Detect format**: Auto-detects EPUB/PDF/Markdown from file extension
2. **Extract content**: Parses book structure, chapters, metadata
3. **Generate notes**: Uses Claude to create themed summaries with cross-references

## Format support

- **EPUB** (priority): Full support with chapter hierarchy extraction
- **Markdown**: Native support, uses headings for structure
- **PDF**: Text-based PDFs only (no OCR for scanned pages)

## Output structure

Generated notes use **深层级 Markdown 列表格式** (Deep hierarchical Markdown list format):

### Features
- ✓ 纯要点列表，无结构化标签 (Pure bullet points, no structured labels)
- ✓ 使用 `-` 符号 + 缩进（2空格）表示层级 (Uses `-` symbol + 2-space indentation for hierarchy)
- ✓ **4-5层深度**的递进式结构 (4-5 level depth with progressive structure)
- ✓ 从概念→解释→细节→例证→补充的层级展开 (Hierarchy flows: concept → explanation → details → examples → supplements)
- ✓ 每个要点简洁明了 (Each point is concise and clear)
- ✓ 完全使用中文 (Fully Chinese output)
- ✓ 保留公式（LaTeX 格式）(Preserves formulas in LaTeX format)
- ✓ 按逻辑组织，不按时间顺序 (Organized by logic, not chronologically)

### Example output

```markdown
## 第3章：统一性的消失

- 统一时间的消失
  - 牛顿力学的绝对时间观
    - 牛顿对绝对时间的描述
      - 绝对的、真实的和数学的时间，由其特性决定，自身均匀流逝
      - 牛顿力学宣扬存在一个超脱于物质和空间之外的背景：时间
    - 牛顿方程中时间变量`t`的含义
      - 在经典力学框架中，`t`用于表示时间的流逝
      - 告诉我们随着钟表测量的时间，事物如何改变
      - 这个`t`被假定为全宇宙统一的
  - 广义相对论对绝对时间的否定
    - 相对时空观的核心原理
      - 不存在全宇宙统一的"绝对时间"
      - 每个观察者都有自己的"固有时"
    - 时间测量的相对性
      - 不同观察者处在不同引力场中
      - 不同观察者处于不同运动状态
      - 对同一事件的时间测量结果可以不同
        - 接近大质量物体的时间流逝更慢
        - 高速运动的物体时间膨胀效应
  - 统一时间概念的彻底崩溃
    - 根据广义相对论，时间失去了统一性
    - 时间成为局部性、相对性的物理量
```

**注意层级深度：**
- 示例展示了5层深度（从顶层"统一时间的消失"到最深的"时间膨胀效应"）
- 复杂概念充分展开，不停留在浅层
- 递进式深入：概念→解释→细节→具体例子

See `references/output-format.md` for detailed examples.

## Advanced options

### Two-phase workflow

Separate extraction and generation for inspection:

```bash
# Phase 1: Extract content for inspection
python {baseDir}/scripts/extract_content.py book.epub --output book.json

# Phase 2: Review structure, then generate
python {baseDir}/scripts/generate_notes.py book.json --output notes.md
```

### Custom detail level

```bash
python {baseDir}/scripts/generate_notes.py book.epub \
  --output notes.md \
  --points-per-chapter 8 \
  --detail high \
  --focus "leadership principles" \
  --audience "software engineers"
```

### Options

- `--points-per-chapter INT`: Number of key points per chapter (default: 6)
- `--detail low|medium|high`: Detail level (default: medium)
- `--focus STRING`: Custom focus area for summarization
- `--audience STRING`: Target audience for notes

## Examples

Extract notes from Chinese EPUB:
```bash
python {baseDir}/scripts/generate_notes.py 乌合之众.epub \
  --output 乌合之众_notes.md \
  --points-per-chapter 6 \
  --focus "group psychology and leadership"
```

Process PDF with custom settings:
```bash
python {baseDir}/scripts/generate_notes.py technical_book.pdf \
  --output notes.md \
  --points-per-chapter 8 \
  --detail high \
  --audience "software developers"
```

Two-phase workflow for large books:
```bash
# Extract and inspect structure
python {baseDir}/scripts/extract_content.py large_book.epub --output book.json
cat book.json | jq '.chapters[] | {number, title, word_count}'

# Generate notes after review
python {baseDir}/scripts/generate_notes.py book.json --output notes.md
```

## Dependencies

Required Python packages:
```bash
pip install ebooklib beautifulsoup4 lxml PyMuPDF markdown-it-py pyyaml anthropic[vertex]
```

**API Configuration:**

The skill requires Claude API access for generating summaries. Two options:

1. **Direct API** (recommended for most users):
   ```bash
   export ANTHROPIC_API_KEY='your-key-here'
   ```

2. **Vertex AI** (for Google Cloud users):
   ```bash
   export ANTHROPIC_VERTEX_PROJECT_ID='your-project-id'
   export CLAUDE_CODE_USE_VERTEX=1
   ```

Get your API key at: https://console.anthropic.com/

## Implementation notes

### Content extraction

- **EPUB**: Uses `ebooklib` to read EPUB structure, `BeautifulSoup` for HTML parsing
- **PDF**: Uses `PyMuPDF` (fitz) for text extraction, regex patterns for chapter detection
- **Markdown**: Uses `markdown-it-py` for parsing, heading levels define chapter structure

### Chapter detection

- EPUB: Uses document items and TOC structure
- PDF: Regex patterns for "Chapter N", "第X章", etc.
- Markdown: Heading levels (# and ## become chapters)

### Cross-references

Uses keyword similarity (Jaccard similarity) to identify related chapters. Chapters with >15% keyword overlap are considered related.

### Formula preservation

Detects and preserves LaTeX formulas in `$...$` (inline) and `$$...$$` (display) notation.

### AI generation

- Uses Claude API (Sonnet 4.5) to generate chapter summaries
- Supports both direct Anthropic API and Vertex AI
- Each chapter summary includes: 2-3 sentence overview, theme-organized key points, concrete examples, cross-references, and importance ratings
- Book overview generated separately based on chapter titles and metadata
- API calls are made sequentially (one per chapter) to avoid rate limits

## Limitations

- PDF support is limited to text-based PDFs; scanned images require OCR preprocessing
- Very long chapters (>8000 characters) are truncated in the prompt
- Cross-reference detection is keyword-based and may miss conceptual relationships
- Processing time increases linearly with number of chapters (~3-5 seconds per chapter)

## Troubleshooting

### EPUB extraction fails

Check file is valid EPUB:
```bash
python {baseDir}/scripts/extract_content.py book.epub --output test.json
cat test.json | jq '.metadata'
```

### Chinese text garbled

Ensure UTF-8 encoding:
```bash
file -I book.epub  # Should show charset=utf-8
```

### No chapters detected in PDF

Try manual chapter markers or convert to Markdown first:
```bash
pandoc book.pdf -o book.md
python {baseDir}/scripts/generate_notes.py book.md --output notes.md
```

## Resources

### scripts/

Executable Python scripts for content extraction and note generation:

- `extract_content.py` - Main content extraction script (auto-detects format)
- `generate_notes.py` - Note generation orchestrator
- `utils/epub_parser.py` - EPUB parsing logic
- `utils/pdf_parser.py` - PDF parsing logic
- `utils/markdown_parser.py` - Markdown parsing logic
- `utils/summarizer.py` - AI prompt building and response parsing

### references/

- `output-format.md` - Detailed output format examples and templates

## Technical details

### JSON intermediate format

The `extract_content.py` script outputs JSON with this structure:

```json
{
  "metadata": {
    "title": "Book Title",
    "author": "Author Name",
    "language": "zh",
    "publisher": "Publisher",
    "isbn": "123-456"
  },
  "chapters": [
    {
      "id": "chapter_1",
      "number": 1,
      "title": "Chapter Title",
      "level": 1,
      "content": "Full text content...",
      "images": [...],
      "formulas": [...],
      "word_count": 1234
    }
  ],
  "toc": [...],
  "source_file": "/path/to/book.epub",
  "format": "epub"
}
```

This allows inspection and debugging between extraction and generation phases.
