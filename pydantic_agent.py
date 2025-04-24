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
ollama_model = OpenAIModel(
    model_name='qwen2.5', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)



#Creacción del cliente y el agente, usa las tools ofrecidas en el .json especificado
# y el agente está creado con el modelo especificado.
async def get_pydantic_ai_agent():
    client = mcp_client.MCPClient()
    client.load_servers("GhidraMCP.json")
    tools = await client.start()
    return client, Agent(model=ollama_model, tools=tools)


#Creacción del main para correr el agente y crear una pequeña interfaz sencilla para el chat 
async def main():
    client, agent = await get_pydantic_ai_agent()
    while True:
        #Tell me all the files you can find in the directory
        user_input =input("\n[You]:")

        if user_input.lower() in ['exit', 'quit']:
            print ("goodbye")
            break
        
        result = await agent.run(user_input)
        print('['+agent.model.model_name+']:', result.output)

if __name__ == '__main__':
    asyncio.run(main())
