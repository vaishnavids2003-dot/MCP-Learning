import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()


class ServiceNowClient:

    def __init__(self):
        self.base_url = os.getenv("SERVICENOW_INSTANCE_URL")
        self.username = os.getenv("SERVICENOW_USERNAME")
        self.password = os.getenv("SERVICENOW_PASSWORD")

        if not self.base_url:
            raise ValueError("SERVICENOW_INSTANCE_URL is missing")

        if not self.username:
            raise ValueError("SERVICENOW_USERNAME is missing")

        if not self.password:
            raise ValueError("SERVICENOW_PASSWORD is missing")

        self.base_url = self.base_url.rstrip("/")

    async def request(
        self,
        method: str,
        table: str,
        sys_id: str | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ):

        url = f"{self.base_url}/api/now/table/{table}"

        if sys_id:
            url += f"/{sys_id}"

        async with httpx.AsyncClient(
            timeout=30,
            auth=(self.username, self.password),
        ) as client:

            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
            )

            response.raise_for_status()

            if response.status_code == 204:
                return {"success": True}

            return response.json()

    async def get(
        self,
        table: str,
        query: str | None = None,
        fields: str | None = None,
        limit: int = 10,
    ):

        params = {
            "sysparm_limit": limit,
            "sysparm_display_value": "true",
        }

        if query:
            params["sysparm_query"] = query

        if fields:
            params["sysparm_fields"] = fields

        return await self.request(
            "GET",
            table,
            params=params,
        )

    async def get_one(
        self,
        table: str,
        sys_id: str,
    ):

        return await self.request(
            "GET",
            table,
            sys_id=sys_id,
            params={
                "sysparm_display_value": "true"
            },
        )

    async def create(
        self,
        table: str,
        data: dict[str, Any],
    ):

        return await self.request(
            "POST",
            table,
            data=data,
        )

    async def update(
        self,
        table: str,
        sys_id: str,
        data: dict[str, Any],
    ):

        return await self.request(
            "PATCH",
            table,
            sys_id=sys_id,
            data=data,
        )