---
name: dagster-debug
description: Debug failed or erroneous Dagster jobs through GraphQL API queries, event log analysis, and systematic troubleshooting. Use when investigating Dagster run failures, asset materialization errors, or pipeline execution issues.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Dagster Debug Skill

This skill provides comprehensive patterns and tools for debugging failed or erroneous Dagster jobs using the Dagster GraphQL API.

## Overview

When Dagster jobs fail, you need to:
1. Identify the failed run and understand its status
2. Retrieve and analyze event logs to find the root cause
3. Examine step-level failures and error messages
4. Review asset materialization failures
5. Investigate configuration and environment issues

This skill provides scripts and patterns to systematically debug Dagster runs using the GraphQL API.

## Quick Start

### When to Use This Skill

- **Run failures**: A Dagster job/run has failed and you need to investigate why
- **Asset materialization errors**: Assets are not materializing or failing during materialization
- **Step-level failures**: Specific steps in a pipeline are failing
- **Event log analysis**: Need to review detailed event logs for a run
- **Performance issues**: Investigating slow or hanging runs

### Prerequisites

- Dagster instance URL (local or Dagster Cloud)
- API token (for Dagster Cloud deployments)
- Run ID or job name to investigate

## Core Debugging Workflow

### 1. Get Run Status and Metadata

Start by retrieving basic information about the run:

```python
# See scripts/get_run_info.py
# Retrieves: run status, start/end times, job name, configuration
```

**Key Information to Gather:**
- Run ID
- Run status (FAILURE, SUCCESS, STARTED, etc.)
- Job/pipeline name
- Start and end timestamps
- Run configuration

### 2. Retrieve Event Logs

Get detailed event logs to understand what happened during execution:

```python
# See scripts/get_run_logs.py
# Retrieves: all events with timestamps, levels, messages, step keys
```

**Event Types to Look For:**
- `STEP_FAILURE`: Step-level failures with error details
- `PIPELINE_FAILURE`: Overall pipeline failure
- `ASSET_MATERIALIZATION`: Successful asset materializations
- `STEP_SUCCESS`: Successful step completions
- `EXECUTION_STEP_START`: Step execution start times
- `LOGS_CAPTURED`: Captured log messages
- `RUN_FAILURE`: Run-level failure information

### 3. Analyze Failure Events

Focus on failure events to identify root causes:

```python
# Filter events by type
failure_events = [e for e in events if 'FAILURE' in e.get('eventType', '')]

# Common failure patterns:
# - Import errors: Check for module/package issues
# - Configuration errors: Verify run config and resource definitions
# - Resource errors: Check database connections, API credentials
# - Data errors: Validate input data format and quality
# - Timeout errors: Review step execution times
```

### 4. Check Step Statistics

Examine which steps failed and their execution details:

```python
# See scripts/get_run_stats.py
# Retrieves: step keys to execute, steps failed, execution statistics
```

## Common Debugging Scenarios

### Scenario 1: Job Failed - Unknown Cause

**Steps:**
1. Get run info to check status and timestamps
2. Retrieve all event logs for the run
3. Filter for FAILURE events
4. Review error messages and stack traces
5. Identify the failing step or asset

**Script Usage:**
```bash
# Get run info
python scripts/get_run_info.py --run-id <run-id> --url <dagster-url> --token <token>

# Get event logs with failures only
python scripts/get_run_logs.py --run-id <run-id> --event-type FAILURE --url <dagster-url> --token <token>
```

### Scenario 2: Asset Materialization Failed

**Common Causes:**
- IO Manager errors (storage/database issues)
- Data validation failures
- Resource initialization failures
- Upstream dependency failures

**Investigation Steps:**
1. Check for ASSET_MATERIALIZATION events
2. Review IO manager logs (HANDLED_OUTPUT events)
3. Examine upstream asset status
4. Verify resource configurations

**Script Usage:**
```bash
# Get asset-related events
python scripts/get_run_logs.py --run-id <run-id> --event-type "ASSET_MATERIALIZATION,STEP_FAILURE" --url <dagster-url> --token <token>
```

### Scenario 3: Specific Step is Failing

**Steps:**
1. Get run stats to see which steps were executed
2. Filter event logs by step key
3. Review step-specific error messages
4. Check step inputs and configuration

**Script Usage:**
```bash
# Get logs for a specific step
python scripts/get_run_logs.py --run-id <run-id> --step-key <step-name> --url <dagster-url> --token <token>
```

### Scenario 4: Job Runs for a Pipeline Show Pattern of Failures

**Steps:**
1. Get all runs for a job/pipeline
2. Analyze failure patterns across runs
3. Compare configurations between successful and failed runs
4. Identify environmental or data-related issues

**Script Usage:**
```bash
# Get all runs for a job
python scripts/get_job_runs.py --job-name <job-name> --url <dagster-url> --token <token>
```

## GraphQL API Reference

### Key Queries

#### Get Run Information
```graphql
query GetRun($runId: ID!) {
  runOrError(runId: $runId) {
    __typename
    ... on Run {
      id
      status
      pipelineName
      startTime
      endTime
      runConfigYaml
    }
    ... on RunNotFoundError {
      message
    }
    ... on PythonError {
      message
      stack
    }
  }
}
```

