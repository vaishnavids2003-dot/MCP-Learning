from mcp import Client


class MCPClient:

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.client = Client(server_url)

    async def connect(self):

        await self.client.__aenter__()

        return self.client

    async def close(self):

        await self.client.__aexit__(
            None,
            None,
            None,
        )

    async def list_tools(self):

        return await self.client.list_tools()

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):

        return await self.client.call_tool(
            tool_name,
            arguments,
        )