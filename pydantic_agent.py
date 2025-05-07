from pydantic import BaseModel
import mcp_client
from pydantic_ai import Agent

import asyncio
#Imports y creacción del modelo para Gemini
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
gemini_model = GeminiModel(
    'gemini-2.0-flash', provider=GoogleGLAProvider(api_key='AIzaSyAYXNByPMyooQTZDig21a088vAus0bnV0I')
)



#Imports y creacción del modelo para Ollama
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
# Ensure the Ollama model is properly initialized and integrated
ollama_model = OpenAIModel(
    model_name='qwen2.5:14b', 
    provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)



#Creacción del cliente y el agente, usa las tools ofrecidas en el .json especificado
# y el agente está creado con el modelo especificado.
# Update the get_pydantic_ai_agent function to use the Ollama model
async def get_pydantic_ai_agent():
    try:
        client = mcp_client.MCPClient()
        client.load_servers("GhidraMCP.json")
        tools = await client.start()
        return client, Agent(ollama_model, tools=tools)
    except Exception as e:
        print(f"Error initializing the agent: {e}")
        raise


#Logfire api para ver que nos dice que encuentra en una interfaz online, para comprobar los problemas con más facilidad
import logfire_api
logfire_api.configure()


#Creacción del main para correr el agente y crear una pequeña interfaz sencilla para el chat 
# Add error handling in the main function
async def main():
    try:
        client, agent = await get_pydantic_ai_agent()
        while True:
            user_input = input("\n[You]:")

            if user_input.lower() in ['exit', 'quit']:
                print("goodbye")
                break

            try:
                result = await agent.run(user_input)
                logfire_api.info(result.output)
                print("\n\n")
                print('[' + agent.model.model_name + ']:', result.output)
            except Exception as e:
                print(f"Error during agent execution: {e}")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == '__main__':
    asyncio.run(main())