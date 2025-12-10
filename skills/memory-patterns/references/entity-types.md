# Memory Entity Types Quick Reference

## Entity Types

| Type | Purpose | When to Create |
|------|---------|----------------|
| `branch` | Track branch purpose and status | Starting new branch/worktree |
| `feature_implementation` | Document completed features | After feature completion |
| `architectural_decision` | Record design choices (ADRs) | When making significant decisions |
| `learning` | Capture patterns and gotchas | When discovering valuable insights |
| `orchestration_pattern` | Multi-agent workflow patterns | When patterns emerge in coordination |
| `fragility_note` | Areas needing careful handling | When identifying risky areas |
| `project_context` | High-level project information | Project setup or major changes |
| `business_context` | Business requirements and processes | When documenting business alignment |

## Required Fields (All Types)

```
date_added: YYYY-MM-DD
date_updated: YYYY-MM-DD
```

## Type-Specific Fields

### branch
```
purpose: Why this branch exists
goals: [List of goals]
linear_issue: LIN-XXX (if applicable)
status: active|merged|abandoned
worktree_path: Path if using worktree
```

### feature_implementation
```
description: What was implemented
branch: Branch name
linear_issue: LIN-XXX
use_cases: [List of use cases]
limitations: [Known limitations]
architectural_impact: How it affects architecture
alternatives_considered: [Other approaches evaluated]
verification: How to verify it works
```

### architectural_decision
```
decision: What was decided
context: Why decision was needed
rationale: Why this choice
tradeoffs: [Accepted tradeoffs]
affected_components: [Components impacted]
supersedes: Previous decision if any
```

### learning
```
category: implementation_pattern|gotcha|best_practice|anti_pattern
title: Short descriptive title
description: Detailed explanation
applies_to: [Relevant areas/tags]
source_issue: Where discovered
confidence: high|medium|low
```

### orchestration_pattern
```
pattern_type: success|failure|improvement
title: Pattern name
description: What the pattern is
applies_to: [Which agents/workflows]
discovered_in: Source context
recommendation: How to apply
```

### fragility_note
```
component: Affected component path
issue: What the fragility is
trigger: What causes problems
mitigation: How to handle safely
affected_by_changes_to: [Related components]
severity: high|medium|low
```

## Relation Types

| Relation | From → To | Use Case |
|----------|-----------|----------|
| `modifies` | feature → component | Feature changes component |
| `implements` | feature → decision | Feature implements ADR |
| `supersedes` | new_decision → old | Decision replacement |
| `applies_to` | learning → component | Learning relevance |
| `related_to` | any → any | General association |
| `discovered_in` | learning → issue | Learning source |
| `depends_on` | component → component | Dependencies |

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| branch | `{type}/{feature-name}` | `implement/user-auth` |
| feature_implementation | `{feature-name}-implementation` | `user-auth-jwt-implementation` |
| architectural_decision | `adr-{number}-{short-name}` | `adr-001-jwt-over-sessions` |
| learning | `learning-{topic}` | `learning-async-db-pooling` |
| orchestration_pattern | `pattern-{name}` | `pattern-focused-context` |
| fragility_note | `fragile-{component}-{issue}` | `fragile-payment-webhook-order` |
