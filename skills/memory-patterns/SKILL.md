---
name: memory-patterns
description: Patterns for using persistent memory (memory2 MCP) effectively. Covers what to store, when to query, entity schemas, and knowledge areas. Prevents transient data pollution while building valuable long-term knowledge. Use when persisting synthesized learnings.
allowed-tools: Read, Write, Edit, Glob, Grep, mcp__memory2__create_entities, mcp__memory2__create_relations, mcp__memory2__add_observations, mcp__memory2__delete_entities, mcp__memory2__delete_observations, mcp__memory2__delete_relations, mcp__memory2__read_graph, mcp__memory2__search_nodes, mcp__memory2__open_nodes
---

# Memory Patterns Skill

This skill provides patterns for using the `memory2` MCP server to build and maintain persistent knowledge. The goal is to accumulate valuable, long-term knowledge while avoiding pollution from transient working state.

## When to Use This Skill

- Starting a new branch or worktree
- Planning features (querying for relevant context)
- Completing implementations (documenting learnings)
- Building project/architectural knowledge
- Tracking multi-agent orchestration patterns

## Core Principles

1. **Persistent, not transient** - Only store knowledge valuable beyond the current session
2. **Query early, write late** - Read during planning, write at completion
3. **Structured entries** - Consistent fields enable effective querying
4. **Knowledge areas** - Organize by purpose (business, architecture, learnings, etc.)
5. **Always timestamp** - Include `date_added` and `date_updated`

## What TO Store

| Knowledge Area | Examples | Value |
|---------------|----------|-------|
| **Business context** | How feature relates to business requirements, process flows | Alignment & prioritization |
| **Project architecture** | High-level component structure, key design decisions | Onboarding & consistency |
| **Implementation learnings** | Patterns that worked, gotchas discovered | Avoiding repeated mistakes |
| **Orchestration patterns** | What worked/failed in multi-agent coordination | Improving workflows |
| **Recurring issues** | Fragile areas, common failure modes | Careful handling |
| **Branch purposes** | What each branch is for, related issue IDs | Coordination & cleanup |
| **Architectural decisions** | Why X was chosen over Y, tradeoffs accepted | Future decision-making |

## What NOT to Store

| Don't Store | Why | Where It Belongs |
|-------------|-----|------------------|
| Current task state | Transient | Working state in orchestrator |
| Detailed implementation progress | Changes frequently | Linear issue updates |
| Code diffs or file contents | Too granular | Git commits |
| Temporary blockers | Short-lived | Linear comments |
| Session-specific context | Not reusable | Conversation context |
| Raw conversation logs | Not structured knowledge | Nowhere (ephemeral) |

## Required Fields

**Every memory entry must include:**

```json
{
  "date_added": "2024-01-15",
  "date_updated": "2024-01-15"
}
```

Update `date_updated` whenever modifying existing memories.

## Entity Schemas

### Branch Memory

Create when starting a new branch or worktree:

```json
{
  "entity_type": "branch",
  "name": "implement/user-authentication",
  "observations": [
    "date_added: 2024-01-15",
    "purpose: Implement JWT-based user authentication",
    "goals: [Secure login, Token refresh, Session management]",
    "linear_issue: LIN-123",
    "status: active",
    "worktree_path: ../project-implement-auth"
  ]
}
```

### Feature Implementation Memory

Create when completing a feature:

```json
{
  "entity_type": "feature_implementation",
  "name": "user-authentication-jwt",
  "observations": [
    "date_added: 2024-01-20",
    "description: JWT-based authentication with refresh tokens",
    "branch: implement/user-authentication",
    "linear_issue: LIN-123",
    "use_cases: [User login, API authentication, Session persistence]",
    "limitations: [No OAuth support yet, Single device sessions only]",
    "architectural_impact: Added auth middleware to all API routes",
    "alternatives_considered: [Session-based auth (rejected: stateful), OAuth only (rejected: complexity)]",
    "verification: Run auth test suite, verify token refresh flow"
  ]
}
```

### Architectural Decision Memory

Create when making significant design choices:

```json
{
  "entity_type": "architectural_decision",
  "name": "adr-001-jwt-over-sessions",
  "observations": [
    "date_added: 2024-01-15",
    "decision: Use JWT tokens instead of server-side sessions",
    "context: Need stateless authentication for horizontal scaling",
    "rationale: JWTs enable stateless auth, better for microservices",
    "tradeoffs: [Larger request size, Can't revoke individual tokens easily]",
    "affected_components: [auth-service, api-gateway, user-service]",
    "supersedes: none"
  ]
}
```

### Learning Memory

Create when discovering valuable patterns or gotchas:

