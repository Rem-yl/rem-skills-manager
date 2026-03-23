---
name: repo-simplifier
description: Simplify repository code, documentation, and tests by removing duplicates, consolidating docs, eliminating redundant parameters, and cleaning up outdated tests while preserving functionality. Use this skill when users want to "clean up the codebase", "simplify the repository", "remove duplicate code", "consolidate documentation", "clean up command-line arguments", "reduce code complexity", "merge redundant functions", "streamline the project", "remove outdated tests", "simplify test files", or "clean up redundant tests". Also trigger for mentions of "repository bloat", "too many docs", "confusing documentation", "duplicate utilities", "unnecessary CLI flags", or "test cleanup".
---

# Repository Simplifier

A skill for systematically simplifying repositories by removing code duplication, consolidating documentation, eliminating redundant command-line parameters, and cleaning up outdated tests — all while preserving functionality through careful verification.

## Core Principles

**Safety First**: Always create a backup branch before making any changes. Every simplification must be verified to ensure functionality is preserved.

**Incremental Progress**: Make changes in small, logical commits. Each commit represents one type of simplification (e.g., "merge duplicate utility functions", "consolidate README"). This makes review easier and rollback safer.

**Evidence-Based Decisions**: Don't guess whether code is redundant — analyze usage, run tests, and verify behavior before removing anything.

**Preserve Functionality**: The goal is to simplify, not to change behavior. Tests should pass before and after. If functionality must change, explicitly document why and get user approval first.

## When to Use This Skill

This skill is specifically designed for:
- Codebases with obvious duplicate functions or utilities
- Projects with scattered, redundant documentation
- CLI tools with too many overlapping or unused flags
- Repositories that have grown organically and need consolidation
- Projects where maintainability is suffering due to complexity

## Workflow

### Phase 1: Analysis and Backup

**1. Create Backup Branch**

ALWAYS start by creating a backup branch:

```bash
git checkout -b backup-before-simplification-$(date +%Y%m%d-%H%M%S)
git checkout -
```

This ensures the user can easily return to the original state.

**2. Understand Repository Structure**

Analyze the repository to understand:
- Primary programming language(s) - focus on Python and Go
- Project structure and organization
- Documentation files (README, docs/, CONTRIBUTING, etc.)
- Entry points (main files, CLI interfaces)
- Test infrastructure
- Dependencies and build system

**3. Identify Simplification Opportunities**

Create four checklists:

**Code Duplication Checklist:**
- [ ] Duplicate utility functions across modules
- [ ] Similar logic in different files (copy-paste)
- [ ] Redundant helper functions
- [ ] Overlapping class implementations
- [ ] Duplicated constants or configurations

**Documentation Redundancy Checklist:**
- [ ] Information repeated in multiple files
- [ ] Outdated or conflicting documentation
- [ ] Scattered usage examples
- [ ] README vs docs/ overlap
- [ ] Missing or incomplete main README

**Command-Line Parameter Redundancy Checklist:**
- [ ] Flags that do nothing (dead code)
- [ ] Overlapping flags with same effect
- [ ] Flags with default values that are never changed
- [ ] Overly granular flags that could be consolidated
- [ ] Flags that contradict each other

**Test File Cleanup Checklist:**
- [ ] Duplicate test cases (identical logic)
- [ ] Tests for removed/deprecated code
- [ ] Outdated tests that no longer reflect current behavior
- [ ] Tests that always pass (non-discriminating)
- [ ] Overly specific tests covered by more general ones
- [ ] Tests with excessive setup duplicated across files

Present these checklists to the user and ask them to confirm priorities.

### Phase 2: Code Simplification

**For Python Projects:**

1. **Find Duplicate Functions**

Use AST analysis or grep to find similar function signatures:

```bash
# Find function definitions
grep -r "^def " --include="*.py" .

# Look for similar names
grep -r "def.*util\|def.*helper" --include="*.py" .
```

2. **Verify Usage Before Removal**

