#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "jsonschema>=4.20.0",
# ]
# ///

"""
Context Handoff Validation Utilities

This script provides validated JSON read/write operations for agent communication.
Use these functions to ensure all assignments and results conform to schemas.

Usage:
    from context_handoff import write_assignment, read_assignment, write_result, read_result

Examples:
    # Write a validated assignment
    assignment = {
        "assignment_type": "implementation",
        "issue_id": "LIN-123",
        "task": {"summary": "Implement rate limiting"},
        "acceptance_criteria": ["Rate limit applied", "Returns 429 on limit"],
        "expected_output": {
            "result_path": ".agents/session-x/results/01-result.json",
            "format": "implementation_result",
            "required_fields": ["status", "summary"]
        }
    }
    write_assignment(".agents/session-x/assignments/01.json", assignment)

    # Read and validate
    assignment = read_assignment(".agents/session-x/assignments/01.json")
"""

import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import validate, ValidationError


# Path to schemas directory
SCHEMAS_DIR = Path(__file__).parent / "schemas"


def load_schema(schema_name: str) -> dict[str, Any]:
    """Load a JSON schema from the schemas directory."""
    schema_path = SCHEMAS_DIR / f"{schema_name}.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    
    with open(schema_path) as f:
        return json.load(f)


def validate_json(data: dict[str, Any], schema_name: str) -> None:
    """
    Validate JSON data against a schema.
    
    Args:
        data: JSON data to validate
        schema_name: Name of schema file (without .json extension)
    
    Raises:
        ValidationError: If validation fails
    """
    schema = load_schema(schema_name)
    validate(instance=data, schema=schema)


def write_json_validated(
    path: str | Path,
    data: dict[str, Any],
    schema_name: str,
    create_dirs: bool = True
) -> None:
    """
    Write JSON data to file after validating against schema.
    
    Args:
        path: Path to write to
        data: JSON data to write
        schema_name: Schema to validate against
        create_dirs: Whether to create parent directories
    
    Raises:
        ValidationError: If data doesn't match schema
    """
    # Validate before writing
    validate_json(data, schema_name)
    
    path = Path(path)
    
    # Create parent directories if needed
    if create_dirs:
        path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to file
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def read_json_validated(path: str | Path, schema_name: str) -> dict[str, Any]:
    """
    Read and validate JSON data from file.
    
    Args:
        path: Path to read from
        schema_name: Schema to validate against
    
    Returns:
        Validated JSON data
    
    Raises:
        FileNotFoundError: If file doesn't exist
        ValidationError: If data doesn't match schema
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path) as f:
        data = json.load(f)
    
    # Validate after reading
    validate_json(data, schema_name)
    
    return data


# Convenience functions for specific message types

def write_assignment(path: str | Path, assignment: dict[str, Any]) -> None:
    """Write a validated assignment file."""
    write_json_validated(path, assignment, "assignment")


def read_assignment(path: str | Path) -> dict[str, Any]:
    """Read and validate an assignment file."""
    return read_json_validated(path, "assignment")


def write_assignment_reference(path: str | Path, reference: dict[str, Any]) -> None:
    """Write a validated assignment reference."""
    write_json_validated(path, reference, "assignment_reference")


def read_assignment_reference(path: str | Path) -> dict[str, Any]:
    """Read and validate an assignment reference."""
    return read_json_validated(path, "assignment_reference")


def write_result(path: str | Path, result: dict[str, Any]) -> None:
    """Write a validated result file."""
    write_json_validated(path, result, "result")


def read_result(path: str | Path) -> dict[str, Any]:
    """Read and validate a result file."""
    return read_json_validated(path, "result")


def create_result_reference(
    result_path: str,
    result_type: str,
    status: str,
    summary: str,
    requires_attention: bool = False,
    attention_reason: str | None = None,
    decision: str | None = None
) -> dict[str, Any]:
    """
    Create a validated result reference.
    
    This is what agents return to coordinators - lightweight reference
    instead of full result.
    
    Args:
        result_path: Path to full result file
        result_type: Type of result (implementation, planning, review, knowledge_synthesis)
        status: Status (complete, blocked, needs_clarification, partial)
        summary: One sentence outcome (10-200 chars)
        requires_attention: Whether coordinator action needed
        attention_reason: Why attention is needed (required if requires_attention=True)
        decision: Review decision (for review results only)
    
    Returns:
        Validated result reference dict
    """
    reference = {
        "result_path": result_path,
        "result_type": result_type,
        "status": status,
        "summary": summary,
        "requires_attention": requires_attention,
        "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z")
    }
    
    if attention_reason:
        reference["attention_reason"] = attention_reason
    
    if decision:
        reference["decision"] = decision
    
    # Validate before returning
    validate_json(reference, "result_reference")
    
    return reference


def create_session_directory(session_id: str, base_dir: str = ".agents") -> Path:
    """
    Create directory structure for a new session.
    
    Args:
        session_id: Session identifier (e.g., "session-20241210-143022-implement-auth")
        base_dir: Base directory for agent files
    
    Returns:
        Path to session directory
    """
    session_dir = Path(base_dir) / session_id
    
    # Create subdirectories
    (session_dir / "assignments").mkdir(parents=True, exist_ok=True)
    (session_dir / "results").mkdir(parents=True, exist_ok=True)
    (session_dir / "escalations").mkdir(parents=True, exist_ok=True)
    
    # Create empty metadata file
    metadata = {
        "session_id": session_id,
        "created_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "status": "active"
    }
    
    metadata_path = session_dir / "metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    return session_dir


def generate_session_id(workflow_name: str) -> str:
    """
    Generate a session ID with timestamp and workflow name.
    
    Args:
        workflow_name: Name of workflow (e.g., "implement-auth")
    
    Returns:
        Session ID string (e.g., "session-20241210-143022-implement-auth")
    """
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    return f"session-{timestamp}-{workflow_name}"


# CLI for testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Validate file:  uv run context_handoff.py validate <schema_name> <file_path>")
        print("  Create session: uv run context_handoff.py create-session <workflow_name>")
        print("\nExamples:")
        print("  uv run context_handoff.py validate assignment .agents/session-x/assignments/01.json")
        print("  uv run context_handoff.py create-session implement-auth")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "validate":
        if len(sys.argv) != 4:
            print("Usage: uv run context_handoff.py validate <schema_name> <file_path>")
            sys.exit(1)
        
        schema_name = sys.argv[2]
        file_path = sys.argv[3]
        
        try:
            data = read_json_validated(file_path, schema_name)
            print(f"✅ Valid {schema_name}: {file_path}")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Summary: {data.get('summary', data.get('task', {}).get('summary', 'N/A'))}")
        except ValidationError as e:
            print(f"❌ Validation failed: {e.message}")
            print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"❌ File not found: {e}")
            sys.exit(1)
    
    elif command == "create-session":
        if len(sys.argv) != 3:
            print("Usage: uv run context_handoff.py create-session <workflow_name>")
            sys.exit(1)
        
        workflow_name = sys.argv[2]
        session_id = generate_session_id(workflow_name)
        session_dir = create_session_directory(session_id)
        
        print(f"✅ Created session: {session_id}")
        print(f"   Directory: {session_dir}")
        print(f"   Assignments: {session_dir / 'assignments'}")
        print(f"   Results: {session_dir / 'results'}")
        print(f"   Escalations: {session_dir / 'escalations'}")
        print(f"   Metadata: {session_dir / 'metadata.json'}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
