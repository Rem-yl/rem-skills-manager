---
name: paper-summary
description: Summarize academic research papers from markdown files across six key dimensions (problem, approach, method, experimental design, methodology, results). Use when user asks to "summarize this paper", "analyze this research paper", "extract key insights", "create a digest", "what's the main contribution", or "explain the methodology" for .md files containing academic papers. Preserves all LaTeX formulas and image references.
---

# Paper Summary Skill

Analyze academic research papers from markdown files and generate structured summaries across six key analytical dimensions. This skill produces well-organized markdown summaries with preserved mathematical notation and images.

## When to Use This Skill

Use this skill when the user wants to:
- Summarize an academic paper from a markdown file
- Analyze a research paper's methodology or results
- Extract key insights or contributions
- Get a quick digest of a paper
- Understand the experimental design
- Compare approaches across papers

**Trigger phrases:**
- "Summarize this paper: paper.md"
- "Analyze this research paper: transformer.md"
- "Extract key insights from resnet.md"
- "Create a digest of this paper"
- "What's the main contribution of bert.md?"
- "Explain the methodology in attention-is-all-you-need.md"

## Input Requirements

- **File path**: Absolute or relative path to a markdown file
- **File content**: Should contain academic paper content (abstract, introduction, methods, results, etc.)
- **Detail level** (optional): Brief, Standard, or Detailed
  - If not specified, ask the user to choose
  - Standard is the default recommendation

## Detail Levels

### Brief (500-800 words)
- 2-3 sentences per main section
- Emphasize problem statement and core contribution
- Include only the most important formulas
- Summary tables only (no exhaustive details)
- **Use case**: Quick scan, literature review, deciding whether to read full paper

### Standard (1200-1800 words) - DEFAULT
- 1 paragraph per main section
- Balanced coverage of all six dimensions
- Important derivations and key equations
- Key results tables and main datasets
- **Use case**: General understanding, seminar prep, reference for later work

### Detailed (2500-4000 words)
- 2-3 paragraphs per main section with subsections
- Comprehensive analysis of all dimensions
- Full mathematical formulation
- All tables, datasets, baselines, ablation studies
- **Use case**: Deep analysis, implementation planning, paper review, PhD reading

## Analysis Framework: Six Dimensions

Every summary must analyze the paper across these dimensions:

### 1. Problem Statement
What problem does the paper address? Why is it important? What are the limitations of existing solutions?

### 2. Solution Approach
What is the high-level approach to solving the problem? What's the core idea or insight?

### 3. Proposed Method
How does the method work? What are the technical components, architecture, or algorithm details?

### 4. Experimental Design
What datasets, baselines, and evaluation metrics are used? How are experiments structured?

### 5. Experimental Methodology
How are experiments conducted? What are the implementation details, hyperparameters, and training procedures?

### 6. Experimental Results
What are the main findings? How does the proposed method compare to baselines? What insights emerge from ablation studies?

## Formula Preservation - CRITICAL

**Preserving LaTeX formulas is critical for technical papers.** All mathematical notation must remain exactly as it appears in the input.

**Rules:**
- Preserve all inline formulas: `$...$`
- Preserve all display formulas: `$$...$$`
- Do NOT convert formulas to plain text
- Do NOT simplify notation
- Do NOT change whitespace within formulas
- Keep backslashes, subscripts, superscripts, Greek letters, special symbols exactly as written

**Example preservation:**
- Input: `$\mathcal{L} = -\sum_{i=1}^{N} \log p(y_i | x_i; \theta)$`
- Output: Same exact string (no changes)

**Why this matters**: Mathematical notation is precise and unambiguous. Converting to text loses information. Many tools render LaTeX natively (Obsidian, Notion, GitHub, Jupyter).

## Image References

Preserve all image references with original paths:
- Keep `![caption](path)` syntax intact
- Do not modify paths
- Include images in the output structure where relevant
- Note if images are referenced but context is unclear

## Structure Requirements

