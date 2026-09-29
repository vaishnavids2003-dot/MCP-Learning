
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():

    # MCP server URL
    server_url = "http://127.0.0.1:8000/mcp"

    # Connect to the MCP server using Streamable HTTP
    async with streamable_http_client(server_url) as (
        read_stream,
        write_stream,
        _,
    ):

        # Create an MCP client session
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            # --------------------------------------------------
            # STEP 1: Initialize the MCP connection
            # --------------------------------------------------

            await session.initialize()

            print("\nConnected to MCP server!")

            # --------------------------------------------------
            # STEP 2: Discover available tools
            # --------------------------------------------------

            result = await session.list_tools()

            print("\nAvailable tools:")

            for tool in result.tools:
                print(f"- {tool.name}")

            # --------------------------------------------------
            # STEP 3: Call the search_incidents tool
            # --------------------------------------------------

            print("\nCalling search_incidents...")

            response = await session.call_tool(
                "search_incidents",
                {
                    "query": "wifi",
                    "limit": 5,
                },
            )

            # --------------------------------------------------
            # STEP 4: Display the tool response
            # --------------------------------------------------

            print("\nTool response:")

            print(response)


if __name__ == "__main__":
    asyncio.run(main())

