---
name: context-handoff
description: Structured patterns for passing context between agents, phases, and workflows. Ensures clear communication with minimal overhead through standardized JSON formats and focused context principles. Use when needing to manage communication between multiple agents.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Context Handoff Skill

This skill provides patterns for efficient context transfer between agents, workflow phases, and systems. Good context handoff is critical for multi-agent coordination - too little context causes errors, too much wastes tokens and confuses focus.

## When to Use This Skill

- Assigning work to subagents
- Passing results between workflow phases
- Documenting work for future reference
- Summarizing outcomes for parent coordinators

## Core Principles

1. **Minimal sufficient context** - Include only what's needed for the task
2. **Structured formats** - Use consistent JSON schemas
3. **Clear expectations** - Always specify expected outputs
4. **Single focus** - One task per handoff
5. **Explicit boundaries** - State what's in scope and out of scope

## Context Budget Guidelines

| Handoff Type | Target Budget | Includes |
|--------------|---------------|----------|
| Task assignment | <2000 tokens | Task, criteria, constraints, 2-3 learnings |
| Result return | <1500 tokens | Status, summary, divergences, artifacts |
| Phase transition | <1000 tokens | Phase summary, next phase inputs |
| Error escalation | <1000 tokens | Error, context, attempted solutions |

## Assignment Formats

### Standard Task Assignment

Use this format when assigning work to an implementation agent:

```json
{
  "assignment_type": "implementation",
  "issue_id": "LIN-123",
  "task": {
    "summary": "One sentence describing what to implement",
    "description": "2-3 sentences of additional context if needed"
  },
  "acceptance_criteria": [
    "Specific, testable criterion 1",
    "Specific, testable criterion 2",
    "Specific, testable criterion 3"
  ],
  "constraints": [
    "Technical constraint or limitation",
    "Style/pattern to follow"
  ],
  "relevant_context": {
    "files": ["path/to/relevant/file.py"],
    "dependencies": ["LIN-122 must be complete"],
    "learnings": ["Relevant insight from past work"]
  },
  "expected_output": {
    "format": "implementation_result",
    "required_fields": ["status", "summary", "artifacts"],
    "status_values": ["complete", "blocked", "needs_clarification"]
  },
  "scope_boundaries": {
    "in_scope": ["What should be done"],
    "out_of_scope": ["What should NOT be done"]
  }
}
```

### Planning Assignment

Use this format when requesting architectural planning:

```json
{
  "assignment_type": "planning",
  "issue_id": "LIN-100",
  "objective": {
    "summary": "What needs to be planned",
    "success_criteria": ["How we know the plan is good"]
  },
  "context": {
    "background": "Why this work is needed",
    "constraints": ["Technical constraints", "Timeline constraints"],
    "existing_patterns": ["Patterns to follow or reference"]
  },
  "expected_output": {
    "format": "implementation_plan",
    "required_fields": ["approach", "sub_tasks", "dependencies", "risks"],
    "sub_task_fields": ["task", "description", "acceptance_criteria", "estimate"]
  }
}
```

### Review Assignment

Use this format when requesting code review:

```json
{
  "assignment_type": "review",
  "issue_id": "LIN-123",
  "review_scope": {
    "summary": "What was implemented",
    "artifacts": ["path/to/changed/file.py"],
    "pr_link": "https://github.com/..."
  },
  "acceptance_criteria": [
    "Original criterion 1",
    "Original criterion 2"
  ],
  "review_focus": [
    "Specific concern to evaluate",
    "Pattern compliance to check"
  ],
  "expected_output": {
    "format": "review_result",
    "required_fields": ["decision", "summary", "feedback"],
    "decision_values": ["approved", "approved_with_suggestions", "changes_required", "rejected"]
  }
}
```

### Knowledge Synthesis Assignment

Use this format when invoking post-project learning extraction:

