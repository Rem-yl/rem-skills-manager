---
name: tdd-feature-development
description: Guide rigorous feature development with test-driven development and strict quality standards. Use when implementing new features, adding functionality, building new components, or creating new modules. Enforces TDD workflow (tests before implementation), complete type annotations, comprehensive documentation in English, code review after each stage, code formatting, and incremental git commits. Trigger for feature development requests, even without explicit mention of testing or TDD.
---

# TDD Feature Development

A structured workflow for developing new features using test-driven development with emphasis on code quality, documentation, and incremental commits.

## When to Use This Skill

Use this skill when:
- Implementing new features or functionality
- Building new components or modules
- Adding significant new capabilities to existing code
- The user wants a rigorous, quality-focused development process

## Core Principles

1. **Test-First**: Write tests before implementation code
2. **Type Safety**: Complete and accurate type annotations
3. **Documentation**: Comprehensive docs for all key functions and files
4. **Incremental Progress**: Review and commit after each logical stage
5. **Quality Gates**: Code review and formatting before commits

## Development Workflow

### Phase 1: Planning and Design

Before writing any code:

1. **Understand Requirements**
   - Clarify what the feature should do
   - Identify inputs, outputs, and edge cases
   - Determine success criteria

2. **Break Down into Components**
   - Split the feature into logical, testable components
   - Each component should be a self-contained unit of functionality
   - Examples: "user authentication", "data validation", "API endpoint handler"

3. **Plan Test Strategy**
   - What test frameworks are available? (pytest, unittest, Go testing, Jest, etc.)
   - What needs unit tests? Integration tests?
   - What edge cases must be covered?

### Phase 2: Component Development Cycle

For each component, follow this cycle:

#### Step 1: Write Tests First

**Before writing any implementation code**, write comprehensive tests:

```python
# Example: Python with pytest
def test_user_authentication_success():
    """Test successful authentication with valid credentials."""
    auth = AuthService()
    result = auth.authenticate("user@example.com", "correct_password")
    assert result.success is True
    assert result.user_id is not None

def test_user_authentication_failure():
    """Test authentication failure with invalid credentials."""
    auth = AuthService()
    result = auth.authenticate("user@example.com", "wrong_password")
    assert result.success is False
    assert result.error == "Invalid credentials"
```

```go
// Example: Go testing
func TestUserAuthenticationSuccess(t *testing.T) {
    // Test successful authentication with valid credentials
    auth := NewAuthService()
    result, err := auth.Authenticate("user@example.com", "correct_password")

    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }
    if !result.Success {
        t.Error("Expected successful authentication")
    }
}
```

**Test Requirements**:
- Test the happy path (expected behavior)
- Test error conditions and edge cases
- Test boundary conditions
- Include descriptive test names and docstrings (in English)

#### Step 2: Run Tests (They Should Fail)

