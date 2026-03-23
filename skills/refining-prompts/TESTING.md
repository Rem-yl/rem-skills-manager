# Testing the Refining Prompts Skill

## Test Scenarios

Following TDD principles: RED (baseline without skill) → GREEN (with skill) → REFACTOR (close loopholes)

### Scenario 1: Vague Feature Request

**Input:** "Add authentication"

**Expected Refinement:**
- [ ] Authentication method identified (JWT/session/OAuth)
- [ ] Specific endpoints listed
- [ ] Token storage specified
- [ ] Expiration time defined
- [ ] Error handling described
- [ ] Success criteria with tests
- [ ] Files/patterns identified

**Pass Criteria:**
Refined prompt includes all 5Cs with specific implementation details.

---

### Scenario 2: Incomplete Bug Report

**Input:** "Users can't login"

**Expected Refinement:**
- [ ] Error message/type identified
- [ ] Affected users specified (all/some)
- [ ] Reproduction steps provided
- [ ] Expected vs actual behavior clear
- [ ] File/function location identified
- [ ] Success criteria defined
- [ ] Test coverage specified

**Pass Criteria:**
Someone unfamiliar with the project could reproduce and fix the bug.

---

### Scenario 3: Performance Request

**Input:** "Make it faster"

**Expected Refinement:**
- [ ] Specific component identified
- [ ] Current performance metrics
- [ ] Target performance metrics
- [ ] Measurement approach
- [ ] Bottleneck identified or investigation plan
- [ ] Success criteria with benchmarks
- [ ] Constraints specified

**Pass Criteria:**
Clear baseline, target, and approach for optimization.

---

### Scenario 4: Refactoring Request

**Input:** "Clean up the code"

**Expected Refinement:**
- [ ] Specific files/functions identified
- [ ] Issues to address specified
- [ ] Patterns to follow referenced
- [ ] Behavior preservation confirmed
- [ ] Success criteria (tests unchanged)
- [ ] Scope boundaries defined
- [ ] Out of scope explicitly listed

**Pass Criteria:**
Clear extraction/refactoring plan with safety constraints.

---

## Testing Checklist

### Skill Structure
- [x] YAML frontmatter with name and description
- [x] Overview with core principle
- [x] When to use / when NOT to use sections
- [x] Process flow with visual diagram
- [x] All 5Cs defined with examples
- [x] Key techniques documented
- [x] Integration points specified
- [x] Anti-patterns listed
- [x] Completeness check criteria
- [x] Full example workflow

### Framework Completeness
- [x] Context dimension defined
- [x] Constraint dimension defined
- [x] Clarity dimension defined
- [x] Criteria dimension defined
- [x] Completeness dimension defined
- [x] Question templates for each C
- [x] Clarity transformation examples
- [x] Handoff criteria to other skills

### Integration Testing
- [ ] Test transition to brainstorming
- [ ] Test transition to writing-plans
- [ ] Test direct execution handoff
- [ ] Verify no skill overlap conflicts

### Documentation Quality
- [x] Active voice used
- [x] Specific language (no vague terms)
- [x] Scannable structure (tables, lists)
- [x] Concrete examples provided
- [x] README quick reference created
- [x] Examples document comprehensive

### Files Verification
- [x] SKILL.md created (12,301 bytes)
- [x] examples.md created (17,109 bytes)
- [x] README.md created
- [x] TESTING.md created
- [x] Command wrapper created

---

## Manual Testing Protocol

### Phase 1: Baseline (RED)

Test each scenario WITHOUT the skill:

1. Present vague prompt to Claude
2. Count clarification rounds needed
3. Document what information was missing
4. Note if results were off-target
5. Identify wasted effort

**Record findings:** What went wrong? What was missed?

### Phase 2: With Skill (GREEN)

Test same scenarios WITH the skill:

1. Invoke `refining-prompts` skill
2. Follow the refinement process
3. Verify all 5Cs addressed
4. Check if refined prompt is actionable
5. Validate handoff recommendation

**Record findings:** What improved? Are all 5Cs present?

### Phase 3: Edge Cases (REFACTOR)

Test edge cases:

1. Already clear prompt (should skip gracefully)
2. Multi-aspect request (feature + performance)
3. Research task vs implementation task
4. Contradictory requirements (should surface)
5. Missing critical context (should probe deeper)

**Record findings:** Any failure modes? Loopholes to close?

---

## Success Metrics

A successful test produces:

✅ **Refined prompts that:**
- Can be understood by someone unfamiliar with the project
- Include specific file paths or clear discovery approach
- Define measurable success criteria
- Address constraints and edge cases
- Use precise, unambiguous language

✅ **Better outcomes:**
- Fewer clarification rounds during implementation
- Higher quality AI responses on first attempt
- Reduced rework from misunderstood requirements

✅ **Smooth handoffs:**
- Clear recommendation for next action
- Appropriate skill invocation (brainstorming vs writing-plans vs execute)

---

## Known Limitations

Document any identified issues:

1. **Overhead concern:** May add upfront time for simple tasks
   - Mitigation: Clear guidance on when to skip

2. **Skill overlap:** Some questions overlap with brainstorming
   - Differentiation: refining-prompts = articulate request; brainstorming = explore solution

3. **User experience:** Could feel bureaucratic
   - Mitigation: Progressive disclosure, early termination when clear

---

## Next Steps

After testing:

1. [ ] Run all 4 test scenarios
2. [ ] Document baseline failures (RED phase)
3. [ ] Verify skill addresses failures (GREEN phase)
4. [ ] Test edge cases (REFACTOR phase)
5. [ ] Gather user feedback
6. [ ] Iterate based on real-world usage
7. [ ] Update skill based on learnings

---

## Test Results Log

**Date:** 2026-02-26
**Version:** 1.0.0
**Status:** Implementation complete, ready for testing

### Test Run 1: [Date]
- Scenario 1: [PASS/FAIL] - Notes:
- Scenario 2: [PASS/FAIL] - Notes:
- Scenario 3: [PASS/FAIL] - Notes:
- Scenario 4: [PASS/FAIL] - Notes:

### Observations:
[Record real-world usage observations here]

### Improvements Needed:
[List any refinements to the skill based on testing]
