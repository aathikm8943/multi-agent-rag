import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.ollama import OllamaChatCompletionClient
from dotenv import load_dotenv
import os

from src.config.config import MODEL_NAME

# Load API key
load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY')

class GeneralCodeReviewAgent():

    def _ModelConfig(self):
        # open_router_model_client =  OpenAIChatCompletionClient(
        #     base_url="https://openrouter.ai/api/v1",
        #     model="qwen/qwen3-coder:free",
        #     api_key = OPEN_ROUTER_API_KEY,
        #     model_info={
        #         "family":'qwen',
        #         "vision" :True,
        #         "function_calling":True,
        #         "json_output": False,
        #         "structured_output": False,
        #     }
        # )

        ollama_client = OllamaChatCompletionClient(
            model="qwen3:1.7b",)

        return ollama_client

    def AgentConfig(self):
        open_router_model_client = self._ModelConfig()

        assistant_agent = AssistantAgent(
            name = 'common_code_review_agent',
            model_client = open_router_model_client,
            system_message="""
                You are an intelligent code review assistant agent, capable of reviewing code across a wide range of programming languages, including Python, TypeScript, R, C, and C++.
                """

                # Your role is to:

                # 1. Perform thorough and strict code reviews.
                # 2. Analyze code quality based on SonarQube rules and industry best practices.
                # 3. Provide actionable suggestions to improve code quality, performance, and security.
                # 4. Guide developers with precise and context-aware recommendations for refactoring or fixing issues.
                # 5. Your focus is to enhance code reliability and maintainability across MuleSoft projects.
        )

        return assistant_agent

    async def run(self, query):
        assistant_agent = self.AgentConfig()

        # Run the agent with the provided query
        result = await assistant_agent.run(task=query)

        return result.messages[-1].content

if __name__ == "__main__":
    # Run the agent
    print("Starting the agent...")
    master_agent = GeneralCodeReviewAgent()
    query = "What is mulesoft, how will it help in api development? What are common file types are there?"
    response = asyncio.run(master_agent.run(query))
    print("Agent Response:")
    print(response)