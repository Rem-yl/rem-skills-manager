# Refining Prompts Skill

## Overview

The `refining-prompts` skill transforms vague or incomplete user requests into clear, structured prompts using the **5C Framework**.

## Quick Start

**Invoke the skill:**
```
Use the refining-prompts skill
```

Or use the command wrapper:
```
/refine-prompt
```

## The 5C Framework

| C | What It Means | Example Question |
|---|---------------|------------------|
| **Context** | Project state, relevant files, existing patterns | "What files are involved?" |
| **Constraint** | Technical/business/time limitations | "What libraries must we use?" |
| **Clarity** | Specific, unambiguous, actionable language | "What exact behavior should change?" |
| **Criteria** | How success will be measured | "What tests should pass?" |
| **Completeness** | All necessary details provided | "What edge cases matter?" |

## When to Use

**Use when:**
- Request is vague ("improve performance", "fix the bug")
- Starting complex multi-step work
- No clear success criteria mentioned
- Previous attempts produced unclear results

**Skip when:**
- Request already clear and complete
- Simple single-step task
- Already in implementation phase

## Process

1. **Capture Intent** - Identify which Cs are missing
2. **Refine** - Ask targeted questions (one at a time, prefer multiple choice)
3. **Assemble** - Present structured prompt with all 5Cs
4. **Handoff** - Recommend next action (brainstorming/writing-plans/execute)

## Files

- **SKILL.md** - Main skill documentation with framework, process, techniques
- **examples.md** - 6 comprehensive before/after examples
- **README.md** - This quick reference

## Examples

See `examples.md` for detailed before/after transformations:
- Authentication feature request
- Bug fix with missing context
- Performance optimization
- Refactoring task
- UI responsiveness
- Form validation

## Integration

After refining a prompt:

→ **brainstorming** - If design decisions needed
→ **writing-plans** - If implementation with clear spec
→ **Direct execution** - If simple, single action

## Success Indicators

A refined prompt should:
- Be understandable by someone unfamiliar with the project
- Include specific file paths or clear discovery approach
- Define measurable success criteria
- Address constraints and edge cases
- Use precise, unambiguous language

## Quick Question Templates

**Context:** "Which files or components handle [X]?"
**Constraint:** "Are there technical requirements or limitations?"
**Clarity:** "What exact behavior should change?"
**Criteria:** "How will we know this works correctly?"
**Completeness:** "What edge cases should we handle?"

---

**Related Skills:**
- `brainstorming` - Explores design alternatives
- `writing-plans` - Creates implementation plans
- `elements-of-style:writing-clearly-and-concisely` - Applies clarity principles

**Command:** `/refine-prompt`
