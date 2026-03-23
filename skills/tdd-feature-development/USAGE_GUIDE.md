# TDD Feature Development Skill - Usage Guide

## Overview

The **tdd-feature-development** skill guides you through rigorous, test-driven development of new features with emphasis on code quality, documentation, and incremental commits.

**Best For:**
- Production codebases requiring high quality
- Teams committed to TDD methodology
- Long-term maintained projects
- Educational/learning contexts

**Not Recommended For:**
- Quick prototypes or throwaway code
- Bug fixes (use debugging skills instead)
- Simple refactoring tasks
- Tight deadlines with limited resources

## Installation

### Option 1: Install from Package File

```bash
# Copy the .skill file to your Claude skills directory
cp tdd-feature-development.skill ~/.claude/skills/

# Or use Claude Code's skill installation command
claude skill install tdd-feature-development.skill
```

### Option 2: Install from Directory

```bash
# Clone or copy the skill directory
cp -r /Users/yule/tdd-feature-development ~/.claude/skills/

# Claude Code will automatically discover it
```

## How to Use

### Automatic Triggering

The skill automatically triggers when you request feature development:

```
"Implement a rate limiting feature for our API"
"Add user authentication with JWT"
"Build a caching layer for database queries"
"Create a new module for file uploads"
```

### Manual Invocation

If you want to explicitly use the skill:

```
/tdd-feature-development

# Then provide your feature request
"I need to implement email validation for our registration form"
```

## What to Expect

### The Workflow

When you use this skill, Claude will:

1. **Understand Requirements**
   - Ask clarifying questions
   - Identify inputs, outputs, edge cases

2. **Break Down into Components**
   - Split feature into logical, testable parts
   - Each component is a self-contained unit

3. **For Each Component:**
   - ✅ Write comprehensive tests FIRST
   - ❌ Run tests (they should fail)
   - ✅ Implement the feature with types and docs
   - ✅ Run tests (they should pass)
   - 🔍 Invoke code review (mandatory)
   - 🎨 Format code
   - 📝 Create git commit

4. **Integration**
   - Test components working together
   - Final code review
   - Documentation

### Time and Token Costs

Based on evaluation results:

| Metric | With Skill | Without Skill | Difference |
|--------|------------|---------------|------------|
| **Quality Score** | 88.9% | 55.6% | +33.3 pp |
| **Time** | ~12 minutes | ~6 minutes | +100% |
| **Tokens** | ~70,000 | ~40,000 | +75% |
| **Commits** | 5-7 | 1-2 | +250% |
| **Test Coverage** | 94-97% | 56-95% | More consistent |

**Verdict**: Approximately **2x cost** for **60% better quality**

## Examples from Real Evaluations

### Example 1: Rate Limiting (Python/FastAPI)

**User Request:**
```
"I need to implement a rate limiting feature for our API.
It should limit requests to 100 per minute per user, using
a token bucket algorithm. We're using Python with FastAPI."
```

**What the Skill Delivered:**
- ✅ 5 incremental git commits showing TDD progression
- ✅ 39 passing tests with 94% coverage
- ✅ Complete type hints (mypy --strict passes)
- ✅ Comprehensive English docstrings
- ✅ Clean git history documenting development
- ✅ Working FastAPI integration with proper headers

**Files Created:**
- `token_bucket.py` - Core algorithm (129 lines, fully typed)
- `rate_limiter.py` - Per-user service (123 lines)
- `fastapi_rate_limit.py` - FastAPI integration (114 lines)
- `test_token_bucket.py` - 13 tests
- `test_rate_limiter.py` - 11 tests
- `test_fastapi_integration.py` - 10 tests
- `test_integration.py` - 5 end-to-end tests
- `README.md` - Comprehensive documentation

### Example 2: Input Validation (Go)

**User Request:**
```
"Add a new feature to validate user input for our registration form.
We need to check email format, password strength (min 8 chars,
must have uppercase, lowercase, number), and username uniqueness.
This is a Go project using the standard library."
```

**What the Skill Delivered:**
- ✅ 4 incremental commits per component
- ✅ 40 passing tests with 97% coverage
- ✅ Proper Go doc comments for all exported functions
- ✅ Thread-safe username store with sync.RWMutex
- ✅ Well-separated components (email, password, username validators)
- ✅ go fmt and go vet compliant

