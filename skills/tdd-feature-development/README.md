# TDD Feature Development Skill

**A rigorous, quality-focused skill for developing new features using Test-Driven Development**

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)]()
[![Quality](https://img.shields.io/badge/quality%20score-88.9%25-brightgreen)]()
[![Languages](https://img.shields.io/badge/languages-Python%20%7C%20Go%20%7C%20TypeScript-blue)]()

## Quick Start

```bash
# Install the skill
claude skill install tdd-feature-development.skill

# Use it naturally
"Implement rate limiting for our API"
"Add email validation to the registration form"
"Build a caching layer for database queries"
```

The skill automatically triggers and guides you through professional TDD workflow.

## What This Skill Does

This skill enforces disciplined feature development:

1. ✅ **Tests First**: Write comprehensive tests before any implementation
2. 🔴 **Red Phase**: Run tests, verify they fail
3. ✅ **Implementation**: Write minimal code to make tests pass
4. 🟢 **Green Phase**: Run tests, verify they pass
5. 🔍 **Code Review**: Mandatory review via code-reviewer skill
6. 🎨 **Format Code**: Run language-specific formatters
7. 📝 **Git Commit**: Create clear, descriptive commits

## Results from Real Evaluations

We ran 6 comprehensive evaluations comparing code produced **with** vs **without** this skill:

| Metric | With Skill | Without Skill | Improvement |
|--------|------------|---------------|-------------|
| **Overall Quality** | 88.9% | 55.6% | **+33.3 pp** |
| **TDD Workflow** | 100% ✅ | 0% ❌ | **+100 pp** |
| **Code Formatting** | 100% ✅ | 0% ❌ | **+100 pp** |
| **Documentation** | 100% ✅ | 33% ⚠️ | **+67 pp** |
| **Test Coverage** | 94-97% | 56-95% | More consistent |
| **Git Commits** | 5-7 | 1-2 | **+250%** |
| **Time Cost** | 12.3 min | 6.2 min | +98.7% |
| **Token Cost** | 70,570 | 40,347 | +74.9% |

**Trade-off**: ~2x cost for ~60% better quality

## Supported Languages

### Fully Supported
- **Python** - Type hints, pytest, black/isort, mypy
- **Go** - Doc comments, go test, go fmt/vet
- **TypeScript** - Type annotations, Jest/Vitest, Prettier/ESLint

### Adaptable
The skill adapts to other languages by applying core TDD principles with language-appropriate tools.

## When to Use

### ✅ Recommended For:
- Production features requiring high quality
- Long-term maintained codebases
- Teams committed to TDD methodology
- Educational contexts (learning TDD)
- Features that will be reviewed/audited

### ❌ Not Recommended For:
- Quick prototypes or throwaway code
- Bug fixes (use debugging skills)
- Simple refactoring tasks
- Tight deadlines with limited resources
- Configuration changes

## What You Get

### Code Quality
- **Complete type annotations** - No `any` types, strict mode
- **Comprehensive documentation** - All public functions documented in English
- **Clean code** - Formatted with industry-standard tools
- **High test coverage** - Typically 90%+ coverage
- **Edge case handling** - Tests include boundary conditions and error cases

### Development Artifacts
- **Clean git history** - 5-7 commits showing TDD progression
- **Working tests** - Comprehensive test suites
- **Documentation** - README and inline comments
- **Type safety** - Full compile-time type checking

### Quality Assurance
- **Code review** - Automated review after each component
- **Continuous testing** - Tests run throughout development
- **Incremental commits** - Easy to review and rollback

## Real Example: Rate Limiting Feature

**Request:**
> "Implement rate limiting for our API using a token bucket algorithm. Python with FastAPI."

**Delivered:**
- 📁 3 implementation files (366 lines)
- 🧪 4 test files (723 lines, 39 tests, 94% coverage)
- 📚 README with examples (256 lines)
- 🔧 Working example application
- 📝 5 git commits showing TDD progression
- ✅ All tests passing, code formatted, fully typed

**Time:** 13.5 minutes | **Tokens:** 79,343

[See full example in USAGE_GUIDE.md]

## Installation

### From Package
```bash
# Download tdd-feature-development.skill
claude skill install tdd-feature-development.skill
```

### From Source
```bash
# Clone this repository
git clone <repo-url>

# Copy to Claude skills directory
cp -r tdd-feature-development ~/.claude/skills/
```

## Documentation

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Comprehensive usage guide with examples
- **[SKILL.md](SKILL.md)** - Full skill specification and workflow
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and bug fixes
- **[evals/](evals/)** - Evaluation test cases and results

## Evaluation Results

Full evaluation results available in:
- `/tdd-feature-development-workspace/iteration-1/`
- Benchmark: `benchmark.json`
- Analysis: `analysis.md`
- Interactive viewer: http://localhost:8765 (when running)

## Known Issues

### Fixed in v2.0:
- ✅ Code review integration (was broken, now mandatory)

### Current Limitations:
- ⚠️ Higher time/token cost (~2x) - inherent to rigorous TDD
- ⚠️ Best suited for production code, not prototypes

## Contributing

To improve this skill:

1. Test with your use cases
2. Document issues with examples
3. Suggest improvements to workflow
4. Add support for more languages

## Version History

- **v2.0** (2026-02-27) - Fixed code review bug, made it mandatory
- **v1.0** (2026-02-27) - Initial release

## License

See [LICENSE.txt](LICENSE.txt)

## Acknowledgments

Built using the [skill-creator](https://github.com/anthropics/skill-creator) framework and tested with rigorous evaluations across multiple languages and scenarios.

---

**Quality matters.** If you're building production features that need to last, this skill ensures they're built right the first time.
