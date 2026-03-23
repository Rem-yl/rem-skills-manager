# Prompt Refinement Examples

This document provides before/after examples showing how the refining-prompts skill transforms vague requests into clear, actionable prompts.

## Example 1: Vague Feature Request

### Before (Vague)
```
"Add authentication to the app"
```

**Problems:**
- No auth method specified (JWT? Session? OAuth?)
- Unclear scope (which endpoints? all routes?)
- No storage mechanism mentioned
- Missing success criteria
- No constraints about libraries or patterns

### Refinement Questions Asked

1. **Context:** "Which parts of the app need authentication? (a) All API endpoints (b) Specific routes (c) Admin panel only"
   - Answer: "All API endpoints under /api/"

2. **Constraint:** "Do you have a preference for auth method? (a) JWT (b) Session-based (c) OAuth (d) No preference"
   - Answer: "JWT"

3. **Clarity:** "Where should JWT tokens be stored? (a) httpOnly cookies (b) localStorage (c) Authorization header"
   - Answer: "httpOnly cookies"

4. **Completeness:** "What should token expiration be? (a) 24 hours (b) 7 days (c) 30 days (d) Custom"
   - Answer: "24 hours"

5. **Criteria:** "How should we validate this? (a) Unit tests (b) Integration tests (c) Both (d) Manual testing"
   - Answer: "Both unit and integration tests"

6. **Completeness:** "What should happen for unauthenticated requests? (a) 401 JSON error (b) Redirect to /login (c) Custom handler"
   - Answer: "401 JSON error with message"

### After (Refined)

```markdown
## Refined Prompt: Add JWT Authentication

**Goal:** Implement JWT-based authentication for all API endpoints

**Context:**
- Scope: All routes under /api/*
- Files to modify: middleware/, routes/api.ts, controllers/auth.ts
- Follow existing middleware pattern in middleware/validation.ts

**Requirements:**
- Implement JWT token generation on successful login
- Store tokens in httpOnly cookies for security
- Add authentication middleware to verify tokens on protected routes
- Token expiration: 24 hours
- Return 401 JSON response for unauthenticated requests

**Constraints:**
- Must use httpOnly cookies (not localStorage)
- Use existing Express middleware pattern
- Compatible with current CORS configuration

**Success Criteria:**
- Unit tests for JWT generation and verification
- Integration tests for protected route access
- Unauthenticated requests receive 401 with clear error message
- Authenticated requests with valid token succeed
- Expired tokens properly rejected

**Out of Scope:**
- User registration (separate task)
- Password reset functionality
- Role-based access control (RBAC)
- Refresh tokens
```

**Next Action:** Invoke brainstorming to explore implementation approaches (middleware architecture, error handling, token refresh strategy).

---

## Example 2: Incomplete Bug Report

### Before (Vague)
```
"Users can't login"
```

**Problems:**
- No specific error described
- Unclear which users affected (all? some?)
- No reproduction steps
- Missing environment info
- No investigation done

### Refinement Questions Asked

1. **Context:** "When did this start happening? (a) After recent deploy (b) Always been an issue (c) Intermittent (d) Not sure"
   - Answer: "After deploy yesterday"

2. **Clarity:** "What exactly happens when users try to login? (a) Error message (b) Infinite loading (c) Redirect to wrong page (d) Other"
   - Answer: "Error message: 'Invalid credentials'"

3. **Completeness:** "Is this affecting all users or specific ones? (a) All users (b) Some users (c) Just one user (d) Not tested"
   - Answer: "Only users with special characters in email (like +)"

4. **Context:** "What file handles login? Do you know?"
   - Answer: "AuthController.ts login() method"

5. **Criteria:** "How can we reproduce this? What email should we test with?"
   - Answer: "test+user@example.com fails, testuser@example.com works"

6. **Completeness:** "What changed in yesterday's deploy?"
   - Answer: "Added email validation with regex"

### After (Refined)

