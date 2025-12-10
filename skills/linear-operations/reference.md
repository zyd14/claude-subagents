# Linear Status Workflow Reference

## Standard Status Flow

```
Backlog → Todo → In Progress → In Review → Done
                      ↓
                   Blocked → (back to In Progress when unblocked)
```

## Status Definitions

| Status | When to Use | Next Actions |
|--------|-------------|--------------|
| **Backlog** | Identified but not scheduled | Prioritize and move to Todo |
| **Todo** | Ready to start, prioritized | Pick up and move to In Progress |
| **In Progress** | Actively being worked on | Complete and move to In Review |
| **In Review** | Implementation done, awaiting review | Process feedback or move to Done |
| **Blocked** | Cannot proceed, waiting on something | Resolve blocker, return to In Progress |
| **Done** | Complete and verified | Close or archive |

## Status Transition Rules

### Into In Progress
- Must have clear acceptance criteria
- Dependencies must be resolved
- Assignee must be set

### Into In Review
- All acceptance criteria addressed
- PR created (if code change)
- Summary comment added to issue

### Into Blocked
- Blocker clearly documented
- Impact assessed
- Resolution path identified (if known)

### Into Done
- All acceptance criteria verified
- Review approved
- Artifacts linked (PRs, commits)
- Divergences documented

## Common Anti-patterns

❌ **Stale In Progress** - Task sitting for days without updates
❌ **Premature Done** - Closed without verification
❌ **Undefined Blocked** - No blocker description
❌ **Review without Summary** - No context for reviewer
