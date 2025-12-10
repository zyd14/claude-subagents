# Context Token Budget Reference

## Budget Guidelines by Handoff Type

| Handoff Type | Target | Maximum | Notes |
|--------------|--------|---------|-------|
| Task Assignment | 1500 | 2000 | Include only task-relevant context |
| Result Return | 1000 | 1500 | Summary focus, details on request |
| Phase Transition | 800 | 1000 | Distilled insights only |
| Error Escalation | 600 | 1000 | Focus on actionable info |
| Review Request | 1200 | 1800 | Include criteria and artifacts |

## What to Include vs Exclude

### Always Include
- Issue ID for traceability if available
- Clear task description
- Acceptance criteria
- Expected output format
- Scope boundaries

### Include When Relevant
- 2-3 specific learnings (not generic advice)
- File paths (not file contents)
- Dependency references
- Technical constraints

### Never Include
- Full file contents (use paths)
- Entire project history
- Unrelated learnings
- Multiple unrelated tasks
- Verbose explanations

## Token Estimation Guide

| Content Type | Approximate Tokens |
|--------------|-------------------|
| Issue ID + title | 10-20 |
| One-line description | 15-30 |
| Acceptance criterion | 20-50 |
| File path | 10-30 |
| JSON structure (empty) | 50-100 |
| Learning/insight | 30-60 |
| Full paragraph | 50-150 |

## Compression Strategies

1. **Use references, not content** - "See src/auth/validator.py" not full file
2. **Summarize, don't transcript** - High-fidelity key decisions, not discussion
3. **List, don't prose** - Bullet points over paragraphs
4. **Relevant only** - What agent needs for THIS task
5. **Standard formats** - Consistent structure reduces confusion overhead
