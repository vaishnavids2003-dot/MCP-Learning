from fastmcp import FastMCP

mcp = FastMCP("ServiceNow IT Service Desk")


@mcp.tool()
def search_incidents(query: str = "", limit: int = 10) -> dict:
    """Search ServiceNow incidents."""
    
    incidents = [
        {
            "number": "INC0010001",
            "short_description": "Laptop is not connecting to WiFi",
            "state": "In Progress",
            "priority": "2"
        },
        {
            "number": "INC0010002",
            "short_description": "VPN connection problem",
            "state": "Open",
            "priority": "3"
        }
    ]

    return {
        "query": query,
        "results": incidents[:limit]
    }


@mcp.tool()
def get_incident(sys_id: str) -> dict:
    """Get an incident by sys_id."""

    return {
        "sys_id": sys_id,
        "number": "INC0010001",
        "short_description": "Laptop is not connecting to WiFi",
        "state": "In Progress",
        "priority": "2"
    }


@mcp.tool()
def create_incident(
    short_description: str,
    description: str
) -> dict:
    """Create a new incident."""

    return {
        "success": True,
        "number": "INC0010099",
        "short_description": short_description,
        "description": description,
        "message": "Mock incident created successfully"
    }


@mcp.tool()
def server_info() -> dict:
    """Return information about this MCP server."""

    return {
        "server": "ServiceNow IT Service Desk MCP",
        "transport": "Streamable HTTP",
        "endpoint": "/mcp",
        "mode": "MOCK"
    }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000
    )