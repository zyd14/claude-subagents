#!/usr/bin/env python3
# /// script
# dependencies = [
#   "dagster-graphql>=1.5.0",
#   "gql>=3.0.0",
# ]
# ///
"""
Get event logs for a Dagster run with optional filtering.

Usage:
    python get_run_logs.py --run-id <run-id> [OPTIONS]

Examples:
    # Get all logs
    python get_run_logs.py --run-id abc123-def456

    # Get only failure events
    python get_run_logs.py --run-id abc123-def456 --event-type FAILURE

    # Get logs for a specific step
    python get_run_logs.py --run-id abc123-def456 --step-key my_asset

    # Get specific event types
    python get_run_logs.py --run-id abc123-def456 \\
        --event-type "STEP_FAILURE,PIPELINE_FAILURE,ASSET_MATERIALIZATION"

    # Limit results and use pagination
    python get_run_logs.py --run-id abc123-def456 --limit 100

    # Output as JSON for further processing
    python get_run_logs.py --run-id abc123-def456 --json > logs.json
"""

import argparse
import json
import sys
from datetime import datetime

from dagster_client import DagsterDebugClient


def format_timestamp(timestamp: str | float) -> str:
    """Format timestamp to human-readable format."""
    if isinstance(timestamp, str):
        # Parse ISO format or other string formats
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return timestamp
    elif isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    return str(timestamp)


def format_event(event: dict, show_step: bool = True) -> str:
    """Format a single event for display."""
    timestamp = format_timestamp(event.get("timestamp", ""))
    level = event.get("level", "INFO")
    event_type = event.get("eventType", "UNKNOWN")
    step_key = event.get("stepKey", "")
    message = event.get("message", "")

    # Color codes for different levels (if terminal supports it)
    level_colors = {
        "ERROR": "\033[91m",     # Red
        "CRITICAL": "\033[91m",  # Red
        "WARNING": "\033[93m",   # Yellow
        "INFO": "\033[94m",      # Blue
        "DEBUG": "\033[90m",     # Gray
    }
    reset_color = "\033[0m"

    color = level_colors.get(level, "")

    # Build formatted string
    parts = [f"[{timestamp}]", f"{color}{level}{reset_color}"]

    if show_step and step_key:
        parts.append(f"[{step_key}]")

    parts.append(f"{event_type}")

    if message:
        parts.append(f"- {message}")

    return " ".join(parts)


def main():
    parser = argparse.ArgumentParser(
        description="Get event logs for a Dagster run"
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
        "--event-type",
        help="Comma-separated event types to filter (e.g., 'STEP_FAILURE,PIPELINE_FAILURE')"
    )
    parser.add_argument(
        "--step-key",
        help="Filter events by step key"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5000,
        help="Maximum number of events to retrieve (default: 5000)"
    )
    parser.add_argument(
        "--cursor",
        help="Pagination cursor for subsequent pages"
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

        # Get logs
        result = client.get_run_logs(
            run_id=args.run_id,
            limit=args.limit,
            cursor=args.cursor,
            event_type=args.event_type,
            step_key=args.step_key
        )

        events = result["events"]
        has_more = result["hasMore"]
        cursor = result["cursor"]

        if args.json:
            # Output raw JSON
            print(json.dumps(result, indent=2))
        else:
            # Output formatted text
            print("\n" + "="*80)
            print(f"Event Logs for Run: {args.run_id}")
            if args.event_type:
                print(f"Filtered by event type: {args.event_type}")
            if args.step_key:
                print(f"Filtered by step key: {args.step_key}")
            print(f"Events retrieved: {len(events)}")
            if has_more:
                print(f"More events available (cursor: {cursor})")
            print("="*80 + "\n")

            if not events:
                print("No events found matching the criteria.\n")
            else:
                for event in events:
                    print(format_event(event, show_step=not args.step_key))

            print("\n" + "="*80)

            if has_more:
                print(f"\nTo retrieve more events, use:")
                print(f"  --cursor {cursor}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