```json
{
  "entity_type": "learning",
  "name": "learning-async-db-connections",
  "observations": [
    "date_added: 2024-01-18",
    "category: implementation_pattern",
    "title: Always use connection pooling with async DB access",
    "description: Discovered that creating new connections per request caused connection exhaustion under load",
    "applies_to: [database, async, performance]",
    "source_issue: LIN-145",
    "confidence: high"
  ]
}
```

### Orchestration Pattern Memory

Create when discovering what works/doesn't in multi-agent workflows:

```json
{
  "entity_type": "orchestration_pattern",
  "name": "pattern-focused-agent-context",
  "observations": [
    "date_added: 2024-01-20",
    "pattern_type: success",
    "title: Keep agent context under 2000 tokens",
    "description: Agents perform better with focused context; including full project history caused confusion",
    "applies_to: [all_agents]",
    "discovered_in: LIN-100 implementation",
    "recommendation: Summarize previous phase outcomes, don't dump full history"
  ]
}
```

### Fragility Note Memory

Create when identifying areas needing careful handling:

```json
{
  "entity_type": "fragility_note",
  "name": "fragile-payment-webhook-ordering",
  "observations": [
    "date_added: 2024-01-22",
    "component: payment-service/webhooks",
    "issue: Webhooks can arrive out of order causing state corruption",
    "trigger: High volume of rapid transactions",
    "mitigation: Always check event timestamps, implement idempotency",
    "affected_by_changes_to: [payment-service, event-processor]",
    "severity: high"
  ]
}
```

## Query Patterns

### When Planning a Feature

Query for context about affected components:

```python
# Search for memories related to components you'll touch
mcp__memory2__search_nodes(query="auth-service")
mcp__memory2__search_nodes(query="user authentication")

# Look for architectural decisions in that area
mcp__memory2__search_nodes(query="architectural_decision auth")

# Check for fragility notes
mcp__memory2__search_nodes(query="fragility payment")

# Find relevant learnings
mcp__memory2__search_nodes(query="learning database async")
```

### When Starting a Branch

```python
# Create branch memory
mcp__memory2__create_entities(entities=[{
  "name": "implement/feature-name",
  "entityType": "branch",
  "observations": [
    "date_added: 2024-01-15",
    "purpose: ...",
    "linear_issue: LIN-XXX"
  ]
}])
```

### When Completing Work

```python
# Update branch status
mcp__memory2__add_observations(observations=[{
  "entityName": "implement/feature-name",
  "contents": [
    "date_updated: 2024-01-20",
    "status: merged",
    "outcome: Successfully implemented"
  ]
}])

# Create feature implementation memory
mcp__memory2__create_entities(entities=[{
  "name": "feature-name-implementation",
  "entityType": "feature_implementation",
  "observations": ["..."]
}])

# Create relations to affected components
mcp__memory2__create_relations(relations=[{
  "from": "feature-name-implementation",
  "to": "auth-service",
  "relationType": "modifies"
}])
```

## Workflow Integration

### In Orchestration Workflows

```
Planning Phase:
├── Query memory for relevant learnings
├── Query memory for architectural context
├── Query memory for fragility notes
└── Load into working state (DO NOT query again during execution)

Execution Phase:
├── Reference pre-loaded learnings
├── DO NOT query memory (overhead)
└── Track learnings to document later

Completion Phase:
├── Delegate to knowledge-synthesizer (preferred)
├── OR manually create structured memories
└── Update branch status
```

### In Implementation Workflows

```
Start:
├── Create branch memory
└── Query for relevant context

During:
├── No memory operations
└── Track notable learnings mentally

End:
├── Create feature implementation memory
├── Create learning memories (if significant discoveries)
├── Update branch memory status
└── Create relations to affected components
```

## Relation Types

Use these relation types for connecting entities:

| Relation | Meaning | Example |
|----------|---------|---------|
| `modifies` | Feature changes component | feature → component |
| `implements` | Feature implements decision | feature → ADR |
| `supersedes` | New decision replaces old | new_ADR → old_ADR |
| `applies_to` | Learning relevant to area | learning → component |
| `related_to` | General association | entity → entity |
| `discovered_in` | Where learning came from | learning → issue |
| `depends_on` | Architectural dependency | component → component |

## Best Practices

### Do

- ✅ Always include `date_added` and `date_updated`
- ✅ Query during planning, write at completion
- ✅ Use consistent entity types
- ✅ Create relations to build a knowledge graph
- ✅ Include `linear_issue` when applicable
- ✅ Document "why" not just "what"
- ✅ Update branch memories when status changes

### Don't

- ❌ Store working/transient state
- ❌ Query memory during execution phases
- ❌ Create memories for every small task
- ❌ Store code snippets or full file contents
- ❌ Forget to update `date_updated`
- ❌ Create orphan entities with no relations
- ❌ Use inconsistent naming patterns
