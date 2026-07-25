"""Minimal GraphQL client."""

from __future__ import annotations

from typing import Any, Dict, Optional

from echoui.api import ApiClient


class GraphQLClient:
    def __init__(self, endpoint: str, *, api: Optional[ApiClient] = None) -> None:
        self.endpoint = endpoint
        self._api = api or ApiClient(base_url=endpoint.rsplit("/graphql", 1)[0])

    async def query(self, document: str, variables: Optional[Dict[str, Any]] = None) -> Any:
        body = {"query": document, "variables": variables or {}}
        return await self._api._request("POST", "/graphql", json=body)

    async def mutate(self, document: str, variables: Optional[Dict[str, Any]] = None) -> Any:
        return await self.query(document, variables)
