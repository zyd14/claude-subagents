#!/usr/bin/env python3
# /// script
# dependencies = [
#   "dagster-graphql>=1.5.0",
#   "gql>=3.0.0",
# ]
# ///
"""
Get run statistics for one or more Dagster runs.

Usage:
    python get_run_stats.py --run-id <run-id> [OPTIONS]

Examples:
    # Get stats for a single run
    python get_run_stats.py --run-id abc123-def456

    # Get stats for multiple runs
    python get_run_stats.py --run-ids abc123-def456,xyz789-ghi012

    # Output as JSON
    python get_run_stats.py --run-id abc123-def456 --json
"""

import argparse
import json
import sys

from dagster_client import DagsterDebugClient


def format_stats(run_data: dict) -> str:
    """Format run statistics for display."""
    run_id = run_data.get("runId", "N/A")
    step_keys = run_data.get("stepKeysToExecute", [])
    stats = run_data.get("stats", {})

    steps_failed = stats.get("stepsFailed", 0)
    steps_succeeded = stats.get("stepsSucceeded", 0)
    materializations = stats.get("materializations", 0)
    expectations = stats.get("expectations", 0)

    total_steps = len(step_keys)

    output = []
    output.append(f"\nRun ID: {run_id}")
    output.append("-" * 60)
    output.append(f"Total Steps:        {total_steps}")
    output.append(f"Steps Succeeded:    {steps_succeeded}")
    output.append(f"Steps Failed:       {steps_failed}")
    output.append(f"Materializations:   {materializations}")
    output.append(f"Expectations:       {expectations}")

    if step_keys:
        output.append("\nSteps to Execute:")
        for i, step_key in enumerate(step_keys, 1):
            output.append(f"  {i}. {step_key}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Get run statistics for Dagster runs"
    )

    # Allow either --run-id for single run or --run-ids for multiple
    run_group = parser.add_mutually_exclusive_group(required=True)
    run_group.add_argument(
        "--run-id",
        help="Single run ID to query"
    )
    run_group.add_argument(
        "--run-ids",
        help="Comma-separated list of run IDs to query"
    )

    parser.add_argument(
        "--url",
        help="Dagster instance URL (default: http://127.0.0.1:3000)"
    )
    parser.add_argument(
        "--token",
        help="Dagster Cloud API token"
    )
    parser.add_argument(
        "--deployment",
        help="Dagster Cloud deployment name"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of formatted text"
    )

    args = parser.parse_args()

    try:
        # Create client
        client = DagsterDebugClient.create_client(
            url=args.url,
            token=args.token,
            deployment=args.deployment
        )

        # Parse run IDs
        if args.run_id:
            run_ids = [args.run_id]
        else:
            run_ids = [rid.strip() for rid in args.run_ids.split(",")]

        # Get stats
        result = client.get_run_stats(run_ids)

        if args.json:
            # Output raw JSON
            print(json.dumps(result, indent=2))
        else:
            # Output formatted text
            print("\n" + "="*60)
            print("Run Statistics")
            print("="*60)

            runs_or_error = result.get("runsOrError", {})
            typename = runs_or_error.get("__typename")

            if typename == "Runs":
                runs = runs_or_error.get("results", [])
                if not runs:
                    print("\nNo runs found.\n")
                else:
                    for run_data in runs:
                        print(format_stats(run_data))
            else:
                print(f"\nError: Unexpected response type: {typename}\n")

            print("\n" + "="*60 + "\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
