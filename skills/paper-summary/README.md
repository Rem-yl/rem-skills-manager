# Paper Summary Skill

A Claude Code skill for summarizing academic research papers from markdown files across six key analytical dimensions.

## Quick Start

### Installation

1. Copy the `paper-summary` folder to your Claude Code skills directory:
   ```bash
   cp -r paper-summary ~/.claude/skills/
   ```

2. The skill will be automatically available in Claude Code.

### Basic Usage

**Standard summary (recommended):**
```
Summarize this paper: ~/papers/attention-is-all-you-need.md
```

**Brief summary (quick overview):**
```
Give me a brief summary of resnet.md
```

**Detailed analysis:**
```
I need a comprehensive analysis of bert.md, especially the experimental design
```

## Detail Levels

| Level | Word Count | Use Case | When to Use |
|-------|-----------|----------|-------------|
| **Brief** | 500-800 | Quick scan | Literature review, deciding whether to read full paper |
| **Standard** | 1200-1800 | General understanding | Seminar prep, reference for later work |
| **Detailed** | 2500-4000 | Deep analysis | Implementation planning, paper review, PhD reading |

## What Gets Analyzed

Every summary covers six dimensions:

1. **Problem Statement** - What problem? Why important?
2. **Solution Approach** - High-level approach and core insight
3. **Proposed Method** - Technical details, architecture, algorithms
4. **Experimental Design** - Datasets, baselines, metrics
5. **Experimental Methodology** - Implementation, hyperparameters, procedures
6. **Experimental Results** - Findings, comparisons, ablations

## Key Features

✅ **Preserves LaTeX formulas** - All `$...$` and `$$...$$` notation kept intact
✅ **Preserves image references** - All `![...](path)` links maintained
✅ **Structured output** - Clean markdown with headers, tables, bullets
✅ **Configurable detail** - Three levels for different use cases
✅ **Edge case handling** - Missing sections, non-academic content, PDFs

## Example Output Structure

```markdown
# [Paper Title]

**Authors**: [Author list]
**Venue**: [Conference/Journal, Year]
**Summary Level**: Standard

---

## Abstract (1 sentence)
[Core contribution and main result]

---

## 1. Problem Statement
[What problem, why important, limitations of existing work]

## 2. Solution Approach
[High-level approach, core insight, key differences]

## 3. Proposed Method
### 3.1 Architecture
[System/model architecture]

### 3.2 Mathematical Formulation
$$
\mathcal{L}(\theta) = -\sum_{i=1}^{N} \log p(y_i | x_i; \theta)
$$

## 4. Experimental Design
[Datasets, baselines, metrics in tables]

## 5. Experimental Methodology
[Implementation details, hyperparameters, training procedure]

## 6. Experimental Results
[Main results, ablations, error analysis in tables]

---

## Limitations & Future Work
[Identified limitations and future directions]

---

## Key Takeaways
- Main contribution 1
- Main contribution 2
- Main contribution 3
```

## Requirements

- **Input**: Markdown file containing academic paper content
- **Claude Code**: Latest version with skill support
- **Paper format**: Must contain typical academic sections (abstract, methods, results)

## Common Use Cases

### Literature Review
```
Give me brief summaries of:
- paper1.md
- paper2.md
- paper3.md
```

### Deep Dive for Implementation
```
I need a detailed analysis of transformer.md with focus on the architecture and training methodology
```

### Quick Reference
```
What's the main contribution of resnet.md?
```

### Comparative Analysis
```
Summarize bert.md and gpt.md in standard detail, then compare their approaches
```

## Tips for Best Results

1. **Use clear file paths**: `~/papers/filename.md` or absolute paths
2. **Specify detail level early**: Include "brief", "detailed", or "comprehensive" in your request
3. **Focus on specific sections**: "especially the experimental design" → emphasizes those sections
4. **Convert PDFs first**: Use `pandoc` or Claude Code's pdf skill to convert to markdown

## Converting PDFs to Markdown

If you have a PDF paper, convert it first:

```bash
# Using pandoc
pandoc paper.pdf -o paper.md

# Using Claude Code's pdf skill
/pdf extract paper.pdf > paper.md
```

Then summarize the markdown file:
```
Summarize this paper: paper.md
```

## Edge Cases

### Missing Sections
The skill will note what's missing and infer from context:
```
"The paper doesn't explicitly state limitations, but based on
experimental results, potential limitations include..."
```

### Non-Academic Content
The skill will politely decline and suggest alternatives:
```
"This skill is designed for academic research papers. The provided
file appears to be a blog post. Would you like me to summarize it
using general-purpose summarization instead?"
```

### Multiple Papers
Process one at a time, or request batch processing:
```
I'll process these one by one. Should I start with paper1.md?
```

## Skill Structure

```
paper-summary/
├── SKILL.md                      # Main skill definition
├── references/
│   └── output-template.md        # Output structure template
├── evals/
│   ├── evals.json               # Test cases
│   └── files/                   # Sample papers for testing
└── README.md                     # This file
```

## Testing

Run validation:
```bash
python /path/to/skill-creator/scripts/quick_validate.py paper-summary
```

Package for distribution:
```bash
python /path/to/skill-creator/scripts/package_skill.py paper-summary
```

## Contributing

Improvements welcome! Areas for enhancement:

- [ ] Domain-specific terminology glossaries (CV, NLP, RL)
- [ ] Multi-paper comparison mode
- [ ] Citation extraction and formatting
- [ ] Figure/table deep analysis
- [ ] Paper type detection (theoretical, empirical, survey)

## License

MIT License - Free to use and modify

## Credits

Created for Claude Code skill ecosystem.
Follows skill-creator best practices and patterns.

---

**Version**: 1.0.0
**Last Updated**: 2026-02-27
**Skill Name**: `paper-summary`
