# Rem's Claude Code Skills

Personal collection of productivity skills for Claude Code.

## Skills Included

### 📚 book-notes-extractor
Extract structured reading notes from EPUB, PDF, and Markdown books with chapter-organized summaries.

### 📊 code-visualize
Generate architecture diagrams, sequence diagrams, flowcharts using Mermaid syntax.

### 📄 paper-summary
Summarize academic research papers across six key dimensions (problem, approach, method, results).

### ✨ refining-prompts
Transform vague requests into clear, structured prompts using the 5C Framework.

### 🧹 repo-simplifier
Simplify repositories by removing duplicates, consolidating docs, cleaning up tests.

### 🧪 tdd-feature-development
Guide rigorous feature development with TDD workflow and quality standards.

### 🌏 translate-pdf-to-markdown
Translate English PDF academic papers to Chinese Markdown with LaTeX formulas preserved.

### 🔄 retro
Session retrospective — distill lessons and decisions, persist to project memory. Use at the end of a work session.

## Installation

### From GitHub
```bash
# In Claude Code
/plugin marketplace add Rem-yl/rem-skills-manager
/plugin install rem-skills@rem-marketplace
```

### Local Development
```bash
# Clone this repository
git clone https://github.com/Rem-yl/rem-skills-manager.git
cd rem-skills-manager

# In Claude Code, add local marketplace
/plugin marketplace add /Users/yule/workspace/skills-manager
/plugin install rem-skills@rem-marketplace
```

## Requirements

Some skills have Python package dependencies:
- **book-notes-extractor**: ebooklib, beautifulsoup4, lxml, PyMuPDF, markdown-it-py, pyyaml, anthropic[vertex]

Install as needed when Claude prompts you.

## License

Personal use.
