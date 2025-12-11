---
name: linear-operations
description: Patterns and best practices for interacting with Linear issue tracking. Provides structured approaches for creating issues, managing status, updating with summaries, and maintaining Linear as a source of truth. Use when tracking state for a Linear issue or retrieving issue or project context.
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, mcp__memory2__read_graph, mcp__memory2__search_nodes, mcp__memory2__open_nodes, mcp__linear2__list_comments, mcp__linear2__create_comment, mcp__linear2__get_document, mcp__linear2__list_documents, mcp__linear2__get_issue, mcp__linear2__list_issues, mcp__linear2__create_issue, mcp__linear2__update_issue, mcp__linear2__list_issue_statuses, mcp__linear2__get_issue_status, mcp__linear2__list_issue_labels, mcp__linear2__create_issue_label, mcp__linear2__get_project, mcp__linear2__update_project, mcp__linear2__list_project_labels, mcp__linear2__search_documentation, mcp__ide__getDiagnostics
---

# Linear Operations Skill

This skill provides patterns for effective Linear issue management in development workflows. Use these patterns when your workflow involves Linear for task tracking, whether for full project orchestration or lightweight issue updates.

## When to Use This Skill

- Creating or updating Linear issues programmatically
- Managing parent/child issue relationships
- Tracking implementation progress in Linear
- Documenting divergences and artifacts
- Maintaining Linear as source of truth for project state

## Core Principles

1. **Linear is the source of truth** - All project state should be reflected in issues
2. **Atomic issues** - Each issue represents one clear, completable unit of work
3. **Clear acceptance criteria** - Every issue has testable "done" conditions
4. **Document divergences** - Plan changes are logged with rationale
5. **Link artifacts** - All outputs (PRs, commits, docs) linked to issues

## Issue Creation Patterns

### Parent Issue Structure

Parent issues represent complete features or projects:

```markdown
## Objective
[Clear statement of what this project/feature achieves]

## Scope
- [Included item 1]
- [Included item 2]
- NOT included: [Explicit exclusion]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

## Technical Context
[Relevant technical constraints or decisions]

## Sub-issues
- [ ] LIN-XXX: [Sub-task 1]
- [ ] LIN-XXX: [Sub-task 2]
```

### Sub-issue Structure

Sub-issues are atomic, assignable work items:

```markdown
## Task
[One-sentence description of what to implement]

## Context
[Brief background - why this task exists, what it's part of]

## Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

## Technical Notes
[Implementation hints, constraints, or dependencies]

## Dependencies
- Blocked by: [LIN-XXX if applicable]
- Blocks: [LIN-XXX if applicable]
```

## Status Management

### Standard Status Flow

```
Backlog → Todo → In Progress → In Review → Done
                      ↓
                   Blocked
```

### Status Update Patterns

**Moving to In Progress:**
```
Starting work on this issue.
Approach: [Brief description of implementation approach]
```

**Moving to In Review:**
```
Implementation complete. Ready for review.

Summary:
- [What was implemented]
- [Key decisions made]

Artifacts:
- PR: [link]
- Files changed: [list]
```

**Moving to Blocked:**
```
Blocked by: [Description of blocker]
Waiting on: [What needs to happen]
Impact: [How this affects timeline/other work]
```

**Moving to Done:**
```
Completed and verified.

Final summary:
- [What was delivered]
- [Any divergences from original plan]

Artifacts:
- PR: [link]
- Commit: [hash]
```

## Comment Patterns

### Progress Update

```markdown
## Progress Update

**Status:** [On track / At risk / Blocked]
**Completed:** [What's done]
**Next:** [What's happening next]
**Blockers:** [Any blockers, or "None"]
```

### Divergence Documentation

When implementation differs from the original plan:

```markdown
## Plan Divergence

**Original plan:** [What was planned]
**Actual implementation:** [What was done instead]
**Rationale:** [Why the change was made]
**Impact:** [Effect on timeline, scope, or other issues]
**Approved by:** [If applicable]
```

### Review Feedback

```markdown
## Review Feedback

**Decision:** [Approved / Changes Required / Rejected]
**Summary:** [Brief overall assessment]

### Required Changes
1. [Change 1]
2. [Change 2]

### Suggestions (Optional)
- [Suggestion 1]
- [Suggestion 2]
```

## MCP Tool Reference

### Reading Issues

```python
# Get single issue with full details
mcp__linear2__get_issue(id="LIN-123")

# List issues with filters
mcp__linear2__list_issues(
    project="project-name",
    state="in_progress",
    assignee="user-id"
)
```

### Creating Issues

```python
# Create sub-issue linked to parent
mcp__linear2__create_issue(
    title="Implement user validation",
    description="[Markdown description]",
    team="team-id",
    project="project-id",
    parentId="parent-issue-id",
    state="todo",
    labels=["backend", "auth"]
)
```

### Updating Issues

```python
# Update issue status and add comment
mcp__linear2__update_issue(
    id="LIN-123",
    state="in_progress"
)

mcp__linear2__create_comment(
    issueId="LIN-123",
    body="Starting implementation. Approach: ..."
)
```

## Best Practices

### Do

- ✅ Create issues before starting work
- ✅ Update status when it changes
- ✅ Document all divergences from plan
- ✅ Link all artifacts (PRs, commits, docs)
- ✅ Keep descriptions concise but complete
- ✅ Use labels consistently
- ✅ Close issues only when verified complete

### Don't

- ❌ Leave issues in stale states
- ❌ Make changes without updating Linear
- ❌ Create issues without acceptance criteria
- ❌ Let scope creep without documenting
- ❌ Close parent before all children complete
- ❌ Use Linear for ephemeral notes (use comments for updates)

## Integration with Workflows

This skill can be used by:

- **Full orchestration workflows** - Creating and managing all project issues
- **Lightweight workflows** - Just updating existing issues with progress
- **Review workflows** - Adding review feedback to issues
- **Planning workflows** - Creating issue structure from plans

When a workflow doesn't need Linear, simply don't invoke this skill's patterns.
