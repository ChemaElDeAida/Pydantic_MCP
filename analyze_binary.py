import asyncio
from pydantic_ai import Agent
import mcp_client
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
async def analyze_binary():
    try:
        # Initialize the MCP client and agents
        client = mcp_client.MCPClient()
        client.load_servers("GhidraMCP.json")
        tools = await client.start()

        gemini_model = GeminiModel(
            'gemini-2.0-flash', provider=GoogleGLAProvider(api_key='AIzaSyAYXNByPMyooQTZDig21a088vAus0bnV0I')
        )
        agent_gemini = Agent(gemini_model, tools=tools,
                             system_prompt="You will need to use the MCP tools to response the following questions, and please, take all the time you need.")

        claude_model = AnthropicModel('claude-3-7-sonnet-latest', 
                                      provider=AnthropicProvider(api_key='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')
        )
        agent_claude = Agent(claude_model, tools=tools,
                             system_prompt="You will need to use the MCP tools to response the following questions, and please, take all the time you need.")

        print("Agents initialized successfully.")

        # Ask the agents to analyze the binary
        questions = [
            "Can you identify the main function?",
            "Can you identify the password of the crackMe",
            "Can you list all the functions?"
        ]

        # Add specific questions for crackMe or malware binaries
        """if "crackme" in binary_path.lower():
            questions.append("What is the key or password required to crack this binary?")
            questions.append("Can you identify the anti-debugging techniques used in this binary?")
        elif "malware" in binary_path.lower():
            questions.append("What are the indicators of compromise (IOCs) for this malware?")
            questions.append("Can you identify the command-and-control (C2) server used by this malware?")"""

        for question in questions:
            print(f"[You]: {question}")
            result_gemini = await agent_gemini.run(f"{question}")
            print(f"[{agent_gemini.model.model_name}]: {result_gemini.output}\n")

            print(f"[You]: {question}")
            result_claude = await agent_claude.run(f"{question}")
            print(f"[{agent_claude.model.model_name}]: {result_claude.output}\n")

            # Save the question and answers to a .txt file
            with open("analysis_results.txt", "a") as file:
                file.write(f"[You]: {question}\n")
                file.write(f"[Gemini]: {result_gemini.output}\n")
                file.write(f"[Claude]: {result_claude.output}\n\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    
    asyncio.run(analyze_binary())