For each potential duplicate:
- Check where it's imported/called
- Verify the logic is truly identical (not just similar names)
- Run tests with one version removed to confirm equivalence

3. **Consolidate Strategically**

- Move shared utilities to a central `utils.py` or appropriate module
- Keep functions near where they're used if only one module needs them
- Document why the consolidated version is in its location

**For Go Projects:**

1. **Find Duplicate Functions**

```bash
# Find function definitions
grep -r "^func " --include="*.go" .

# Check for duplicate helper functions
grep -r "func.*Helper\|func.*Util" --include="*.go" .
```

2. **Check Package Organization**

Go encourages small, focused packages. Look for:
- Functions that could move to existing packages
- Duplicate implementations across packages
- Utility packages that overlap

3. **Preserve Interfaces**

Be extremely careful with exported functions (capitalized). Changing these may break external users.

**General Code Simplification Principles:**

- Prefer keeping one well-tested version over multiple untested versions
- Document the consolidation in code comments
- Update imports across the codebase
- Run tests after each consolidation

**Commit Strategy:**

Make one commit per logical consolidation:

```bash
git add <changed-files>
git commit -m "Consolidate duplicate <function-name> implementations

Merged 3 copies of similar logic into single implementation in <location>.
All existing tests pass. Previous locations: <list-them>."
```

### Phase 3: Documentation Simplification

**Goal**: Consolidate into a single, comprehensive README while preserving essential information.

**1. Inventory Current Documentation**

