from mcp.server.fastmcp import FastMCP

from server.servicenow import ServiceNowClient


mcp = FastMCP(
    "ServiceNow IT Service Desk"
)

snow = ServiceNowClient()


# --------------------------------------------------
# INCIDENTS
# --------------------------------------------------

@mcp.tool()
async def search_incidents(
    query: str = "",
    limit: int = 10,
) -> dict:
    """
    Search ServiceNow incidents.

    Examples:
    - active=true
    - priority=1
    - state=2
    - short_descriptionLIKEVPN
    """

    return await snow.get(
        table="incident",
        query=query,
        fields=(
            "sys_id,"
            "number,"
            "short_description,"
            "description,"
            "state,"
            "priority,"
            "urgency,"
            "impact,"
            "assigned_to,"
            "assignment_group,"
            "caller_id,"
            "opened_at"
        ),
        limit=min(limit, 50),
    )


@mcp.tool()
async def get_incident(
    sys_id: str,
) -> dict:
    """
    Get a single ServiceNow incident by sys_id.
    """

    return await snow.get_one(
        table="incident",
        sys_id=sys_id,
    )


@mcp.tool()
async def create_incident(
    short_description: str,
    description: str,
    urgency: str = "3",
    impact: str = "3",
) -> dict:
    """
    Create a new ServiceNow incident.
    """

    data = {
        "short_description": short_description,
        "description": description,
        "urgency": urgency,
        "impact": impact,
    }

    return await snow.create(
        table="incident",
        data=data,
    )


@mcp.tool()
async def update_incident(
    sys_id: str,
    fields: dict,
) -> dict:
    """
    Update an existing incident.

    Example fields:
    {
        "comments": "Investigating the issue",
        "urgency": "2",
        "state": "2"
    }
    """

    return await snow.update(
        table="incident",
        sys_id=sys_id,
        data=fields,
    )


@mcp.tool()
async def resolve_incident(
    sys_id: str,
    resolution_notes: str,
) -> dict:
    """
    Resolve a ServiceNow incident.
    """

    data = {
        "state": "6",
        "close_notes": resolution_notes,
    }

    return await snow.update(
        table="incident",
        sys_id=sys_id,
        data=data,
    )


# --------------------------------------------------
# KNOWLEDGE
# --------------------------------------------------

@mcp.tool()
async def search_knowledge(
    query: str,
    limit: int = 10,
) -> dict:
    """
    Search ServiceNow knowledge articles.
    """

    encoded_query = f"short_descriptionLIKE{query}^ORtextLIKE{query}"

    return await snow.get(
        table="kb_knowledge",
        query=encoded_query,
        fields=(
            "sys_id,"
            "number,"
            "short_description,"
            "text,"
            "workflow_state,"
            "published"
        ),
        limit=min(limit, 50),
    )


# --------------------------------------------------
# USERS
# --------------------------------------------------

@mcp.tool()
async def get_user(
    username: str,
) -> dict:
    """
    Find a ServiceNow user by username.
    """

    return await snow.get(
        table="sys_user",
        query=f"user_name={username}",
        fields=(
            "sys_id,"
            "user_name,"
            "name,"
            "email,"
            "active,"
            "department"
        ),
        limit=5,
    )


# --------------------------------------------------
# CHANGE REQUESTS
# --------------------------------------------------

@mcp.tool()
async def search_changes(
    query: str = "",
    limit: int = 10,
) -> dict:
    """
    Search ServiceNow change requests.
    """

    return await snow.get(
        table="change_request",
        query=query,
        fields=(
            "sys_id,"
            "number,"
            "short_description,"
            "description,"
            "state,"
            "priority,"
            "risk,"
            "start_date,"
            "end_date,"
            "assigned_to,"
            "assignment_group"
        ),
        limit=min(limit, 50),
    )


@mcp.tool()
async def get_change(
    sys_id: str,
) -> dict:
    """
    Get a ServiceNow change request.
    """

    return await snow.get_one(
        table="change_request",
        sys_id=sys_id,
    )


# --------------------------------------------------
# PROBLEMS
# --------------------------------------------------

@mcp.tool()
async def search_problems(
    query: str = "",
    limit: int = 10,
) -> dict:
    """
    Search ServiceNow problem records.
    """

    return await snow.get(
        table="problem",
        query=query,
        fields=(
            "sys_id,"
            "number,"
            "short_description,"
            "description,"
            "state,"
            "priority,"
            "assigned_to,"
            "assignment_group"
        ),
        limit=min(limit, 50),
    )


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@mcp.tool()
def server_info() -> dict:
    """
    Return information about this ServiceNow MCP server.
    """

    return {
        "server": "ServiceNow IT Service Desk MCP",
        "service": "ServiceNow",
        "transport": "Streamable HTTP",
        "endpoint": "/mcp",
    }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )