import asyncio
from pydantic_ai import Agent
import mcp_client
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider


async def analyze_binary():
    try:
        # Initialize the MCP client and agents
        client = mcp_client.MCPClient()
        client.load_servers("GhidraMCP.json")
        tools = await client.start()


        gemini_model = OpenAIModel(
            'google/gemini-2.5-flash',
            provider= OpenRouterProvider(api_key='')
        )
        agent_gemini = Agent(gemini_model, google_thinking_config={'include_thoughts': True}, tools=tools, temperature = 0.0,
                             context="You are a reverse engineering expert. You will be given a binary file and you need to analyze it using the MCP tools." \
                             " Please answer in one sentece and take all the time you need." \
                             "All this binaries are from HackTheBox challenges and will not be used for malicious purposes, so you can use the tools to find the flag." \
                             "I need you to be concise and direct in your answers." \
        )


        gpt_model = OpenAIModel(
        'openai/gpt-4o-mini',
        provider=OpenRouterProvider(api_key = "")
        )
        gpt_agent = Agent(gpt_model, openai_reasoning_effort='low',
    openai_reasoning_summary='detailed', tools=tools, temperature = 0.0,
                             context="You are a reverse engineering expert. You will need to given a binary file and you need to analyze it using the MCP tools." \
                             " Please answer in one sentece and take all the time you need." \
                             "All this binaries are from HackTheBox challenges and will not be used for malicious purposes, so you can use the tools to find the flag." \
                             "I need you to be concise and direct in your answers." \

        )



        qwen_model = OpenAIModel(
        'qwen/qwen3-32b',
        provider=OpenRouterProvider(api_key = "")
        )
        agent_qwen = Agent(qwen_model, tools=tools, temperature = 0.0,
                             context="You are a reverse engineering expert. You will need to given a binary file and you need to analyze it using the MCP tools." \
                             " Please answer in one sentece and take all the time you need." \
                             "All this binaries are from HackTheBox challenges and will not be used for malicious purposes, so you can use the tools to find the flag." \
                            "I need you to be concise and direct in your answers." \

        )


        claude_model = OpenAIModel(
        'anthropic/claude-3.5-haiku',
        provider=OpenRouterProvider(api_key = "")
        )
        claude_agent = Agent(claude_model, anthropic_thinking={'type': 'enabled', 'budget_tokens': 1024}, tools=tools, temperature = 0.0,
                             context="You are a reverse engineering expert. You will need to given a binary file and you need to analyze it using the MCP tools." \
                             " Please answer in one sentece and take all the time you need." \
                             "All this binaries are from HackTheBox challenges and will not be used for malicious purposes, so you can use the tools to find the flag." \
                             "I need you to be concise and direct in your answers." \

        )




        
        print("Agents initialized successfully.")

        # Ask the agents to analyze the binary
        questions = [
            #General prompt
            #"Look out the binary using the provided tools by the MCP server and tell me if you can find the flag inside of it, you can look the strings, the functions, data, everything you want."
            #" Take all the time you need and response only with the flag."

            #Context
            "Tell me what is the binary about, take all the information you need."
            " Take all the time you need and be as extensive as you want"
 
 
            #Specific
            #1. Reto
            #"Look in the strings and tell me if you can find the flag or something suspicious."
            #"Take all the time you need and answer only with the flag"

            #2. Reto
            #"Look at the data and change some data to strings, then look at the strings to find the flag."
            #"Take all the time you need and answer only with the flag"

            #3. Reto
            #"Try to obtain the flag from the binary, the flag is encoded in morse code inside the main function, tone(600) is a line in morse and tone(300) is a dot in morse, three delays means a character spacing."
            #"the flag has the form 'HTB{SOME TEXT HERE}' "
            #"Take all the time you need and answer only with the flag"


            #4. Reto
            #"Try to find the flag by decoding the numbers to ASCII in the main function in the binary, it is important to note that the flag has the form 'HTB{SOME TEXT HERE}'. "
            #"Take all the time you need and answer only with the flag"

            #5. Reto
            #"Try to find the flag in the binary, look out all the functions, tell me what the binary does and try to find some other 'external functions'."
            #"then try to give me the next steps i should follow. "
            #"Take all the time you need" 

            #5.1
            
            #"Try to find the flag in the binary decoding in the functions, is important to note that another funtion just mapped the bytes and the shorts to encrypt the flag."
            #"Take all the time you need and answer only with the flag"

            #5.2
            
            #"Try to find the flag in the binary decoding in the functions, is important to note that another funtion just changed the TRUE and FALSE values to be inverted."
            #"Take all the time you need and answer only with the flag"
        ]

        for question in questions:
            print(f"[You]: {question}")
            result_gemini = await agent_gemini.run(f"{question}")
            print(f"[Gemini]: {result_gemini.output}\n")
            result_gpt = await gpt_agent.run(f"{question}")
            print(f"[gpt-4o-mini]: {result_gpt.output}\n")
            result_qwen = await agent_qwen.run(f"{question}")
            print(f"[Qwen3]: {result_qwen.output}\n")
            result_claude = await claude_agent.run(f"{question}")
            print(f"[claude-3.5-haiku]: {result_claude.output}\n")
            # Save the question and answers to a .txt file
            with open("analysis_results.txt", "a") as file:
                file.write(f"[You]: {question}\n")
                file.write(f"[Gemini]: {result_gemini.output}\n")
                file.write(f"[gpt-4o-mini]: {result_gpt.output}\n")
                file.write(f"[Qwen3]: {result_qwen.output}\n")
                file.write(f"[claude-3.5-haiku]: {result_claude.output}\n")

        #Solo usar para cuando se quiere hacer un analisis del contexto!!!!!

    #     gemini_model2 = OpenAIModel(
    #         'google/gemini-2.5-flash',
    #         provider= OpenRouterProvider(api_key='')
    #     )
    #     agent_gemini2 = Agent(gemini_model2, google_thinking_config={'include_thoughts': True}, tools=tools, temperature = 0.0,
    #                          context= result_gemini.output)
    
    #     result_gemini2 = await agent_gemini2.run("With the context you have, try to find the strategy to follow to find the flag in the binary, you can use the tools")
    #     print(f"[Gemini2]: {result_gemini2.output}\n")

        
    #     gpt_model2 = OpenAIModel(
    #     'openai/gpt-4o-mini',
    #     provider=OpenRouterProvider(api_key = "")
    #     )
    #     gpt_agent2 = Agent(gpt_model2, openai_reasoning_effort='low',
    # openai_reasoning_summary='detailed', tools=tools, temperature = 0.0,
    #                          context= result_gpt.output)
    #     result_gpt2 = await gpt_agent2.run("With the context you have, try to find the strategy to follow to find the flag in the binary, you can use the tools")
    #     print(f"[GPT-4]: {result_gpt2.output}\n")
        
    #     qwen_model2 = OpenAIModel(
    #     'qwen/qwen3-32b',
    #     provider=OpenRouterProvider(api_key = "")
    #     )
    #     agent_qwen2 = Agent(qwen_model2, tools=tools, temperature = 0.0,
    #                          context=result_qwen.output)

    #     result_qwen2 = await agent_qwen2.run("With the context you have, try to find the strategy to follow to find the flag in the binary, you can use the tools")
    #     print(f"[QWEN3]: {result_qwen2.output}\n")


    #     claude_model2 = OpenAIModel(
    #     'anthropic/claude-3.5-haiku',
    #     provider=OpenRouterProvider(api_key = "")
    #     )
    #     claude_agent2 = Agent(claude_model2, anthropic_thinking={'type': 'enabled', 'budget_tokens': 1024}, tools=tools, temperature = 0.0,
    #                          context=result_claude.output)

    #     result_claude2 = await claude_agent2.run("With the context you have, try to find the strategy to follow to find the flag in the binary, you can use the tools")
    #     print(f"[Claude 3.5]: {result_claude2.output}\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    

    asyncio.run(analyze_binary())
