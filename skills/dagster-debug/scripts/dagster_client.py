#!/usr/bin/env python3
# /// script
# dependencies = [
#   "dagster-graphql>=1.5.0",
#   "gql>=3.0.0",
# ]
# ///
"""
Reusable Dagster GraphQL client for debugging operations.

This module provides a client class that wraps the DagsterGraphQLClient
and extends it with debugging-specific methods.
"""

import os
from typing import Any, Optional

from dagster_graphql import DagsterGraphQLClient
from gql.transport.requests import RequestsHTTPTransport


class DagsterDebugClient(DagsterGraphQLClient):
    """
    Extended Dagster GraphQL client with debugging capabilities.

    Provides methods for querying run information, event logs, and statistics
    specifically tailored for debugging failed or erroneous runs.
    """

    @classmethod
    def create_client(
        cls,
        url: str | None = None,
        token: str | None = None,
        deployment: str | None = None,
    ) -> "DagsterDebugClient":
        """
        Create a DagsterDebugClient instance.

        Args:
            url: Dagster instance URL. If not provided, uses environment variable
                 DAGSTER_URL or defaults to http://127.0.0.1:3000
            token: API token for Dagster Cloud. If not provided, uses environment
                   variable DAGSTER_CLOUD_TOKEN
            deployment: Dagster Cloud deployment name. If provided, constructs URL
                       from deployment name

        Returns:
            DagsterDebugClient instance
        """
        # Determine URL
        if deployment:
            dagster_url = f"https://{os.getenv('DAGSTER_CLOUD_ORG', 'org')}.dagster.cloud/{deployment}"
        elif url:
            dagster_url = url
        else:
            dagster_url = os.getenv("DAGSTER_URL", "http://127.0.0.1:3000")

        # Get token if needed
        api_token = token or os.getenv("DAGSTER_CLOUD_TOKEN")

        # Create transport with auth if token provided
        if api_token:
            transport = RequestsHTTPTransport(
                url=f"{dagster_url}/graphql",
                headers={"Dagster-Cloud-Api-Token": api_token}
            )
            return cls(hostname=dagster_url, transport=transport)
        else:
            return cls(hostname=dagster_url)

    def get_run_info(self, run_id: str) -> dict[str, Any]:
        """
        Get basic run information including status, timestamps, and configuration.

        Args:
            run_id: The run ID to query

        Returns:
            Dictionary with run information

        Raises:
            RuntimeError: If the run is not found or a GraphQL error occurs
        """
        query = """
        query GetRun($runId: ID!) {
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
        """

        result = self._execute(query, {"runId": run_id})
        run_result = result.get("runOrError")

        if not run_result:
            raise RuntimeError("Empty response from GraphQL API")

        typename = run_result.get("__typename")

        if typename == "PythonError":
            error_msg = run_result.get("message", "Unknown error")
            stack = run_result.get("stack", "")
            raise RuntimeError(f"GraphQL error: {error_msg}\n{stack}")

        if typename == "RunNotFoundError":
            error_msg = run_result.get("message", f"Run {run_id} not found")
            raise RuntimeError(error_msg)

        if typename != "Run":
            raise RuntimeError(f"Unexpected response type: {typename}")

        return run_result

    def get_run_logs(
        self,
        run_id: str,
        limit: int = 5000,
        cursor: str | None = None,
        event_type: str | None = None,
        step_key: str | None = None,
    ) -> dict[str, Any]:
        """
        Get event logs for a run with optional filtering.

        Args:
            run_id: The run ID to query
            limit: Maximum number of events to return
            cursor: Pagination cursor for subsequent pages
            event_type: Comma-separated event types to filter (e.g., "STEP_FAILURE,PIPELINE_FAILURE")
            step_key: Step key to filter events by

        Returns:
            Dictionary with events list, cursor, and hasMore flag

        Raises:
            RuntimeError: If the run is not found or a GraphQL error occurs
        """
        query = """
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
        """

        variables: dict[str, Any] = {"runId": run_id, "limit": limit}
        if cursor:
            variables["afterCursor"] = cursor

        result = self._execute(query, variables)
        logs_result = result.get("logsForRun")

        if not logs_result:
            raise RuntimeError("Empty response from GraphQL API")

        typename = logs_result.get("__typename")

        if typename == "PythonError":
            error_msg = logs_result.get("message", "Unknown error")
            stack = logs_result.get("stack", "")
            raise RuntimeError(f"Failed to get logs: {error_msg}\n{stack}")

        if typename == "RunNotFoundError":
            error_msg = logs_result.get("message", f"Run {run_id} not found")
            raise RuntimeError(error_msg)

        if typename != "EventConnection":
            raise RuntimeError(f"Unexpected response type: {typename}")

        # Apply client-side filters
        events = logs_result.get("events", [])

        if event_type:
            events = self._filter_by_event_type(events, event_type)

        if step_key:
            events = self._filter_by_step_key(events, step_key)

        return {
            "events": events,
            "cursor": logs_result.get("cursor"),
            "hasMore": logs_result.get("hasMore", False)
        }

    def get_run_stats(self, run_ids: list[str]) -> dict[str, Any]:
        """
        Get run statistics including step execution and failure counts.

        Args:
            run_ids: List of run IDs to query

        Returns:
            Dictionary with run statistics
        """
        query = """
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
                    stepsSucceeded
                    expectations
                    materializations
                  }
                }
              }
            }
          }
        }
        """

        result = self._execute(query, {"runIds": run_ids})
        return result

    def get_job_runs(
        self,
        job_name: str,
        limit: int = 100,
        statuses: list[str] | None = None
    ) -> dict[str, Any]:
        """
        Get all runs for a specific job/pipeline.

        Args:
            job_name: Name of the job/pipeline
            limit: Maximum number of runs to return
            statuses: Optional list of statuses to filter by (e.g., ["FAILURE"])

        Returns:
            Dictionary with run information
        """
        query = """
        query JobRuns($pipelineName: String, $limit: Int, $statuses: [RunStatus!]) {
          runsOrError(
            filter: {pipelineName: $pipelineName, statuses: $statuses}
            limit: $limit
          ) {
            __typename
            ... on Runs {
              results {
                runId
                jobName
                pipelineName
                status
                startTime
                endTime
              }
            }
          }
        }
        """

        variables: dict[str, Any] = {
            "pipelineName": job_name,
            "limit": limit
        }
        if statuses:
            variables["statuses"] = statuses

        result = self._execute(query, variables)
        return result

    def _filter_by_event_type(
        self,
        events: list[dict[str, Any]],
        event_type: str
    ) -> list[dict[str, Any]]:
        """Filter events by comma-separated event types (case-insensitive)."""
        types = [t.strip().upper() for t in event_type.split(",")]
        return [
            e for e in events
            if e.get("eventType", "").upper() in types
        ]

    def _filter_by_step_key(
        self,
        events: list[dict[str, Any]],
        step_key: str
    ) -> list[dict[str, Any]]:
        """Filter events by step key (case-insensitive partial match)."""
        step_key_lower = step_key.lower()
        return [
            e for e in events
            if e.get("stepKey", "").lower().find(step_key_lower) != -1
        ]