List all documentation files:
- README.md (or README.rst, README.txt)
- docs/ directory contents
- CONTRIBUTING.md, CHANGELOG.md
- Inline documentation in code
- Wiki or external docs (note but don't modify)

**2. Extract Essential Information**

For each doc file, identify:
- **Unique information** (not repeated elsewhere)
- **Outdated information** (contradicts code or other docs)
- **Redundant information** (duplicates README or other files)

**3. Create Comprehensive README Structure**

A good consolidated README should have:

```markdown
# Project Name

Brief description (1-2 sentences)

## Features

Key capabilities (bulleted list)

## Installation

Step-by-step setup instructions

## Quick Start

Minimal example to get running

## Usage

### Basic Usage
Common use cases with examples

### Advanced Features
More complex scenarios

### Command-Line Reference (if applicable)
Complete CLI documentation

## Configuration

How to configure the tool/library

## Development

### Setup Development Environment
### Running Tests
### Contributing Guidelines (if substantial, keep CONTRIBUTING.md separate)

## Architecture (optional, if complex project)

High-level overview of structure

## FAQ / Troubleshooting

Common issues and solutions

## License

## Changelog (or link to CHANGELOG.md if you keep it separate)
```

**4. Merge Documentation Files**

- Copy unique content from scattered docs into appropriate README sections
- Remove files that are now redundant
- Keep CHANGELOG.md and LICENSE separate (these are standard)
- Keep CONTRIBUTING.md separate only if it's substantial (>100 lines)
- Update references to deleted docs

**5. Verify Documentation Accuracy**

- Check that all code examples actually work
- Verify installation steps
- Ensure links aren't broken
- Update version numbers if present

**Commit Strategy:**

```bash
git add README.md docs/ <other-doc-files>
git commit -m "Consolidate documentation into comprehensive README

Merged content from:
- docs/usage.md
- docs/installation.md
- USAGE.txt

Removed outdated references to deprecated features.
All code examples verified working."
```

### Phase 4: Command-Line Simplification

**This is the most dangerous phase** — changing CLI interfaces can break user scripts and workflows. Proceed carefully.

**1. Analyze Current CLI Interface**

For Python (argparse, click, typer):
```bash
# Find argument definitions
grep -r "add_argument\|@click.option\|@click.argument" --include="*.py" .
```

For Go (flag, cobra, pflag):
```bash
# Find flag definitions
grep -r "flag\.\|cmd.Flags()" --include="*.go" .
```

**2. Categorize Parameters**

Create a spreadsheet or table:

| Parameter | Type | Default | Used In Code? | Used In Tests? | User Impact | Action |
|-----------|------|---------|---------------|----------------|-------------|--------|
| --verbose | bool | false | Yes (logging) | No | Medium | Keep |
| --debug | bool | false | Yes (logging) | No | Medium | Merge with --verbose |
| --output-format | string | json | No (unused) | No | Low | Remove |

**3. Identify Safe Removals**

Safe to remove:
- Parameters that literally do nothing (dead code)
- Parameters with defaults that are never overridden in tests or examples
- Internal/debug flags not documented

**Risky to remove:**
- Any documented flag
- Flags used in examples
- Flags that change behavior (even if not tested)

**4. Consolidate Overlapping Parameters**

Example patterns:
- `--verbose` + `--debug` → single `--verbose` with levels
- `--output-json` + `--output-yaml` → `--format json|yaml`
- Multiple boolean flags → single `--mode` enum

**5. Update Tests**

Critical: Update tests BEFORE removing parameters. This verifies your assumptions:

```bash
# Search for parameter usage in tests
grep -r "\-\-parameter-name" tests/
```

**6. Preserve Backward Compatibility (If Needed)**

If the tool is used by others, consider:
- Keeping deprecated flags as aliases (with warnings)
- Documenting migration path
- Bumping major version

**Commit Strategy:**

One commit per parameter change:

```bash
git add <cli-files> <test-files>
git commit -m "Remove unused --output-format parameter

Analysis showed this parameter was defined but never used in code.
No tests reference it. No documentation mentions it.
Verified all tests still pass."
```

### Phase 5: Test Simplification

Tests accumulate cruft over time — duplicates, tests for deleted code, outdated behavior checks. Simplifying tests makes the suite faster and more maintainable.

**Critical Principle**: Only remove tests that are genuinely redundant or outdated. Never remove tests that provide unique coverage or document important edge cases.

**1. Inventory Test Files**

Locate test files based on language:

```bash
# Python
find . -name "test_*.py" -o -name "*_test.py"
find . -path "*/tests/*"

# Go
find . -name "*_test.go"
```

**2. Identify Redundant Tests**

**Safe to Remove:**

- **Duplicate test cases** (literally copy-pasted with same logic)
  - Example: `test_parse_json` and `test_json_parsing` that do identical things
  - Verify by reading both test bodies — they must be functionally identical

- **Tests for removed code**
  - If you removed a function in Phase 2, remove its tests
  - Check imports — if test imports something that doesn't exist, it's stale

- **Outdated tests for changed behavior**
  - Tests that expect old behavior no longer supported
  - Tests that document deprecated features
  - Update test expectations if behavior changed, remove if feature removed

- **Non-discriminating tests** (always pass regardless of implementation)
  - Tests that assert `result is not None` without checking actual value
  - Tests that just call a function without verifying behavior
  - Tests with no assertions or only trivial ones

- **Overly specific tests covered by general ones**
  - If `test_parse_valid_json_with_numbers` exists and `test_parse_valid_json` already covers it, remove the specific one
  - Keep the general test, remove the subset

- **Duplicate setup code across files**
  - Multiple test files with identical `setUp()` or fixture definitions
  - Consolidate into shared `conftest.py` (Python) or helper file
  - This reduces duplication without removing coverage

**Must Keep:**

- **Edge case tests**
  - Tests for boundary conditions (empty input, max values, etc.)
  - Even if they "overlap" with other tests, edge cases deserve explicit coverage

- **Integration tests**
  - Tests that verify multiple components work together
  - These are expensive to write and shouldn't be removed lightly

- **Regression tests**
  - Tests added to prevent specific bugs from recurring
  - Even if they seem redundant, they document important failures
  - Look for comments like "regression test for issue #123"

- **Tests documenting intended behavior**
  - Tests that serve as examples or specification
  - Tests referenced in documentation

- **Tests that caught bugs in the past**
  - Check git history — if removing a test would have hidden a historical bug, keep it

**3. Analyze Test Coverage (If Tools Available)**

Before removing tests, check coverage:

```bash
# Python
python -m pytest --cov=. --cov-report=term-missing

# Go
go test -cover ./...
```

Don't remove tests if coverage drops significantly. The goal is to remove redundancy, not reduce coverage.

**4. Remove Tests Incrementally**

Remove one category at a time with clear commits:

**Step 1**: Remove tests for deleted code
```bash
git commit -m "Remove tests for deleted utility functions

Removed tests for parse_legacy_format() and transform_old_style()
which were deleted in code consolidation phase."
```

**Step 2**: Remove duplicate tests
```bash
git commit -m "Remove duplicate JSON parsing tests

test_parse_json_numbers and test_parse_json_strings were both
subsets of test_parse_json_all_types. Kept the comprehensive test,
removed the specific ones."
```

**Step 3**: Consolidate duplicate setup
```bash
git commit -m "Consolidate duplicate test fixtures into conftest.py

Three test files had identical database_connection fixture.
Moved to shared conftest.py to reduce duplication."
```

**5. Verify Tests Still Pass**

After each removal, run the test suite:

```bash
# Python
python -m pytest

# Go
go test ./...
```

All remaining tests must pass. If they don't:
- Investigate why
- Fix the issue (maybe you removed something needed)
- Revert if you can't fix it

**6. Update Test Documentation**

If the project has test documentation (like `tests/README.md`), update it to reflect:
- Removed test files
- New consolidated fixtures
- Any changes to how to run tests

**Language-Specific Test Patterns**

**Python:**
- Look for `unittest.TestCase` classes with duplicate methods
- Check for multiple `@pytest.fixture` definitions with same logic
- Consolidate assertion helpers scattered across files
- Remove unused `mock.patch` decorators

**Go:**
- Look for table-driven tests with redundant cases
- Consolidate helper functions across `*_test.go` files
- Remove unused test data structures
- Check for benchmark tests (`Benchmark*`) that test same code

**Warning Signs to Stop**

If you see these, be more conservative:

- Test coverage dropping >5%
- Tests that look similar but have subtle differences in edge cases
- Many tests with comments explaining why they exist
- Test suite that's already small (<50 tests total)

In these cases, consult with the user before removing anything.

**Commit Strategy Summary:**

Each commit should:
- Focus on one type of simplification
- Explain what was removed and why
- Note any coverage impact
- Confirm remaining tests pass

Example:
```bash
git commit -m "Simplify authentication tests

Removed:
- test_login_with_valid_credentials_lowercase (covered by test_login_valid)
- test_login_with_valid_credentials_uppercase (covered by test_login_valid)
- test_logout_user (function removed in Phase 2)

Consolidated:
- Three identical user_fixture definitions into conftest.py

All 47 remaining tests pass. Coverage: 94% (unchanged)."
```

### Phase 6: Verification and Review

**1. Run Test Suite**

```bash
# Python
python -m pytest
# or
python -m unittest discover

# Go
go test ./...
```

All tests must pass. If they don't:
- Investigate what broke
- Fix or revert the change
- Document why in the commit

**2. Create Functionality Checklist**

Based on the project type, create a manual verification checklist:

**For CLI Tools:**
```
- [ ] Help text displays correctly
- [ ] Basic command runs without errors
- [ ] Common use cases work (test 2-3 examples)
- [ ] Error handling works (try invalid input)
- [ ] Configuration loading works
```

**For Libraries:**
```
- [ ] Import statements work
- [ ] Basic API calls function
- [ ] Examples from README work
- [ ] Error handling works
```

Ask user to verify this checklist or verify it yourself by running examples.

**3. Review All Commits**

Generate a summary:

```bash
git log backup-before-simplification-$(git log --all --grep="backup-before-simplification" --format="%h" -n 1)..HEAD --oneline
```

Show this to the user with a summary of:
- Number of files changed
- Lines of code removed
- Functions consolidated
- Documentation files merged
- Parameters removed

**4. Create Summary Report**

Present a final report:

```markdown
# Repository Simplification Summary

## Code Changes
- Consolidated X duplicate functions into [location]
- Removed Y lines of redundant code
- Merged Z similar implementations
- Moved utilities to centralized modules

## Documentation Changes
- Merged [list of files] into comprehensive README
- Removed X outdated references
- Updated Y code examples
- Added Z missing sections to README

## CLI Changes
- Removed X unused parameters: [list]
- Consolidated Y overlapping flags: [list with mappings]
- Simplified parameter structure

## Test Changes
- Removed X duplicate test cases
- Removed Y tests for deleted code
- Consolidated Z duplicate fixtures/helpers
- Test coverage: before X% → after Y% (change: +/-Z%)
- All remaining tests pass ✓

## Verification
- [✓] Test suite passes (X tests, Y seconds)
- [✓] Core functionality verified
- [✓] Examples work
- [✓] Documentation accurate
- [✓] No regressions detected

## Impact Metrics
- Lines of code: before X → after Y (reduced Z%)
- Test files: before X → after Y
- Documentation files: before X → after Y
- Total commits made: X

## Files Changed
- Added: [count]
- Modified: [count]
- Removed: [count]

## Commit History
[List of commit messages showing incremental changes]

## Next Steps
1. Review the changes: `git diff backup-before-simplification-[timestamp]`
2. Test thoroughly in your environment
3. Run your own verification checks
4. If satisfied: merge or continue from current state
5. If not: `git checkout backup-before-simplification-[timestamp]`

## Backup Branch
Created: `backup-before-simplification-[timestamp]`
```

## Anti-Patterns to Avoid

**Don't:**
- Remove code you don't understand
- Assume similar-looking functions are identical without testing
- Change functionality "because it seems simpler"
- Remove tests without running them first
- Merge documentation without reading it
- Remove CLI parameters that are documented
- Make all changes in one giant commit
- Skip creating the backup branch
- Simplify without user approval on risky changes

**Do:**
- Verify every assumption with tests or code execution
- Make small, reviewable commits
- Preserve functionality above all else
- Ask the user when uncertain
- Document your reasoning in commit messages
- Keep the backup branch as insurance
- Test after every significant change

## Edge Cases and Considerations

**When you find multiple "almost identical" functions:**
Sometimes functions that look the same have subtle differences (different error handling, slightly different logic for edge cases). Don't blindly merge them — verify they're truly equivalent.

**When documentation conflicts:**
If different docs say different things, investigate which is correct by checking the code. Update docs to match reality.

**When tests fail after simplification:**
This means you removed something that was needed, or the tests themselves need updating. Fix or revert before proceeding.

**When CLI parameters have undocumented users:**
Be conservative. If you're not sure whether anyone uses a parameter, keep it (possibly with a deprecation warning).

**When dealing with exported APIs (Go) or public APIs (Python packages):**
Be extremely careful. Removing these is a breaking change. Consider deprecation instead of removal.

## Language-Specific Notes

### Python
- Use AST parsing for robust function detection
- Check `__init__.py` files for what's exported
- Look for duplicate requirements in `requirements.txt`, `setup.py`, `pyproject.toml`
- Consider consolidating small modules into larger ones
- Watch for circular imports when moving code

### Go
- Exported (capitalized) functions are public API — handle with care
- Internal packages are good consolidation targets
- Check `go.mod` for redundant dependencies
- Look for duplicate error definitions
- Consider whether to consolidate small packages

## When This Skill Isn't Appropriate

Don't use this skill when:
- The repository is already well-organized and minimal
- The user wants to add features (use a development skill)
- The user wants to refactor architecture (use a refactoring skill)
- There's no obvious duplication or redundancy
- The project is large and complex (>10k LOC) without a clear simplification target — break it down into smaller scopes first

## Expected Outcome

After running this skill, the repository should be:
- Easier to understand (less code, clearer documentation)
- Easier to maintain (less duplication, fewer files)
- Functionally identical (all tests pass, examples work)
- Safer (backup branch exists)
- Reviewable (incremental commits show what changed and why)

The user should feel confident that nothing broke, understand what changed, and be able to roll back if needed.
