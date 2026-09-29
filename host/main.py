
from pathlib import Path
import json

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


app = FastAPI(
    title="ServiceNow MCP Host",
    description="FastAPI Host for connecting to a ServiceNow MCP Server",
    version="1.0.0",
)


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home():

    index_file = STATIC_DIR / "index.html"

    return index_file.read_text(
        encoding="utf-8"
    )


# ---------------------------------------------------------
# Discover MCP tools
# ---------------------------------------------------------

@app.post("/tools")
async def list_tools(
    server_url: str = Form(...)
):

    async with streamable_http_client(server_url) as (
        read_stream,
        write_stream,
        _,
    ):

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            # Initialize MCP session
            await session.initialize()

            # Ask MCP server for available tools
            result = await session.list_tools()

            tools = []

            for tool in result.tools:

                tools.append(
                    {
                        "name": tool.name,
                        "description": tool.description,
                    }
                )

            return {
                "success": True,
                "tools": tools,
            }


# ---------------------------------------------------------
# Execute MCP tool
# ---------------------------------------------------------

@app.post("/call")
async def call_tool(
    server_url: str = Form(...),
    tool_name: str = Form(...),
    arguments: str = Form("{}"),
):

    try:

        # Convert JSON string from UI into Python dictionary
        tool_arguments = json.loads(arguments)

    except json.JSONDecodeError:

        return {
            "success": False,
            "error": "Invalid JSON arguments",
        }


    async with streamable_http_client(server_url) as (
        read_stream,
        write_stream,
        _,
    ):

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            # Initialize MCP session
            await session.initialize()

            # Execute requested MCP tool
            result = await session.call_tool(
                tool_name,
                tool_arguments,
            )

            # Convert MCP content into JSON-friendly format
            output = []

            for item in result.content:

                if hasattr(item, "text"):

                    output.append(
                        {
                            "type": "text",
                            "text": item.text,
                        }
                    )

                else:

                    output.append(
                        {
                            "type": str(
                                getattr(item, "type", "unknown")
                            )
                        }
                    )

            return {
                "success": True,
                "result": output,
            }

