# Context Handoff Skill - Validation Utilities

This directory contains the context-handoff skill with JSON schema validation.

## Files

- **`SKILL.md`** - Complete specification of file-based agent communication patterns
- **`reference.md`** - Quick reference guide for agents
- **`context_handoff.py`** - UV script with validation utilities
- **`schemas/`** - JSON schemas for all message types
- **`example.py`** - Working example demonstrating the full workflow
- **`test_validation.py`** - Validation error handling examples

## Quick Start

### 1. Create a Session

```bash
uv run context_handoff.py create-session my-workflow
```

This creates:
```
.agents/session-{timestamp}-my-workflow/
  ├── assignments/
  ├── results/
  ├── escalations/
  └── metadata.json
```

### 2. Use in Python

```python
from context_handoff import (
    write_assignment,
    read_assignment,
    write_result,
    create_result_reference,
    generate_session_id,
    create_session_directory
)

# Create session
session_id = generate_session_id("implement-auth")
session_dir = create_session_directory(session_id)

# Write validated assignment
assignment = {
    "assignment_type": "implementation",
    "issue_id": "LIN-123",
    "task": {"summary": "Implement rate limiting on auth endpoint"},
    "acceptance_criteria": ["Rate limit applied", "Returns 429 on exceed"],
    "expected_output": {
        "result_path": f".agents/{session_id}/results/01.json",
        "format": "implementation_result",
        "required_fields": ["status", "summary"]
    }
}

write_assignment(f".agents/{session_id}/assignments/01.json", assignment)

# Agent reads and validates
assignment = read_assignment(f".agents/{session_id}/assignments/01.json")

# Agent writes result
result = {
    "result_type": "implementation",
    "issue_id": "LIN-123",
    "status": "complete",
    "summary": "Rate limiting implemented successfully",
    # ... more fields
}

write_result(f".agents/{session_id}/results/01.json", result)

# Agent returns lightweight reference
result_ref = create_result_reference(
    result_path=f".agents/{session_id}/results/01.json",
    result_type="implementation",
    status="complete",
    summary="Rate limiting implemented successfully",
    requires_attention=False
)
```

### 3. Validate Existing Files

```bash
# Validate an assignment file
uv run context_handoff.py validate assignment .agents/session-x/assignments/01.json

# Validate a result file
uv run context_handoff.py validate result .agents/session-x/results/01.json
```

## Examples

### Run the Complete Example

```bash
uv run example.py
```

This demonstrates:
1. Coordinator creating a session and assignment
2. Agent receiving, processing, and writing result
3. Coordinator receiving lightweight reference
4. Context savings calculation (94% reduction!)

### Test Validation

```bash
uv run test_validation.py
```

Shows how validation catches errors with clear messages.

## JSON Schemas

All schemas are in `schemas/`:

- **`assignment.json`** - Task assignments to agents
- **`result.json`** - Full results from agents
- **`result_reference.json`** - Lightweight result references
- **`assignment_reference.json`** - Lightweight assignment references

## Benefits

### 1. Schema Enforcement
- **Validation at write time** catches errors early
- Required fields enforced automatically
- Type checking for all fields
- Format validation (e.g., issue IDs, timestamps)

### 2. Context Reduction
- **94% reduction** in coordinator context usage
- Pass references (~100 tokens) instead of full content (~2500 tokens)
- For 10 agents: ~23K tokens saved!

### 3. Observability
- All communication persisted to files
- Complete audit trail
- Easy debugging and replay
- Can inspect workflow at any point

### 4. Type Safety
- Clear contracts between agents
- IDE autocomplete support
- Prevents common errors

## Integration with Agents

Agents should use these utilities in their implementation:

```python
# At the start of your agent
from context_handoff import read_assignment, write_result, create_result_reference

# Read assignment
assignment = read_assignment(assignment_path)

# Do work...

# Write result
write_result(result_path, result_data)

# Return reference
return create_result_reference(
    result_path=result_path,
    result_type="implementation",
    status="complete",
    summary="Brief outcome description",
    requires_attention=False
)
```

## Dependencies

The UV script automatically manages dependencies:
- `jsonschema>=4.20.0` - JSON schema validation

No manual installation needed - UV handles everything!

## See Also

- **SKILL.md** - Full specification with all patterns and formats
- **reference.md** - Quick reference for common operations