```json
{
  "assignment_type": "knowledge_synthesis",
  "parent_issue_id": "LIN-100",
  "project_summary": "Brief project description",
  "completion_status": "delivered",
  "data": {
    "sub_issues": ["LIN-101", "LIN-102", "LIN-103"],
    "divergences": ["All documented divergences"],
    "review_feedback": ["All review outcomes"],
    "blockers_encountered": ["All blockers and resolutions"]
  },
  "metrics": {
    "sub_issues_total": 12,
    "sub_issues_first_pass": 7,
    "avg_review_iterations": 1.4,
    "divergences_tracked": 6,
    "blockers_encountered": 2
  },
  "notes": "Notable observations for learning extraction"
}
```

## Result Formats

### Implementation Result

Agents return this after completing implementation work:

```json
{
  "result_type": "implementation",
  "issue_id": "LIN-123",
  "status": "complete",
  "summary": "Brief description of what was done",
  "details": {
    "approach": "How the task was accomplished",
    "decisions": ["Key decision made and why"]
  },
  "artifacts": {
    "files_created": ["path/to/new/file.py"],
    "files_modified": ["path/to/changed/file.py"],
    "pr_link": "https://github.com/...",
    "commit": "abc123"
  },
  "divergences": [
    {
      "planned": "What was originally planned",
      "actual": "What was actually done",
      "rationale": "Why the change was made",
      "impact": "Effect on scope/timeline"
    }
  ],
  "blockers": [],
  "follow_up_needed": ["Any items requiring future attention"]
}
```

### Planning Result

Architects return this after creating implementation plans:

```json
{
  "result_type": "planning",
  "issue_id": "LIN-100",
  "plan": {
    "approach": "High-level implementation strategy",
    "rationale": "Why this approach was chosen"
  },
  "sub_tasks": [
    {
      "task": "Task title",
      "description": "What this task accomplishes",
      "acceptance_criteria": ["Criterion 1", "Criterion 2"],
      "dependencies": ["Other task IDs"],
      "estimate": "S/M/L",
      "technical_notes": "Implementation hints"
    }
  ],
  "dependencies": {
    "external": ["External system dependencies"],
    "internal": ["Task dependency graph"]
  },
  "risks": [
    {
      "risk": "What could go wrong",
      "likelihood": "low/medium/high",
      "mitigation": "How to address it"
    }
  ],
  "open_questions": ["Questions needing clarification"]
}
```

### Review Result

Reviewers return this after evaluating work:

```json
{
  "result_type": "review",
  "issue_id": "LIN-123",
  "decision": "approved_with_suggestions",
  "summary": "Overall assessment in 1-2 sentences",
  "criteria_assessment": [
    {
      "criterion": "Original acceptance criterion",
      "met": true,
      "notes": "How it was met or why not"
    }
  ],
  "feedback": [
    {
      "type": "required_change|suggestion|praise",
      "severity": "critical|major|minor|info",
      "location": "file:line or general",
      "description": "What the feedback is about",
      "suggestion": "How to address it"
    }
  ],
  "follow_up": {
    "requires_re_review": false,
    "items": ["Any follow-up items"]
  }
}
```

### Knowledge Synthesis Result

Knowledge synthesizer returns this after extracting learnings:

```json
{
  "result_type": "knowledge_synthesis",
  "parent_issue_id": "LIN-100",
  "learnings": [
    {
      "learning_id": "learning-auth-001",
      "category": "best-practice|gotcha|process-improvement|anti-pattern",
      "scope": "global|project-specific",
      "title": "Short descriptive title",
      "description": "Detailed explanation of the learning",
      "source_issues": ["LIN-102", "LIN-105"],
      "applies_to": ["relevant-tags"],
      "confidence": "high|medium|low"
    }
  ],
  "patterns": {
    "divergence_themes": ["Common divergence patterns"],
    "review_feedback_themes": ["Common review issues"],
    "success_factors": ["What worked well"]
  },
  "recommendations": [
    "Suggestions for future projects"
  ]
}
```

