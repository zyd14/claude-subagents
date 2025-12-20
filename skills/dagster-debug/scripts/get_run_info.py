#!/usr/bin/env python3
# /// script
# dependencies = [
#   "dagster-graphql>=1.5.0",
#   "gql>=3.0.0",
# ]
# ///
"""
Get run information for a Dagster run.

Usage:
    python get_run_info.py --run-id <run-id> [--url <url>] [--token <token>]

Examples:
    # Local Dagster instance
    python get_run_info.py --run-id abc123-def456

    # Dagster Cloud
    python get_run_info.py --run-id abc123-def456 \\
        --url https://myorg.dagster.cloud/prod \\
        --token $DAGSTER_CLOUD_TOKEN

    # Using deployment name
    python get_run_info.py --run-id abc123-def456 --deployment prod
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


def main():
    parser = argparse.ArgumentParser(
        description="Get run information for a Dagster run"
    )
    parser.add_argument(
        "--run-id",
        required=True,
        help="Run ID to query"
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

        # Get run info
        run_info = client.get_run_info(args.run_id)

        if args.json:
            # Output raw JSON
            print(json.dumps(run_info, indent=2))
        else:
            # Output formatted text
            print("\n" + "="*60)
            print(f"Run Information: {run_info.get('runId', args.run_id)}")
            print("="*60)
            print(f"Status:        {run_info.get('status', 'UNKNOWN')}")
            print(f"Job Name:      {run_info.get('jobName') or run_info.get('pipelineName', 'N/A')}")
            print(f"Mode:          {run_info.get('mode', 'N/A')}")
            print(f"Start Time:    {format_timestamp(run_info.get('startTime'))}")
            print(f"End Time:      {format_timestamp(run_info.get('endTime'))}")
            print(f"Duration:      {format_duration(run_info.get('startTime'), run_info.get('endTime'))}")

            # Show config if available
            config_yaml = run_info.get('runConfigYaml')
            if config_yaml:
                print("\nRun Configuration:")
                print("-" * 60)
                print(config_yaml)

            print("="*60 + "\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
