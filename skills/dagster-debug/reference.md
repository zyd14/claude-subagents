# Dagster Debug Reference

This document provides comprehensive reference information for debugging Dagster jobs.

## Table of Contents

1. [Event Types](#event-types)
2. [Common Error Patterns](#common-error-patterns)
3. [GraphQL Query Examples](#graphql-query-examples)
4. [Debugging Workflows](#debugging-workflows)
5. [Advanced Techniques](#advanced-techniques)

## Event Types

### Run-Level Events

| Event Type | Description | When It Occurs |
|------------|-------------|----------------|
| `RUN_START` | Run execution begins | At the very start of a run |
| `RUN_SUCCESS` | Run completed successfully | When all steps complete successfully |
| `RUN_FAILURE` | Run failed | When the run encounters a fatal error |
| `RUN_CANCELED` | Run was canceled | When a user or system cancels the run |
| `RUN_ENQUEUED` | Run was added to queue | When queuing is enabled |
| `RUN_DEQUEUED` | Run removed from queue | When run starts executing from queue |
| `RUN_STARTING` | Run is starting | Between enqueue and actual start |

### Step-Level Events

| Event Type | Description | When It Occurs |
|------------|-------------|----------------|
| `STEP_START` | Step execution begins | At the start of each step/op |
| `STEP_SUCCESS` | Step completed successfully | When step completes without errors |
| `STEP_FAILURE` | Step failed | When step encounters an error |
| `STEP_SKIPPED` | Step was skipped | When step is skipped due to branching |
| `STEP_UP_FOR_RETRY` | Step will be retried | When retry policy triggers |
| `STEP_RESTARTED` | Step restarted | When step is restarted |

### Output/Input Events

| Event Type | Description | When It Occurs |
|------------|-------------|----------------|
| `STEP_OUTPUT` | Step produced output | When step yields or returns value |
| `STEP_INPUT` | Step received input | When step consumes input |
| `HANDLED_OUTPUT` | Output was handled by IO manager | After IO manager stores output |
| `LOADED_INPUT` | Input was loaded | When IO manager loads input |

### Asset Events

| Event Type | Description | When It Occurs |
|------------|-------------|----------------|
| `ASSET_MATERIALIZATION` | Asset was materialized | When asset produces a value |
| `ASSET_MATERIALIZATION_PLANNED` | Asset materialization planned | When asset is scheduled to materialize |
| `ASSET_OBSERVATION` | Asset was observed | When asset observation runs |

### Resource Events

| Event Type | Description | When It Occurs |
|------------|-------------|----------------|
| `RESOURCE_INIT_STARTED` | Resource initialization starting | Before resource setup |
| `RESOURCE_INIT_SUCCESS` | Resource initialized successfully | After resource setup completes |
| `RESOURCE_INIT_FAILURE` | Resource initialization failed | When resource setup fails |

### Engine Events

| Event Type | Description | When It Occurs |
|------------|-------------|----------------|
| `ENGINE_EVENT` | Generic engine event | Various engine operations |
| `LOGS_CAPTURED` | Logs were captured | When logging is captured |
| `HOOK_COMPLETED` | Hook execution completed | After hook runs |
| `HOOK_ERRORED` | Hook execution failed | When hook encounters error |
| `HOOK_SKIPPED` | Hook was skipped | When hook is skipped |

## Common Error Patterns

### 1. Import/Module Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'my_package'
ImportError: cannot import name 'MyClass' from 'my_module'
```

**Event Pattern:**
- Early `STEP_FAILURE` or `RUN_FAILURE`
- Occurs at step start before any meaningful work
- Error message contains "Import" or "Module"

**Investigation Steps:**
1. Check Python environment and installed packages
2. Verify `PYTHONPATH` is correct
3. Review Docker image or deployment configuration
4. Check for circular imports

**Example Query:**
```bash
python scripts/get_run_logs.py --run-id <run-id> \
    --event-type "STEP_FAILURE,RUN_FAILURE" | grep -i "import\|module"
```

### 2. Resource Configuration Errors

**Symptoms:**
```
Resource 'database' failed to initialize
ConnectionRefusedError: [Errno 111] Connection refused
Authentication failed for resource 'api_client'
```

**Event Pattern:**
- `RESOURCE_INIT_FAILURE` events
- Occurs before any steps execute
- Error mentions specific resource name

**Investigation Steps:**
1. Check resource configuration in run config
2. Verify credentials and connection strings
3. Test external service availability
4. Review resource definition code

**Example Event:**
```json
{
  "eventType": "RESOURCE_INIT_FAILURE",
  "message": "Failed to initialize resource 'database'",
  "level": "ERROR",
  "timestamp": "2023-10-27T10:00:05Z"
}
```

### 3. Data Validation Errors

**Symptoms:**
```
ValueError: Expected column 'id' but not found
TypeError: Expected int, got str
ValidationError: Field 'email' is required
```

**Event Pattern:**
- `STEP_FAILURE` during data processing
- Often follows `LOADED_INPUT` or during `STEP_OUTPUT`
- Error message mentions data types, schemas, or validation

**Investigation Steps:**
1. Check upstream asset outputs
2. Verify data schema expectations
3. Review input data samples
4. Check for schema evolution

**Example Analysis:**
```bash
# Get step events around failure
python scripts/get_run_logs.py --run-id <run-id> \
    --step-key my_asset \
    --event-type "LOADED_INPUT,STEP_FAILURE,STEP_OUTPUT"
```

### 4. IO Manager Errors

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: '/path/to/file'
FileNotFoundError: No such file or directory
S3 bucket not accessible
```

**Event Pattern:**
- Failures during `HANDLED_OUTPUT` or `LOADED_INPUT`
- Error mentions file paths, S3, databases, or storage
- May occur after `STEP_SUCCESS` during output handling

**Investigation Steps:**
1. Check IO manager configuration
2. Verify permissions (filesystem, S3, database)
3. Review storage paths and bucket names
4. Check disk space or quota limits

**Example:**
```bash
# Find IO manager events
python scripts/get_run_logs.py --run-id <run-id> \
    --event-type "HANDLED_OUTPUT,LOADED_INPUT" | grep -i "error\|failed"
```

### 5. Timeout/Hanging Issues

**Symptoms:**
- Run never completes
- Step execution takes much longer than expected
- No events for extended periods

**Event Pattern:**
- `STEP_START` without corresponding `STEP_SUCCESS`
- Large time gaps between events
- No `RUN_SUCCESS` or `RUN_FAILURE`

**Investigation Steps:**
1. Check execution duration for each step
2. Look for blocking operations (network, database)
3. Review resource utilization
4. Check for deadlocks or infinite loops

**Example Analysis:**
```python
# Analyze step durations
import json
from datetime import datetime

# Get logs as JSON
logs = json.loads(subprocess.check_output([
    "python", "scripts/get_run_logs.py",
    "--run-id", run_id,
    "--event-type", "STEP_START,STEP_SUCCESS,STEP_FAILURE",
    "--json"
]))

# Calculate durations
step_times = {}
for event in logs["events"]:
    step_key = event.get("stepKey")
    event_type = event["eventType"]
    timestamp = event["timestamp"]

    if event_type == "STEP_START":
        step_times[step_key] = {"start": timestamp}
    elif event_type in ["STEP_SUCCESS", "STEP_FAILURE"]:
        if step_key in step_times:
            step_times[step_key]["end"] = timestamp
            # Calculate duration...
```

### 6. Dependency/Upstream Failures

**Symptoms:**
```
Failed to load input 'upstream_asset': No materialization found
Upstream step 'parent_step' did not produce expected output
```

**Event Pattern:**
- `STEP_FAILURE` with messages about missing inputs
- Occurs when loading inputs
- May follow upstream `STEP_FAILURE`

**Investigation Steps:**
1. Check upstream asset/step status
2. Verify dependency graph
3. Review upstream run status
4. Check if upstream outputs exist

**Example:**
```bash
# Check all step failures in order
python scripts/get_run_logs.py --run-id <run-id> \
    --event-type "STEP_FAILURE,STEP_SUCCESS" | grep "STEP_"
```

## GraphQL Query Examples

### Get Detailed Run Information

```graphql
query DetailedRun($runId: ID!) {
  runOrError(runId: $runId) {
    __typename
    ... on Run {
      id
      runId
      status
      pipelineName
      jobName
      mode
      startTime
      endTime
      runConfigYaml
      tags {
        key
        value
      }
      stats {
        ... on RunStatsSnapshot {
          stepsSucceeded
          stepsFailed
          materializations
          expectations
          startTime
          endTime
        }
      }
    }
  }
}
```

### Get Failed Runs for a Job

```graphql
query FailedRuns($jobName: String!) {
  runsOrError(
    filter: {
      pipelineName: $jobName
      statuses: [FAILURE]
    }
    limit: 50
  ) {
    __typename
    ... on Runs {
      results {
        runId
        status
        startTime
        endTime
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

### Get Events with Full Details

```graphql
query DetailedEvents($runId: ID!, $limit: Int!) {
  logsForRun(runId: $runId, limit: $limit) {
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
        ... on StepMaterializationEvent {
          runId
          timestamp
          stepKey
          materialization {
            label
            description
            metadataEntries {
              label
              description
            }
          }
        }
      }
      cursor
      hasMore
    }
  }
}
```

## Debugging Workflows

### Workflow 1: Investigating a Failed Run

```bash
# 1. Get run information
python scripts/get_run_info.py --run-id <run-id>

# 2. Get all failure events
python scripts/get_run_logs.py --run-id <run-id> \
    --event-type "FAILURE" --json > failures.json

# 3. Analyze the first failure
cat failures.json | jq '.events[0]'

# 4. Get context around the failure (get events for that step)
python scripts/get_run_logs.py --run-id <run-id> \
    --step-key <failed-step-key>

# 5. Check run stats
python scripts/get_run_stats.py --run-id <run-id>
```

### Workflow 2: Comparing Successful and Failed Runs

```bash
# 1. Get recent runs for the job
python scripts/get_job_runs.py --job-name my_job --limit 20

# 2. Identify successful and failed run IDs
# 3. Compare configurations
python scripts/get_run_info.py --run-id <success-run-id> --json > success.json
python scripts/get_run_info.py --run-id <failure-run-id> --json > failure.json

# 4. Diff the configurations
diff <(jq '.runConfigYaml' success.json) <(jq '.runConfigYaml' failure.json)

# 5. Compare event patterns
python scripts/get_run_logs.py --run-id <success-run-id> \
    --event-type "STEP_START,STEP_SUCCESS" > success_events.txt
python scripts/get_run_logs.py --run-id <failure-run-id> \
    --event-type "STEP_START,STEP_SUCCESS,STEP_FAILURE" > failure_events.txt
```

### Workflow 3: Asset Materialization Debugging

```bash
# 1. Get asset materialization events
python scripts/get_run_logs.py --run-id <run-id> \
    --event-type "ASSET_MATERIALIZATION,ASSET_MATERIALIZATION_PLANNED"

# 2. Check for IO manager events
python scripts/get_run_logs.py --run-id <run-id> \
    --event-type "HANDLED_OUTPUT,LOADED_INPUT"

# 3. Look for resource initialization issues
python scripts/get_run_logs.py --run-id <run-id> \
    --event-type "RESOURCE_INIT_STARTED,RESOURCE_INIT_SUCCESS,RESOURCE_INIT_FAILURE"

# 4. Review step outputs
python scripts/get_run_logs.py --run-id <run-id> \
    --event-type "STEP_OUTPUT"
```

## Advanced Techniques

### Using jq for Log Analysis

```bash
# Extract all error messages
python scripts/get_run_logs.py --run-id <run-id> --json | \
    jq -r '.events[] | select(.level == "ERROR") | .message'

# Count events by type
python scripts/get_run_logs.py --run-id <run-id> --json | \
    jq '.events | group_by(.eventType) | map({type: .[0].eventType, count: length})'

# Get timeline of a specific step
python scripts/get_run_logs.py --run-id <run-id> --json | \
    jq '.events[] | select(.stepKey == "my_asset") | {time: .timestamp, event: .eventType, msg: .message}'
```

### Pagination for Large Log Sets

```bash
# Get first page
python scripts/get_run_logs.py --run-id <run-id> --limit 1000 --json > page1.json

# Extract cursor
CURSOR=$(jq -r '.cursor' page1.json)

# Get next page
python scripts/get_run_logs.py --run-id <run-id> --limit 1000 --cursor "$CURSOR" --json > page2.json
```

### Creating Custom Filters

```python
#!/usr/bin/env python3
"""Custom filter for error analysis"""
import json
import sys

# Read logs from stdin
logs = json.load(sys.stdin)

# Filter for import errors
import_errors = [
    e for e in logs["events"]
    if "ERROR" in e.get("level", "")
    and any(keyword in e.get("message", "").lower()
            for keyword in ["import", "module", "cannot"])
]

# Output formatted results
for error in import_errors:
    print(f"[{error['timestamp']}] {error['message']}")
```

Usage:
```bash
python scripts/get_run_logs.py --run-id <run-id> --json | \
    python custom_filter.py
```

### Monitoring Multiple Runs

```bash
#!/bin/bash
# Monitor status of multiple runs

JOB_NAME="my_job"
LIMIT=10

# Get recent runs
python scripts/get_job_runs.py --job-name "$JOB_NAME" --limit "$LIMIT" --json | \
    jq -r '.runsOrError.results[] | "\(.status)\t\(.runId)"' | \
    while IFS=$'\t' read -r status run_id; do
        if [ "$status" == "FAILURE" ]; then
            echo "Failed run: $run_id"
            python scripts/get_run_logs.py --run-id "$run_id" \
                --event-type "FAILURE" --no-color | head -20
            echo "---"
        fi
    done
```

## Best Practices Summary

1. **Start Broad**: Get run info first, then narrow down to specific issues
2. **Follow Timeline**: Review events chronologically to understand sequence
3. **Check Upstream**: Failures may cascade from earlier steps
4. **Use Filters**: Filter by event type and step key to focus on relevant events
5. **Compare Runs**: Compare failed runs with successful ones
6. **Paginate Large Logs**: Use cursor-based pagination for better performance
7. **Automate Common Patterns**: Create scripts for frequently used queries
8. **Save Outputs**: Save logs as JSON for offline analysis and comparison
9. **Use Structured Logging**: Leverage structured metadata in events
10. **Review Resource Init**: Many issues stem from resource configuration

## Additional Resources

- [Dagster Logging Guide](https://docs.dagster.io/guides/log-debug/logging)
- [Dagster GraphQL API Docs](https://docs.dagster.io/api/graphql)
- [Dagster Troubleshooting](https://docs.dagster.io/deployment/guides/troubleshooting)