## Phase Transition Patterns

### Planning → Execution

```json
{
  "transition": "planning_to_execution",
  "parent_issue": "LIN-100",
  "planning_summary": {
    "approach": "Chosen implementation approach",
    "sub_issues_created": ["LIN-101", "LIN-102", "LIN-103"],
    "dependency_order": ["LIN-101", "LIN-102", "LIN-103"],
    "key_decisions": ["Decision 1", "Decision 2"]
  },
  "execution_inputs": {
    "first_task": "LIN-101",
    "loaded_learnings": ["Learning to apply during execution"],
    "risk_mitigations": ["Mitigation to keep in mind"]
  }
}
```

### Execution → Completion

```json
{
  "transition": "execution_to_completion",
  "parent_issue": "LIN-100",
  "execution_summary": {
    "sub_issues_completed": ["LIN-101", "LIN-102", "LIN-103"],
    "total_divergences": 2,
    "review_iterations": 1.3,
    "blockers_resolved": 1
  },
  "completion_inputs": {
    "artifacts_to_link": ["PR links", "Doc links"],
    "divergences_to_document": ["List of divergences"],
    "learnings_to_extract": ["Patterns observed"]
  }
}
```

## Error Escalation Format

When agents encounter issues they can't resolve:

```json
{
  "escalation_type": "blocker|clarification|scope_change",
  "issue_id": "LIN-123",
  "context": {
    "task": "What was being attempted",
    "progress": "How far work got before the issue"
  },
  "issue": {
    "description": "What the problem is",
    "attempted_solutions": ["What was tried"],
    "root_cause": "Best understanding of why this is happening"
  },
  "request": {
    "type": "decision|information|reassignment",
    "options": ["Option 1", "Option 2"],
    "recommendation": "Suggested path forward"
  }
}
```

## Validation

### Before Sending to Agent

- ✅ Required fields present
- ✅ Issue ID valid (if using Linear)
- ✅ Acceptance criteria are testable
- ✅ Context is focused and relevant
- ✅ Total token count <2000

### After Receiving from Agent

- ✅ Required fields present
- ✅ Status value is valid
- ✅ Divergences include rationale
- ✅ Artifacts list is complete
- ✅ Output matches expected format

### When Validation Fails

1. Log the malformed response
2. Request clarification with specific issue
3. Provide format example
4. Track as communication round

## Error Handling

### When agent returns "blocked" or "needs_clarification"

1. Switch to Recovery Mode (if in orchestration)
2. Diagnose the blocker
3. Provide additional context or escalate to user
4. Track resolution for learning

### When format is incorrect

1. Don't proceed with invalid data
2. Ask agent to reformat with specific guidance
3. If repeated failures, reassess task assignment

## Communication Efficiency

### Target Metrics

| Metric | Target | Red Flag |
|--------|--------|----------|
| Context size | <2000 tokens | >2500 tokens |
| Communication rounds | 1-2 per issue | >3 rounds |
| Clarification rate | <10% | >20% |
| Format violations | 0% | Any |

### Red Flags to Watch

- >3 communication rounds for single issue
- Agents requesting information already provided
- Frequent format violations
- Context size consistently >2500 tokens
- Repeated need for clarification

## Best Practices

### Do

- ✅ Always specify expected output format
- ✅ Include only task-relevant context
- ✅ Be explicit about scope boundaries
- ✅ Provide 2-3 relevant learnings maximum
- ✅ Use consistent field names across handoffs
- ✅ Include issue IDs for traceability
- ✅ Validate before sending and after receiving

### Don't

- ❌ Include full file contents (use paths instead)
- ❌ Send entire project history
- ❌ Leave expected outputs ambiguous
- ❌ Assign multiple unrelated tasks in one handoff
- ❌ Use inconsistent status values
- ❌ Omit acceptance criteria from assignments
- ❌ Proceed with invalid agent responses
