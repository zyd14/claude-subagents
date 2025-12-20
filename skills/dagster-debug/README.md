# Dagster Debug Skill

A comprehensive Claude skill for debugging failed or erroneous Dagster jobs using the Dagster GraphQL API.

## Overview

This skill provides tools and patterns for systematically investigating Dagster run failures, asset materialization errors, and pipeline execution issues. It includes Python scripts for querying the Dagster GraphQL API and detailed documentation of debugging workflows.

## Quick Start

### Prerequisites

- Python 3.10+
- Access to a Dagster instance (local or Dagster Cloud)
- API token (for Dagster Cloud)

### Installation

The scripts use inline script dependencies (PEP 723), so they can be run with `uv` or directly with Python after installing dependencies:

```bash
# Using uv (recommended)
uv run scripts/get_run_info.py --run-id <run-id>

# Or install dependencies manually
pip install dagster-graphql gql
python scripts/get_run_info.py --run-id <run-id>
```

### Basic Usage

1. **Get run information:**
   ```bash
   python scripts/get_run_info.py --run-id abc123-def456
   ```

2. **Get event logs with failures:**
   ```bash
   python scripts/get_run_logs.py --run-id abc123-def456 --event-type FAILURE
   ```

3. **Get run statistics:**
   ```bash
   python scripts/get_run_stats.py --run-id abc123-def456
   ```

4. **Get all runs for a job:**
   ```bash
   python scripts/get_job_runs.py --job-name my_job
   ```

## Files

- **SKILL.md** - Main skill documentation with debugging patterns and workflows
- **reference.md** - Comprehensive reference for event types, error patterns, and advanced techniques
- **scripts/dagster_client.py** - Reusable GraphQL client library
- **scripts/get_run_info.py** - Get basic run metadata
- **scripts/get_run_logs.py** - Retrieve and filter event logs
- **scripts/get_run_stats.py** - Get run statistics
- **scripts/get_job_runs.py** - Get all runs for a job

## Features

- **Systematic Debugging Workflows** - Step-by-step processes for investigating failures
- **Event Log Analysis** - Filter and analyze Dagster event logs
- **Error Pattern Recognition** - Common error patterns and their solutions
- **GraphQL Query Library** - Pre-built queries for common debugging tasks
- **Script Automation** - Python scripts for querying Dagster API
- **Comprehensive Documentation** - Detailed reference for event types and debugging techniques

## Configuration

All scripts support the following configuration options:

### Environment Variables

```bash
export DAGSTER_URL="https://myorg.dagster.cloud/prod"
export DAGSTER_CLOUD_TOKEN="your-api-token"
export DAGSTER_CLOUD_ORG="myorg"
```

### Command Line Options

```bash
--url <dagster-url>          # Dagster instance URL
--token <api-token>          # API token for Dagster Cloud
--deployment <deployment>    # Dagster Cloud deployment name
```

## Examples

### Local Dagster Instance

```bash
python scripts/get_run_info.py --run-id abc123
python scripts/get_run_logs.py --run-id abc123 --event-type FAILURE
```

### Dagster Cloud

```bash
python scripts/get_run_info.py \
    --run-id abc123 \
    --url https://myorg.dagster.cloud/prod \
    --token $DAGSTER_CLOUD_TOKEN

# Or using deployment name
python scripts/get_run_info.py \
    --run-id abc123 \
    --deployment prod
```

### Filtering and Analysis

```bash
# Get specific event types
python scripts/get_run_logs.py --run-id abc123 \
    --event-type "STEP_FAILURE,PIPELINE_FAILURE,ASSET_MATERIALIZATION"

# Get logs for a specific step
python scripts/get_run_logs.py --run-id abc123 \
    --step-key my_asset_name

# Get only failed runs
python scripts/get_job_runs.py --job-name my_job \
    --status FAILURE

# Output as JSON for further processing
python scripts/get_run_logs.py --run-id abc123 --json | jq '.events[] | select(.level == "ERROR")'
```

## Common Debugging Scenarios

### Scenario 1: Job Failed - Unknown Cause

```bash
# 1. Get run info
python scripts/get_run_info.py --run-id <run-id>

# 2. Get failure events
python scripts/get_run_logs.py --run-id <run-id> --event-type FAILURE

# 3. Check run stats
python scripts/get_run_stats.py --run-id <run-id>
```

### Scenario 2: Asset Materialization Failed

```bash
# Get asset-related events
python scripts/get_run_logs.py --run-id <run-id> \
    --event-type "ASSET_MATERIALIZATION,STEP_FAILURE,HANDLED_OUTPUT"
```

### Scenario 3: Investigating a Pattern of Failures

```bash
# Get recent runs
python scripts/get_job_runs.py --job-name my_job --status FAILURE

# Compare with successful runs
python scripts/get_job_runs.py --job-name my_job --status SUCCESS
```

## Documentation

- **SKILL.md** - Main documentation with:
  - Debugging workflows
  - Common scenarios
  - GraphQL API reference
  - Error patterns and solutions
  - Best practices

- **reference.md** - Comprehensive reference with:
  - Complete event type listing
  - Detailed error patterns
  - Advanced techniques
  - GraphQL query examples
  - Custom filtering scripts

## Contributing

To extend this skill:

1. Add new GraphQL queries to `scripts/dagster_client.py`
2. Create new scripts following the existing pattern
3. Document new workflows in `SKILL.md`
4. Add examples to `reference.md`

## License

This skill is part of the claude-subagents project.