Run the tests to verify they fail (since the implementation doesn't exist yet):

```bash
# Python
pytest path/to/test_file.py -v

# Go
go test ./... -v

# JavaScript/TypeScript
npm test
```

**Expected**: Tests should fail because the implementation doesn't exist yet. If tests pass without implementation, the tests are wrong.

#### Step 3: Implement the Feature

Now write the minimal code needed to make the tests pass:

**Implementation Requirements**:

1. **Type Annotations** (complete and accurate):
   ```python
   # Python
   from typing import Optional, Dict, Any

   def authenticate(self, email: str, password: str) -> AuthResult:
       """
       Authenticate a user with email and password.

       Args:
           email: User's email address
           password: User's password (plain text, will be hashed)

       Returns:
           AuthResult containing success status and user info or error

       Raises:
           ValueError: If email format is invalid
       """
       # Implementation here
       pass
   ```

   ```go
   // Go
   // Authenticate verifies user credentials and returns authentication result.
   //
   // Parameters:
   //   - email: User's email address
   //   - password: User's password (plain text)
   //
   // Returns:
   //   - *AuthResult: Authentication result with user info
   //   - error: Error if authentication fails or invalid input
   func (a *AuthService) Authenticate(email string, password string) (*AuthResult, error) {
       // Implementation here
   }
   ```

2. **Documentation Comments** (English, comprehensive):
   - Every public function/method needs a docstring
   - Explain what it does, parameters, return values, and exceptions/errors
   - For complex logic, add inline comments explaining why (not just what)

3. **Inline Comments** (English, for non-obvious code):
   ```python
   # Hash password using bcrypt for security
   password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

   # Query database with index hint for performance
   user = db.query(User).filter_by(email=email).first()
   ```

#### Step 4: Run Tests (They Should Pass)

```bash
pytest path/to/test_file.py -v
go test ./... -v
npm test
```

**Expected**: All tests should pass. If any fail, fix the implementation until they pass.

#### Step 5: Refactor (If Needed)

If the code works but can be improved:
- Extract duplicate logic into helper functions
- Simplify complex conditionals
- Improve naming
- **Maintain type annotations and documentation during refactoring**
- Re-run tests after each refactoring change

### Phase 3: Stage Completion

After completing a component (tests pass, implementation works):

#### Step 1: Code Review

**MANDATORY STEP - DO NOT SKIP**

Before proceeding to formatting or commits, you MUST invoke the code-reviewer skill.

**Use the Skill tool with this exact invocation:**

```
Skill tool:
- skill: "superpowers:code-reviewer"
- args: (none needed)
```

**What to say when invoking:**
"I've completed the [component name] implementation. Please review:
- Tests in [file path]
- Implementation in [file path]
- All requirements have been met and tests pass"

The code-reviewer will check:
- Code quality and best practices
- Test coverage and quality
- Documentation completeness
- Type annotation accuracy
- Potential bugs or issues

**CRITICAL**: Address ALL feedback before proceeding. If the reviewer finds issues:
1. Fix the issues
2. Re-run tests to ensure they still pass
3. Invoke code-reviewer AGAIN to verify fixes

Do not proceed to Step 2 (formatting) until code review is complete and all issues are resolved.

#### Step 2: Format Code

Run the appropriate code formatter for your language:

```bash
# Python
black .
isort .
mypy path/to/code  # Type checking

# Go
go fmt ./...
go vet ./...

# JavaScript/TypeScript
npm run format  # or: npx prettier --write .
npm run lint    # or: npx eslint --fix .
```

**Verify tests still pass after formatting.**

#### Step 3: Git Commit

Create a clear, descriptive commit:

```bash
# Stage only the files for this component
git add path/to/test_file.py path/to/implementation.py

# Write a descriptive commit message
git commit -m "feat(auth): implement user authentication with email/password

- Add AuthService with authenticate() method
- Include type hints and comprehensive docstrings
- Add tests for success and failure cases
- Handle edge cases: invalid email format, empty passwords

Tests: 5 passed
"
```

**Commit Message Guidelines**:
- Use conventional commits format: `type(scope): description`
- Types: `feat`, `fix`, `refactor`, `test`, `docs`
- Include what was added/changed
- Note test results
- Keep it under 72 characters for the first line

### Phase 4: Integration and Completion

After all components are implemented:

1. **Integration Testing**
   - Test components working together
   - Verify end-to-end functionality
   - Check edge cases across component boundaries

2. **Final Review**
   - Run code-reviewer on the complete feature
   - Ensure all quality standards are met

3. **Final Commit**
   - Commit integration tests and any final adjustments
   - Update any high-level documentation

## Language-Specific Guidance

### Python

**Type Annotations**:
```python
from typing import List, Optional, Dict, Union, Callable
from dataclasses import dataclass

@dataclass
class User:
    id: int
    email: str
    name: Optional[str] = None
```

**Testing**: Use `pytest` with fixtures
**Formatting**: `black` (code), `isort` (imports), `mypy` (type checking)
**Documentation**: Google-style or NumPy-style docstrings

### Go

**Type Safety**: Use interfaces for abstraction
```go
type Authenticator interface {
    Authenticate(email string, password string) (*AuthResult, error)
}
```

**Testing**: Use table-driven tests for multiple cases
**Formatting**: `go fmt`, `go vet`
**Documentation**: Standard Go doc comments (complete sentences)

### TypeScript/JavaScript

**Type Annotations**:
```typescript
interface AuthResult {
    success: boolean;
    userId?: string;
    error?: string;
}

function authenticate(email: string, password: string): Promise<AuthResult>
```

**Testing**: Jest or Vitest
**Formatting**: Prettier, ESLint
**Documentation**: JSDoc comments

### Other Languages

Adapt the principles:
- Use the language's standard testing framework
- Apply the strictest type system available
- Follow language-specific documentation conventions
- Use standard formatters for the language

## Quality Checklist

Before marking a component as complete, verify:

- [ ] Tests written first (before implementation)
- [ ] All tests pass
- [ ] Complete type annotations on all public interfaces
- [ ] Comprehensive docstrings/documentation (English)
- [ ] Inline comments for complex logic (English)
- [ ] Code reviewed by code-reviewer skill (MANDATORY - use Skill tool)
- [ ] Code formatted with standard tools
- [ ] Git commit created with clear message
- [ ] No commented-out code or TODO markers (resolve them first)

## Common Pitfalls

**Don't**:
- Skip writing tests first ("I'll add them later")
- Write incomplete or vague type annotations
- Use non-English comments or documentation
- Commit without running formatter
- Make giant commits with multiple unrelated changes
- **NEVER skip code review** - it's mandatory, not optional, even if code looks perfect

**Do**:
- Write tests that actually verify behavior
- Use specific types (not `Any` or `interface{}` unless truly needed)
- Explain the "why" in comments, not just the "what"
- Commit early and often
- Keep commits focused on single logical changes
- Take code review feedback seriously

## Example End-to-End Flow

**User Request**: "Implement a user registration feature"

1. **Planning**:
   - Break into components: email validation, password hashing, user creation, duplicate checking

2. **Component 1: Email Validation**:
   - Write tests for valid emails, invalid formats, edge cases
   - Run tests (they fail)
   - Implement `validate_email()` with types and docs
   - Run tests (they pass)
   - **Invoke code-reviewer** (using Skill tool with "superpowers:code-reviewer")
   - Address feedback
   - Format code
   - Commit: `feat(auth): add email validation`

3. **Component 2: Password Hashing**:
   - Write tests for hashing, verification, weak passwords
   - Run tests (they fail)
   - Implement `hash_password()` with types and docs
   - Run tests (they pass)
   - Code review → Format → Commit: `feat(auth): add password hashing with bcrypt`

4. **Component 3: User Creation**:
   - Write tests for creating users, duplicate detection
   - Run tests (they fail)
   - Implement `create_user()` with types and docs
   - Run tests (they pass)
   - Code review → Format → Commit: `feat(auth): implement user registration`

5. **Integration**:
   - Write end-to-end tests
   - Verify all components work together
   - Final review → Commit: `test(auth): add integration tests for registration`

**Result**: A fully-tested, well-documented, type-safe user registration feature with a clean git history.

---

## Quick Reference

**TDD Cycle**: Test (fail) → Implement → Test (pass) → Refactor → **Review (MANDATORY: use Skill tool)** → Format → Commit

**Quality Standards**:
- Type annotations: Complete and accurate
- Documentation: All public functions, English only
- Comments: Complex logic only, English only
- Tests: Before implementation, comprehensive coverage

**Tools** (adapt to your language):
- Python: pytest, black, isort, mypy
- Go: go test, go fmt, go vet
- TypeScript: Jest, Prettier, ESLint