#### Get Event Logs
```graphql
query LogsForRun($runId: ID!, $limit: Int, $afterCursor: String) {
  logsForRun(runId: $runId, limit: $limit, afterCursor: $afterCursor) {
    __typename
    ... on EventConnection {
      events {
        __typename
        ... on MessageEvent {
          runId
          message
          timestamp
          level
          stepKey
          eventType
        }
      }
      cursor
      hasMore
    }
    ... on PythonError {
      message
      stack
    }
    ... on RunNotFoundError {
      message
    }
  }
}
```

#### Get Run Stats
```graphql
query RunStats($runIds: [String]) {
  runsOrError(filter: {runIds: $runIds}) {
    __typename
    ... on Runs {
      results {
        runId
        stepKeysToExecute
        stats {
          ... on RunStatsSnapshot {
            stepsFailed
          }
        }
      }
    }
  }
}
```

#### Get Job Runs
```graphql
query JobRuns($pipelineName: String) {
  runsOrError(filter: {pipelineName: $pipelineName}) {
    __typename
    ... on Runs {
      results {
        runId
        jobName
        status
        startTime
        endTime
      }
    }
  }
}
```

## Error Patterns and Solutions

### Pattern: Import Errors

**Symptoms:**
- `ModuleNotFoundError` or `ImportError` in logs
- Run fails immediately at start
- STEP_FAILURE events early in execution

**Common Causes:**
- Missing dependencies in environment
- Incorrect Python path
- Package version conflicts

**Investigation:**
1. Check STEP_FAILURE messages for import errors
2. Verify environment and package versions
3. Review Dockerfile or requirements files

### Pattern: Resource Initialization Failures

**Symptoms:**
- RESOURCE_INIT_FAILURE events
- Errors mentioning database connections, APIs, or external services
- Failures before any steps execute

**Common Causes:**
- Invalid credentials or tokens
- Network connectivity issues
- Resource configuration errors

**Investigation:**
1. Look for RESOURCE_INIT events
2. Check resource configuration in run config
3. Verify credentials and connection strings
4. Test external service availability

### Pattern: Data Validation Errors

**Symptoms:**
- STEP_FAILURE with data-related error messages
- Failures during asset materialization
- Type errors or constraint violations

**Common Causes:**
- Unexpected data format from upstream
- Schema changes in source data
- Data quality issues

**Investigation:**
1. Check STEP_OUTPUT events for data shapes
2. Review upstream asset materializations
3. Examine input data samples
4. Verify schema definitions

### Pattern: Timeout or Hanging Runs

**Symptoms:**
- Run never completes
- Long execution times
- STEP_START without corresponding STEP_SUCCESS

**Common Causes:**
- Infinite loops or deadlocks
- External service delays
- Resource exhaustion

**Investigation:**
1. Check step execution durations
2. Look for STEP_START without STEP_SUCCESS
3. Review resource utilization
4. Check for blocking operations

## Best Practices

### 1. Systematic Investigation

- **Start broad, then narrow**: Get run info → event logs → specific failures
- **Follow the timeline**: Review events chronologically
- **Check upstream**: Failed steps may be caused by earlier failures
- **Compare runs**: Compare failed runs with successful ones

### 2. Log Analysis

- **Filter by event type**: Focus on relevant events (FAILURE, ERROR)
- **Use step keys**: Isolate specific step failures
- **Check log levels**: ERROR and CRITICAL messages are key
- **Review stack traces**: Full Python tracebacks in error messages

### 3. Pagination

- Event logs can be large; use pagination for better performance
- Default limit is 5000 events per request
- Use cursor-based pagination for large log sets

### 4. Error Context

- Always capture surrounding events, not just failures
- Use `-B` and `-A` context when filtering (before/after events)
- Review STEP_START and STEP_SUCCESS events around failures

## Script Reference

All scripts are located in the `scripts/` directory:

- **get_run_info.py**: Get basic run metadata and status
- **get_run_logs.py**: Retrieve and filter event logs
- **get_run_stats.py**: Get run statistics and step execution details
- **get_job_runs.py**: Get all runs for a specific job
- **dagster_client.py**: Reusable GraphQL client library

### Common Script Options

All scripts support:
- `--url`: Dagster instance URL (default: http://127.0.0.1:3000)
- `--token`: API token for Dagster Cloud (optional for local)
- `--deployment`: Dagster Cloud deployment name (optional)

### Script Examples

```bash
# Local Dagster instance
python scripts/get_run_info.py --run-id abc123

# Dagster Cloud
python scripts/get_run_info.py \
  --run-id abc123 \
  --url https://myorg.dagster.cloud/prod \
  --token $DAGSTER_CLOUD_TOKEN

# Filter logs by event type
python scripts/get_run_logs.py \
  --run-id abc123 \
  --event-type "STEP_FAILURE,PIPELINE_FAILURE" \
  --limit 1000

# Get logs for specific step
python scripts/get_run_logs.py \
  --run-id abc123 \
  --step-key my_asset_name
```

## Additional Resources

- **Dagster Docs**: https://docs.dagster.io/guides/log-debug
- **GraphQL API Docs**: https://docs.dagster.io/api/graphql
- **Event Types Reference**: See `reference.md` for complete list
- **Error Handling Patterns**: See `reference.md` for common error patterns
