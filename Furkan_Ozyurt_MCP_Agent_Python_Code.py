from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import asyncio
import os

# ------------------------------
# 1. Load environment variables
# ------------------------------
load_dotenv()

# Azure OpenAI configuration from .env
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_api_key = os.getenv("AZURE_OPENAI_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_VERSION")

# Firecrawl MCP API key from .env
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

# ------------------------------
# 2. Create LangChain AzureChatOpenAI LLM
# ------------------------------
llm = AzureChatOpenAI(
    deployment_name=deployment_name,
    openai_api_version=api_version,
    azure_endpoint=azure_endpoint,
    api_key=azure_api_key,
    temperature=0,
)

# ------------------------------
# 3. Configure Firecrawl MCP
# ------------------------------
server_params = StdioServerParameters(
    command="npx",  # Run Firecrawl MCP via npx
    env={"FIRECRAWL_API_KEY": firecrawl_api_key},
    args=["firecrawl-mcp"]
)

# ------------------------------
# 4. Main asynchronous function
# ------------------------------
async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)

            while True:
                username = input("\nEnter GitHub username (or 'quit'): ")
                if username.lower() == "quit":
                    break

                github_url = f"https://github.com/{username}?tab=repositories"

                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a career advisor AI assistant. "
                            "You can scrape GitHub repositories using Firecrawl and analyze them. "
                            "For a given GitHub user's repositories page:\n"
                            "1. Extract repository names, stars, and descriptions.\n"
                            "2. Analyze the main technical skills demonstrated (e.g. data engineering, "
                            "backend, frontend, AI/ML, DevOps, security).\n"
                            "3. Based on the skills and repo content, identify the TOP 3 most suitable "
                            "engineering roles for this person.\n"
                            "4. Justify why these roles are suitable, with a short explanation for each."
                        ),
                    },
                    {"role": "user", "content": f"Analyze repos from: {github_url}"}
                ]

                try:
                    response = await agent.ainvoke({"messages": messages})
                    ai_message = response["messages"][-1].content
                    print("\n--- Analysis Result ---\n")
                    print(ai_message)
                    print("\n-----------------------\n")

                except Exception as e:
                    print("Error:", e)

# ------------------------------
# 5. Run the program
# ------------------------------
if __name__ == "__main__":
    asyncio.run(main())