```markdown
## Refined Prompt: Fix Login Failure for Emails with Plus Sign

**Goal:** Fix bug where users with + in email address cannot login

**Context:**
- File: AuthController.ts, login() method
- Introduced in: Yesterday's deploy (commit abc123)
- Recent change: Added email validation with regex
- Working users: Standard emails (test@example.com)
- Failing users: Emails with + (test+user@example.com)

**Requirements:**
- Update email validation regex to allow + character
- Ensure + is properly URL-encoded in any API calls
- Validate fix works for other special characters (@, -, _, .)

**Reproduction Steps:**
1. Navigate to /login
2. Enter email: test+user@example.com
3. Enter any password
4. Click login
5. Observe: "Invalid credentials" error (should succeed)

**Root Cause Hypothesis:**
Email validation regex likely doesn't include + in allowed characters, or + is being mishandled in URL encoding.

**Success Criteria:**
- test+user@example.com can login successfully
- Existing tests still pass
- Add regression test for emails with special characters
- Verify no other special chars are broken

**Files to Check:**
- AuthController.ts (login method)
- email-validation.ts or similar validator
- Any middleware that processes email input
```

**Next Action:** Direct execution - clear bug with specific file and fix approach.

---

## Example 3: Performance Request

### Before (Vague)
```
"Make it faster"
```

**Problems:**
- No specific component mentioned
- "Faster" is not measurable
- No baseline metrics
- Unknown bottleneck

### Refinement Questions Asked

1. **Context:** "What feels slow? (a) Page load (b) API response (c) Search results (d) Form submission (e) Other"
   - Answer: "Search results on /search page"

2. **Clarity:** "What's the current response time?"
   - Answer: "About 2 seconds from typing to results showing"

3. **Criteria:** "What's an acceptable response time? (a) <100ms (b) <500ms (c) <1s (d) Other"
   - Answer: "<500ms"

4. **Context:** "What files handle search?"
   - Answer: "SearchController.ts and SearchService.ts"

5. **Completeness:** "Do you know where the bottleneck is? (a) Database query (b) API network time (c) Frontend rendering (d) Not investigated"
   - Answer: "Not investigated yet"

6. **Constraint:** "Can we change the database schema? (a) Yes (b) No (c) Prefer not to"
   - Answer: "Yes, we can add indexes"

### After (Refined)

```markdown
## Refined Prompt: Optimize Search Performance

**Goal:** Reduce search response time from ~2s to <500ms

**Context:**
- Page: /search
- Files: SearchController.ts, SearchService.ts
- Current performance: ~2 seconds
- Target performance: <500ms
- Schema changes: Allowed (can add indexes)

**Investigation Required:**
1. Profile current search query execution time
2. Check for N+1 queries
3. Analyze database query plans
4. Measure frontend rendering time
5. Check network request waterfall

**Potential Optimizations:**
- Add database indexes on frequently queried columns
- Implement query result caching
- Optimize ORM queries (eliminate N+1)
- Add pagination if returning large result sets
- Consider debouncing search input

**Success Criteria:**
- Search response time <500ms (P95)
- Measure with realistic dataset (10k+ records)
- Before/after metrics documented
- All existing search tests pass
- No regression in search accuracy/completeness

**Constraints:**
- Must maintain current search functionality
- Can't break existing API contract
- Should work with current production data volume

**Metrics to Capture:**
- Database query execution time
- API response time
- Frontend rendering time
- Memory usage
```

**Next Action:** Invoke brainstorming to profile bottleneck and explore optimization strategies (indexes, caching, query optimization).

---

## Example 4: Refactoring Request

### Before (Vague)
```
"Clean up the code"
```

**Problems:**
- No specific files mentioned
- "Clean up" is subjective
- No success criteria
- Unclear what patterns to follow

### Refinement Questions Asked

1. **Context:** "Which code needs cleaning? (a) Specific file (b) Entire directory (c) Whole codebase (d) Not sure"
   - Answer: "UserController.ts - it's gotten messy"

2. **Clarity:** "What makes it messy? (a) Too long (b) Duplicated code (c) Hard to test (d) Unclear logic (e) All of above"
   - Answer: "Too long (500+ lines) and hard to test"