**Files Created:**
- `validator.go` - All validation logic (312 lines)
- `validator_test.go` - 40 table-driven tests (310 lines)
- `go.mod` - Module configuration

### Example 3: Caching Layer (TypeScript)

**User Request:**
```
"We need to build a caching layer for our database queries to
improve performance. The cache should support TTL (time-to-live),
handle cache invalidation, and work with our existing TypeScript/Node.js backend."
```

**What the Skill Delivered:**
- ✅ 7 incremental commits
- ✅ 46 passing tests with 96.8% coverage
- ✅ Full TypeScript strict mode compliance
- ✅ Comprehensive JSDoc for all public APIs
- ✅ Zero ESLint errors/warnings
- ✅ Pattern-based cache invalidation

**Files Created:**
- `src/cache.ts` - Core cache class (267 lines)
- `src/query-cache.ts` - High-level wrapper (196 lines)
- `src/index.ts` - Module exports
- `src/cache.test.ts` - 21 unit tests
- `src/query-cache.test.ts` - 14 unit tests
- `src/integration.test.ts` - 7 integration tests
- `package.json`, `tsconfig.json`, `jest.config.js`

## Tips for Best Results

### 1. Provide Clear Requirements

**Good:**
```
"Implement JWT authentication for our Express API.
Users should login with email/password, get a token valid for 24 hours,
and we need middleware to protect routes."
```

**Too Vague:**
```
"Add authentication"
```

### 2. Specify Your Stack

Always mention:
- Programming language
- Framework/libraries you're using
- Any constraints (e.g., "no external dependencies")

### 3. Trust the Process

- Don't skip steps (especially code review!)
- Let Claude write tests first
- Review the git history to see the TDD progression

### 4. Budget Appropriately

- Allow 2x the time compared to ad-hoc coding
- Expect higher token usage
- Plan accordingly for production features

## Language Support

### Python
- Type hints with mypy strict mode
- Google/NumPy-style docstrings
- pytest for testing
- black + isort formatting

### Go
- Standard library emphasis
- Go doc comments
- Table-driven tests
- go fmt + go vet

### TypeScript
- Strict mode compilation
- JSDoc comments
- Jest or Vitest
- Prettier + ESLint

### Other Languages

The skill adapts to other languages by applying the same principles:
- Use language-standard testing framework
- Strictest type system available
- Language-specific documentation conventions
- Standard formatters

## Troubleshooting

### "The skill seems to be skipping code review"

This was a bug in iteration 1. If you're using the latest version (with CHANGELOG.md showing iteration 2 fixes), code review should be mandatory. If it's still skipped:

1. Check that your Claude Code has access to the `superpowers:code-reviewer` skill
2. Verify the skill file includes the explicit "MANDATORY STEP" section
3. Try manually invoking: `/code-review` after implementation

### "Tests are taking too long"

The skill is optimized for quality, not speed. If time is critical:
- Consider using traditional development for prototypes
- Use this skill only for production-ready features
- Break very large features into smaller, incremental releases

### "I don't need all this rigor"

This skill is intentionally rigorous. For less formal development:
- Don't use this skill
- Use ad-hoc development or simpler skills
- Reserve TDD skill for critical production code

## Customization

### Adjusting the Workflow

The skill is designed to be opinionated. However, you can:

1. **Edit SKILL.md** to adjust:
   - Number of commits required
   - Documentation verbosity
   - Testing coverage thresholds

2. **Skip Certain Steps** (not recommended):
   - Edit the quality checklist
   - Remove formatting requirements
   - Adjust git commit frequency

3. **Add Language Support**:
   - Add new section to "Language-Specific Guidance"
   - Include testing framework, type system, formatters
   - Provide code examples

## Feedback and Improvement

This skill was evaluated against realistic scenarios with measurable results. If you find issues or have suggestions:

1. **Document the Issue**: What went wrong? What was expected?
2. **Provide Context**: Which language? What feature?
3. **Include Examples**: Code snippets, git logs, test results

The skill can be iteratively improved based on real usage patterns.

## Version History

- **v2.0** (2026-02-27): Fixed code review integration bug, made review mandatory
- **v1.0** (2026-02-27): Initial release with Python/Go/TypeScript support

## License

See LICENSE.txt in the skill directory.
