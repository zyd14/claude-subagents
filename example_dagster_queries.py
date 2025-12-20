"""
Contains Dagster resources that abstract interactions with the Dagster GraphQL API
"""

import os
from typing import List, Optional

from dagster import Field, InitResourceContext, resource
from dagster_graphql import DagsterGraphQLClient
from gql.transport.requests import RequestsHTTPTransport

from etxlib.etxdagster.infrastructure.aws.datatypes import SSMSource

DAGSTER_CLOUD_DEPLOYMENT = os.getenv("DAGSTER_CLOUD_DEPLOYMENT_NAME", "local")
if DAGSTER_CLOUD_DEPLOYMENT == "local":
    DAGSTER_URL = "http://127.0.0.1:3000"
else:
    DAGSTER_URL = f"https://empirico.dagster.cloud/{DAGSTER_CLOUD_DEPLOYMENT}"


def get_etx_graphql_client(url: str, token: str):
    transport = RequestsHTTPTransport(
        url=f"{url}/graphql", headers={"Dagster-Cloud-Api-Token": token}
    )
    client = EtxGraphQLClient(hostname=url, transport=transport)
    return client


@resource(
    config_schema={
        "url": Field(
            str,
            default_value=DAGSTER_URL,
        ),
        "token": Field(
            SSMSource,
            default_value={
                "ssm_config": {
                    "param_name": "/dagster/cloud/user_key",
                    "encrypted": True,
                }
            },
        ),
    }
)
def etx_graphql_client(init_context: InitResourceContext):
    """Thin wrapper around the dagster GraphQL API"""
    return get_etx_graphql_client(
        url=init_context.resource_config["url"],
        token=init_context.resource_config["token"],
    )


class EtxGraphQLClient(DagsterGraphQLClient):
    """
    Client for executing GraphQL queries against a Dagster instance, acting as a thin wrapper around the Dagster
    GraphQL API.
    """

    def get_run_stats(self, run_ids: List[str]):
        query = """
                query RunsQuery(
            $runIds: [String]
          ) {
            runsOrError (filter: {runIds: $runIds}) {
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
                """
        variables = {"runIds": run_ids}
        return self._execute(query, variables)

    def get_job_runs(self, job_name: str):
        query = """
        query RunsQuery(
          $pipelineName: String
        ) {
          runsOrError (filter: {pipelineName: $pipelineName}) {
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
        """
        return self._execute(query, {"pipeline_name": job_name})

    def get_run_event_logs(
        self,
        run_id: str,
        cursor: Optional[str] = None,
        limit: int = 5000,
    ):
        non_cursor_query = """
        query LogsForRun($runId: ID!, $limit: Int){
              logsForRun (runId: $runId, limit: $limit) {
                ... on EventConnection {
                  cursor
                  hasMore
                  events {
                    ... on ExecutionStepStartEvent {
                      eventType
                      runId
                      timestamp
                      stepKey
                    }
                    ... on ExecutionStepFailureEvent {
                      eventType
                      runId
                      timestamp
                      stepKey
                    }
                    ... on ExecutionStepSuccessEvent {
                      eventType
                      runId
                      timestamp
                      stepKey
                    }
                  }
                  
                }
              }
            }
        """
        cursor_query = """
        query LogsForRun($runId: ID!, $cursor: String!, $limit: Int){
          logsForRun (runId: $runId, afterCursor: $cursor, limit: $limit) {
            ... on EventConnection {
              cursor
              hasMore
              events {
                ... on ExecutionStepStartEvent {
                  eventType
                  runId
                  timestamp
                  stepKey
                }
                ... on ExecutionStepFailureEvent {
                  eventType
                  runId
                  timestamp
                  stepKey
                }
                ... on ExecutionStepSuccessEvent {
                  eventType
                  runId
                  timestamp
                  stepKey
                }
              }
            }
          }
        }
        """
        if cursor:
            query = cursor_query
            variables = {"runId": run_id, "cursor": cursor, "limit": limit}
        else:
            query = non_cursor_query
            variables = {"runId": run_id, "limit": limit}

        results = self._execute(query, variables)
        return results

    def create_user_token(self, user_id: int, description: str):
        create_token_query = """
        mutation DagsterCloudToken($description: String, $userId: Int!) {
          createUserToken(description: $description, userId: $userId){
            ... on DagsterCloudUserToken {
              token
            }
          }
        }
        """
        variables = {"userId": user_id, "description": description}
        return self._execute(create_token_query, variables)