3. **Completeness:** "What should we extract? (a) Validation logic (b) Database queries (c) Business logic (d) All separate concerns"
   - Answer: "Extract validation logic into separate validator class"

4. **Context:** "What pattern should we follow?"
   - Answer: "We have ValidationService pattern used in ProductController"

5. **Criteria:** "How will we validate the refactor worked? (a) Tests still pass (b) No behavior change (c) Both"
   - Answer: "Both - tests pass and behavior identical"

6. **Constraint:** "Can we change the API contract? (a) Yes (b) No (c) Only internal changes"
   - Answer: "Only internal changes, API must stay the same"

### After (Refined)

```markdown
## Refined Prompt: Refactor UserController Validation Logic

**Goal:** Extract validation logic from UserController into UserValidator class

**Context:**
- File to refactor: UserController.ts (currently 500+ lines)
- Pattern to follow: ValidationService pattern from ProductController.ts
- Current structure: Validation mixed with controller logic
- Target structure: Separate UserValidator class

**Requirements:**
- Create new UserValidator class following ProductValidator pattern
- Extract all validation logic from UserController
- Maintain exact same validation behavior
- Keep all existing tests passing
- Update controller to use new validator

**Constraints:**
- No changes to API contract (same routes, same responses)
- No behavior changes (same validation rules)
- Must follow existing ValidationService pattern
- Maintain current error message format

**Success Criteria:**
- All existing tests pass without modification
- UserController.ts reduced to <200 lines
- UserValidator.ts created with clear single responsibility
- Manual testing confirms identical behavior
- Code coverage maintained or improved

**Files to Create:**
- validators/UserValidator.ts (new)

**Files to Modify:**
- controllers/UserController.ts (extract validation)
- Reference: controllers/ProductController.ts, validators/ProductValidator.ts

**Out of Scope:**
- Changing validation rules
- Adding new validation
- Refactoring other parts of UserController
- Updating tests (should pass as-is)
```

**Next Action:** Invoke writing-plans for step-by-step refactoring plan (read existing code, write validator, update controller, verify tests).

---

## Example 5: UI Implementation

### Before (Vague)
```
"Make it responsive"
```

**Problems:**
- No specific component mentioned
- Unclear breakpoints
- No design reference

### Refinement Questions Asked

1. **Context:** "What component needs to be responsive? (a) Entire app (b) Specific page (c) Single component"
   - Answer: "Dashboard layout on /dashboard"

2. **Clarity:** "What breakpoints should we support? (a) Mobile only (b) Tablet + mobile (c) Full responsive (d) Specific sizes"
   - Answer: "Tablet (768px) and mobile (375px)"

3. **Completeness:** "What should change at each breakpoint?"
   - Answer: "Desktop: 3-column grid, Tablet: 2-column, Mobile: 1-column stacked"

4. **Context:** "What files contain the dashboard layout?"
   - Answer: "components/Dashboard.tsx and styles/dashboard.css"

5. **Criteria:** "How should we test this? (a) Visual inspection (b) Automated responsive tests (c) Both"
   - Answer: "Visual inspection in Chrome DevTools at each breakpoint"

### After (Refined)

```markdown
## Refined Prompt: Make Dashboard Responsive

**Goal:** Add responsive layouts for tablet and mobile viewports

**Context:**
- Component: Dashboard.tsx
- Styles: dashboard.css
- Current state: Fixed 3-column layout (desktop only)

**Requirements:**
- Desktop (≥1024px): 3-column grid (current)
- Tablet (768px-1023px): 2-column grid
- Mobile (≤767px): 1-column stacked layout
- Maintain all existing dashboard functionality
- Smooth transitions between breakpoints

**Constraints:**
- Use CSS media queries (no JS breakpoint detection)
- Follow existing responsive patterns in codebase
- Don't break desktop layout

**Success Criteria:**
- Visual inspection at 375px (mobile), 768px (tablet), 1024px (desktop)
- All dashboard widgets render correctly at each breakpoint
- No horizontal scroll at any breakpoint
- Content readable and accessible on mobile

**Files to Modify:**
- components/Dashboard.tsx (possible structure changes)
- styles/dashboard.css (add media queries)

**Testing Approach:**
1. Chrome DevTools responsive mode
2. Test at 375px, 768px, 1024px, 1440px
3. Verify all widgets visible and functional
4. Check touch targets on mobile (≥44px)
```

