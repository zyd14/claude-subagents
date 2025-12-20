#!/usr/bin/env python3
# /// script
# dependencies = [
#   "dagster-graphql>=1.5.0",
#   "gql>=3.0.0",
# ]
# ///
"""
Example debugging workflow demonstrating how to investigate a failed Dagster run.

This script shows a complete debugging workflow:
1. Get run information
2. Retrieve failure events
3. Analyze error patterns
4. Generate debugging report

Usage:
    python example_debug_workflow.py --run-id <run-id> [--url <url>] [--token <token>]
"""

import argparse
import sys
from datetime import datetime

from dagster_client import DagsterDebugClient


def format_timestamp(timestamp: float | None) -> str:
    """Format Unix timestamp to human-readable format."""
    if timestamp is None:
        return "N/A"
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def analyze_error_pattern(events: list[dict]) -> dict[str, any]:
    """Analyze events to identify error patterns."""
    patterns = {
        "import_errors": [],
        "resource_errors": [],
        "data_errors": [],
        "io_errors": [],
        "timeout_indicators": [],
        "other_errors": []
    }

    keywords = {
        "import_errors": ["import", "module", "cannot import"],
        "resource_errors": ["resource", "connection", "authentication", "credential"],
        "data_errors": ["validation", "schema", "type", "expected"],
        "io_errors": ["permission", "file not found", "s3", "bucket", "storage"],
    }

    for event in events:
        message = event.get("message", "").lower()
        event_type = event.get("eventType", "")

        # Check for timeouts
        if "timeout" in message or "hanging" in message:
            patterns["timeout_indicators"].append(event)
            continue

        # Check against keyword patterns
        matched = False
        for pattern_type, pattern_keywords in keywords.items():
            if any(keyword in message for keyword in pattern_keywords):
                patterns[pattern_type].append(event)
                matched = True
                break

        if not matched and "ERROR" in event.get("level", ""):
            patterns["other_errors"].append(event)

    return patterns


def generate_report(run_info: dict, error_patterns: dict, all_events: list[dict]) -> str:
    """Generate a debugging report."""
    report = []

    report.append("=" * 80)
    report.append("DAGSTER RUN DEBUGGING REPORT")
    report.append("=" * 80)
    report.append("")

    # Run Information
    report.append("RUN INFORMATION")
    report.append("-" * 80)
    report.append(f"Run ID:        {run_info.get('runId', 'N/A')}")
    report.append(f"Status:        {run_info.get('status', 'UNKNOWN')}")
    report.append(f"Job Name:      {run_info.get('jobName') or run_info.get('pipelineName', 'N/A')}")
    report.append(f"Start Time:    {format_timestamp(run_info.get('startTime'))}")
    report.append(f"End Time:      {format_timestamp(run_info.get('endTime'))}")
    report.append("")

    # Error Summary
    report.append("ERROR SUMMARY")
    report.append("-" * 80)

    total_errors = sum(len(errors) for errors in error_patterns.values())
    report.append(f"Total Errors Found: {total_errors}")
    report.append("")

    for pattern_type, errors in error_patterns.items():
        if errors:
            pattern_name = pattern_type.replace("_", " ").title()
            report.append(f"{pattern_name}: {len(errors)}")

    report.append("")

    # Detailed Analysis
    report.append("DETAILED ANALYSIS")
    report.append("-" * 80)

    for pattern_type, errors in error_patterns.items():
        if errors:
            pattern_name = pattern_type.replace("_", " ").title()
            report.append(f"\n{pattern_name}:")
            report.append("-" * 40)

            for error in errors[:5]:  # Show first 5 of each type
                report.append(f"\n  Timestamp: {format_timestamp(error.get('timestamp'))}")
                report.append(f"  Event Type: {error.get('eventType', 'N/A')}")
                report.append(f"  Step Key: {error.get('stepKey', 'N/A')}")
                report.append(f"  Message: {error.get('message', 'N/A')[:200]}...")

            if len(errors) > 5:
                report.append(f"\n  ... and {len(errors) - 5} more")

    # Recommendations
    report.append("\n")
    report.append("RECOMMENDATIONS")
    report.append("-" * 80)

    if error_patterns["import_errors"]:
        report.append("• Check Python environment and installed packages")
        report.append("• Verify PYTHONPATH and module locations")

    if error_patterns["resource_errors"]:
        report.append("• Verify resource configurations in run config")
        report.append("• Check credentials and connection strings")
        report.append("• Test external service availability")

    if error_patterns["data_errors"]:
        report.append("• Review upstream asset outputs")
        report.append("• Verify data schema expectations")
        report.append("• Check for schema evolution")

    if error_patterns["io_errors"]:
        report.append("• Check file/storage permissions")
        report.append("• Verify S3 bucket access or storage paths")
        report.append("• Review disk space and quotas")

    if error_patterns["timeout_indicators"]:
        report.append("• Review step execution times")
        report.append("• Check for blocking operations")
        report.append("• Monitor resource utilization")

    report.append("")
    report.append("=" * 80)

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Example debugging workflow for a failed Dagster run"
    )
    parser.add_argument("--run-id", required=True, help="Run ID to debug")
    parser.add_argument("--url", help="Dagster instance URL")
    parser.add_argument("--token", help="Dagster Cloud API token")
    parser.add_argument("--deployment", help="Dagster Cloud deployment name")

    args = parser.parse_args()

    try:
        print("\n🔍 Starting debugging workflow...\n")

        # Create client
        client = DagsterDebugClient.create_client(
            url=args.url,
            token=args.token,
            deployment=args.deployment
        )

        # Step 1: Get run information
        print("📊 Retrieving run information...")
        run_info = client.get_run_info(args.run_id)
        print(f"   Status: {run_info.get('status')}")
        print(f"   Job: {run_info.get('jobName') or run_info.get('pipelineName')}")

        # Step 2: Get all events
        print("\n📝 Retrieving event logs...")
        logs_result = client.get_run_logs(args.run_id, limit=5000)
        all_events = logs_result["events"]
        print(f"   Retrieved {len(all_events)} events")

        # Step 3: Filter for errors
        print("\n🔴 Filtering for error events...")
        error_events = [
            e for e in all_events
            if "FAILURE" in e.get("eventType", "") or "ERROR" in e.get("level", "")
        ]
        print(f"   Found {len(error_events)} error events")

        # Step 4: Analyze error patterns
        print("\n🧪 Analyzing error patterns...")
        error_patterns = analyze_error_pattern(error_events)

        # Step 5: Generate report
        print("\n📋 Generating debugging report...\n")
        report = generate_report(run_info, error_patterns, all_events)
        print(report)

    except Exception as e:
        print(f"\n❌ Error during debugging: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
