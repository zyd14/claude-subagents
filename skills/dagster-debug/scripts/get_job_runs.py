#!/usr/bin/env python3
# /// script
# dependencies = [
#   "dagster-graphql>=1.5.0",
#   "gql>=3.0.0",
# ]
# ///
"""
Get all runs for a specific Dagster job/pipeline.

Usage:
    python get_job_runs.py --job-name <job-name> [OPTIONS]

Examples:
    # Get all runs for a job
    python get_job_runs.py --job-name my_job

    # Get only failed runs
    python get_job_runs.py --job-name my_job --status FAILURE

    # Get multiple statuses
    python get_job_runs.py --job-name my_job --status FAILURE,SUCCESS

    # Limit results
    python get_job_runs.py --job-name my_job --limit 20

    # Output as JSON
    python get_job_runs.py --job-name my_job --json
"""

import argparse
import json
import sys
from datetime import datetime

from dagster_client import DagsterDebugClient


def format_timestamp(timestamp: float | None) -> str:
    """Format Unix timestamp to human-readable format."""
    if timestamp is None:
        return "N/A"
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def format_duration(start_time: float | None, end_time: float | None) -> str:
    """Calculate and format duration between timestamps."""
    if start_time is None or end_time is None:
        return "N/A"
    duration_seconds = end_time - start_time
    minutes, seconds = divmod(int(duration_seconds), 60)
    hours, minutes = divmod(minutes, 60)

    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def format_status(status: str) -> str:
    """Format status with color coding."""
    status_colors = {
        "SUCCESS": "\033[92m",    # Green
        "FAILURE": "\033[91m",    # Red
        "STARTED": "\033[93m",    # Yellow
        "CANCELED": "\033[90m",   # Gray
    }
    reset_color = "\033[0m"
    color = status_colors.get(status, "")
    return f"{color}{status}{reset_color}"


def format_run_summary(run: dict) -> str:
    """Format a single run summary."""
    run_id = run.get("runId", "N/A")
    status = run.get("status", "UNKNOWN")
    start_time = run.get("startTime")
    end_time = run.get("endTime")

    return (
        f"  {format_status(status):20} | "
        f"{run_id:40} | "
        f"{format_timestamp(start_time):20} | "
        f"{format_duration(start_time, end_time):15}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Get all runs for a Dagster job/pipeline"
    )
    parser.add_argument(
        "--job-name",
        required=True,
        help="Job/pipeline name to query"
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
        "--status",
        help="Comma-separated list of statuses to filter (e.g., 'FAILURE,SUCCESS')"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of runs to retrieve (default: 100)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of formatted text"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    args = parser.parse_args()

    try:
        # Create client
        client = DagsterDebugClient.create_client(
            url=args.url,
            token=args.token,
            deployment=args.deployment
        )

        # Parse statuses if provided
        statuses = None
        if args.status:
            statuses = [s.strip().upper() for s in args.status.split(",")]

        # Get job runs
        result = client.get_job_runs(
            job_name=args.job_name,
            limit=args.limit,
            statuses=statuses
        )

        if args.json:
            # Output raw JSON
            print(json.dumps(result, indent=2))
        else:
            # Output formatted text
            print("\n" + "="*100)
            print(f"Runs for Job: {args.job_name}")
            if statuses:
                print(f"Filtered by status: {', '.join(statuses)}")
            print("="*100)

            runs_or_error = result.get("runsOrError", {})
            typename = runs_or_error.get("__typename")

            if typename == "Runs":
                runs = runs_or_error.get("results", [])

                if not runs:
                    print("\nNo runs found.\n")
                else:
                    print(f"\nTotal runs: {len(runs)}\n")

                    # Print header
                    print(
                        f"  {'Status':20} | "
                        f"{'Run ID':40} | "
                        f"{'Start Time':20} | "
                        f"{'Duration':15}"
                    )
                    print("  " + "-"*96)

                    # Print runs
                    for run in runs:
                        print(format_run_summary(run))

                    # Summary statistics
                    status_counts: dict[str, int] = {}
                    for run in runs:
                        status = run.get("status", "UNKNOWN")
                        status_counts[status] = status_counts.get(status, 0) + 1

                    print("\n" + "-"*100)
                    print("Summary:")
                    for status, count in sorted(status_counts.items()):
                        print(f"  {status}: {count}")
            else:
                print(f"\nError: Unexpected response type: {typename}\n")

            print("\n" + "="*100 + "\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