**Next Action:** Direct execution - clear implementation with specific breakpoints and layout changes.

---

## Pattern Summary

### Common Vague Signals and Fixes

| Vague Request | Key Questions | Refined Output |
|---------------|---------------|----------------|
| "Add [feature]" | Which files? What tech? Success criteria? | Specific files, tech choices, validation approach |
| "Fix [bug]" | Reproduction steps? Which users? What changed? | Exact error, affected scope, root cause hypothesis |
| "Improve [metric]" | Current vs target? Where bottleneck? Can we profile? | Measurable baseline/target, investigation plan |
| "Refactor [code]" | What pattern? What's messy? Can API change? | Specific extraction, pattern to follow, constraints |
| "Make [thing] responsive" | Which component? What breakpoints? Design spec? | Specific component, exact breakpoints, expected behavior |

### Question Type Examples

**Context Questions:**
- "Which files/components handle [X]?"
- "What existing patterns should we follow?"
- "What's the current state/implementation?"

**Constraint Questions:**
- "Can we change [X]? (yes/no/prefer not)"
- "Must we use [library Y]?"
- "What's not allowed to change?"

**Clarity Questions:**
- "What exactly should change from A to B?"
- "What does [vague term] mean specifically?"
- "Can you describe the expected output?"

**Criteria Questions:**
- "How will we know this works?"
- "What tests should pass?"
- "What metrics define success?"

**Completeness Questions:**
- "What edge cases should we handle?"
- "What's explicitly out of scope?"
- "What error states exist?"

---

## Anti-Pattern Examples

### ❌ Asking Too Many Questions at Once

**Bad:**
```
"To refine your request, I need to know:
1. Which files are involved?
2. What's the current behavior?
3. What should change?
4. What constraints exist?
5. How should we test it?
6. What's the timeline?
7. Any libraries to use/avoid?
8. What's out of scope?"
```

**Good:**
```
"Let's start with context - which files or components handle this functionality?
(a) I know the files
(b) I need help finding them
(c) Not sure"
```

### ❌ Making Assumptions Without Validating

**Bad:**
```
"I'll add JWT authentication with Redis for token storage,
implement refresh tokens, and add role-based access control."
```
(User just said "add authentication" - many assumptions!)

**Good:**
```
"For authentication, let's clarify the approach:

What auth method works best for your use case?
(a) JWT (stateless, good for APIs)
(b) Session-based (simpler, server-side state)
(c) OAuth (third-party like Google/GitHub)
(d) Not sure, need guidance"
```

### ❌ Refining Forever (Perfectionism)

**Bad:**
```
"Just a few more questions:
- What error messages for each validation failure?
- Should we log failed login attempts?
- What about rate limiting?
- Password complexity requirements?
- Account lockout policy?
..."
```
(Going beyond the immediate scope)

**Good:**
```
"I think we have enough to proceed. Here's the refined prompt:
[Shows refined prompt]

For now, let's focus on core login functionality.
We can address rate limiting and account lockout in separate tasks."
```

---

## Usage Tips

1. **Start broad, then narrow:** Context → Constraints → Specifics
2. **Use multiple choice aggressively:** Easier for users than open-ended
3. **Know when to stop:** If an unfamiliar person could implement it, you're done
4. **Progressive disclosure:** Don't ask about edge cases until core is clear
5. **Validate assumptions early:** "I'm assuming X, is that correct?"
6. **Reference existing patterns:** "Like we did in [similar feature]?"
7. **Offer expertise where helpful:** "For this use case, JWT is typically better because..."
8. **Acknowledge trade-offs:** "Option A is simpler but less flexible, Option B is more robust but adds complexity"

Remember: The goal is actionable clarity, not bureaucracy. Quick refinement for simple tasks, thorough refinement for complex ones.