The output summary must use:
- **H2 headers** (`##`) for main sections (Problem Statement, Solution Approach, etc.)
- **H3 headers** (`###`) for subsections (e.g., Architecture, Mathematical Formulation)
- **Bullet points** for lists (findings, contributions, limitations)
- **Tables** for datasets, baselines, results (markdown table format)
- **Blockquotes** (`>`) for key quotes or important notes
- **Horizontal rules** (`---`) to separate major sections
- **Code blocks** for formulas (````math` or `$$...$$`)

See `references/output-template.md` for the complete structure template.

## Workflow

Follow these steps when executing this skill:

### Step 1: Read the Paper
Use the Read tool to load the markdown file. If the file path is invalid or file doesn't exist, inform the user and ask for the correct path.

### Step 2: Determine Detail Level
If the user hasn't specified a detail level:
- Ask: "What level of detail would you like? Brief (~600 words), Standard (~1500 words), or Detailed (~3500 words)?"
- Recommend Standard as the default for most use cases

### Step 3: Analyze Content
Extract information for all six dimensions from the paper:
- Read abstract, introduction for problem statement and approach
- Read methods section for proposed method details
- Read experimental setup for design
- Read implementation details for methodology
- Read results/discussion for findings

### Step 4: Generate Summary
Follow the structure in `references/output-template.md`:
- Title block with metadata
- One-sentence abstract
- Six main sections (## 1-6) with appropriate subsections
- Tables for datasets/baselines/results (detail level determines which tables)
- Formula blocks where relevant
- Limitations & Future Work
- Key Takeaways (3-5 bullets)

### Step 5: Preserve Notation
Verify that all LaTeX formulas and image references are preserved exactly:
- Use Read tool on output before finalizing if needed
- Check that `$...$` and `$$...$$` blocks are unchanged
- Verify image paths are intact

### Step 6: Format Output
Return the markdown summary directly to the user. Do NOT save to a file unless explicitly requested.

### Step 7: Handle Edge Cases
- **Missing sections**: Note what's absent (e.g., "Paper lacks explicit experimental methodology section")
- **Non-academic content**: Politely decline and explain this skill is for research papers
- **Multiple papers**: Process one at a time, suggest batch processing if needed
- **PDF input**: Suggest converting to markdown first (recommend tools like `pdf2md` or `pandoc`)

## Edge Cases

### Missing Sections in Paper
If the paper doesn't have all six dimensions clearly stated:
- Note what's missing in the relevant section
- Infer from context if reasonable
- Example: "The paper doesn't explicitly state limitations, but based on the experimental results, potential limitations include..."

### Non-Academic Content
If the input file is not an academic paper (blog post, tutorial, documentation):
- Politely decline: "This skill is designed for academic research papers. The provided file appears to be [type]. Would you like me to summarize it using general-purpose summarization instead?"

### PDF Input
If the user provides a PDF file:
- Respond: "This skill works with markdown files. Please convert the PDF to markdown first. You can use tools like:\n  - `pandoc paper.pdf -o paper.md`\n  - Online converters (pdf2md.com)\n  - Claude Code's pdf skill: /pdf extract paper.pdf > paper.md\n\nOnce converted, I can summarize the markdown file."

### Multiple Papers
If the user wants to summarize multiple papers:
- Process one at a time
- Ask: "I'll process these one by one. Should I start with [first paper]?"
- Suggest creating a comparison table if user wants comparative analysis

## Example Invocations

### Example 1: Standard Summary
**User**: "Summarize this paper: ~/papers/attention-is-all-you-need.md"

**Action**:
1. Read `~/papers/attention-is-all-you-need.md`
2. Ask: "What level of detail? Brief/Standard/Detailed? (Recommend Standard)"
3. User: "Standard"
4. Generate 1200-1800 word summary with all six sections
5. Preserve all transformer architecture formulas
6. Include key results tables
7. Return markdown summary

### Example 2: Brief Summary with Specific Focus
**User**: "Give me a brief summary of resnet.md, I just need the main ideas"

**Action**:
1. Read `resnet.md`
2. Detect "brief" → use Brief detail level (no need to ask)
3. Generate 500-800 word summary
4. Emphasize sections 1, 2, 3 (problem, approach, method)
5. Include only the core residual connection formula
6. Return concise markdown summary

### Example 3: Detailed Analysis
**User**: "I need a comprehensive analysis of bert.md, especially the experimental design"

**Action**:
1. Read `bert.md`
2. Detect "comprehensive" → use Detailed level
3. Generate 2500-4000 word summary
4. Emphasize sections 4, 5, 6 (experimental design, methodology, results)
5. Include all datasets, baselines, hyperparameters
6. Preserve all BERT model formulas
7. Include all ablation study tables
8. Return detailed markdown summary

## Tips for Best Results

1. **Verify file path**: Use tab completion or `ls` to confirm path before invoking
2. **Specify detail level early**: Save time by including it in the initial request
3. **Check formula rendering**: If output will be viewed in a tool that doesn't render LaTeX, mention it upfront
4. **Request specific focus**: "Focus on the methodology" → Emphasize sections 3, 5
5. **Multiple papers**: Create a folder with all papers, process batch-style
6. **Custom structure**: If user needs non-standard structure, clarify before starting

## References

For detailed output structure and template examples, read:
- `references/output-template.md` - Complete markdown structure template with examples
