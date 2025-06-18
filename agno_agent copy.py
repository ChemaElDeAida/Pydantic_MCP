import asyncio
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters

import json
# Load the bridge configuration from a JSON file
def load_bridge_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    return StdioServerParameters(
        command=cfg["command"],
        args=cfg.get("args", []),
        env=cfg.get("env", None),
    )

async def run_agent(message: str) -> None:
    """Run the GhidraMCP tool with the given message."""


    # MCP server to access the filesystem (via `npx`)
    configMCP = load_bridge_config("GhidraMCP_agno.json")
    async with MCPTools(f"python C:\\Users\\Alber\\Desktop\\TFM\\bridge_mcp_ghidra.py --ghidra-server http://127.0.0.1:8080/") as mcp_ghidra:
        agent = Agent(
            model=Gemini(id="gemini-2.0-flash", search=True, api_key="AIzaSyAYXNByPMyooQTZDig21a088vAus0bnV0I"),
            tools=[mcp_ghidra],
            instructions=dedent("""\
                You are an expert in reverse engeniering.
                                You will use the tools provided to analyze a binary file.
                                You will be precise and concise in your answers.
                                You will explain the steps you take to analyze the binary.
n\
            """),
            markdown=True,
            show_tool_calls=True,
            debug_mode=True
        )

        # Run the agent
        await agent.aprint_response(message, stream=True)


# Example usage
if __name__ == "__main__":
    # Basic example - exploring project license
    asyncio.run(run_agent("¿What reversing tools do you have?"))