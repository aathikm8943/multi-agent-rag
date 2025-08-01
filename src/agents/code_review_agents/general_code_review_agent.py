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
                You are an intelligent code review assistant agent, capable of reviewing code across a wide range of programming languages, including Python, TypeScript, R, C, and C++, etc...

               When reviewing code:
            1. Use the analyze_mulesoft_code tool to find issues
            2. Structure your response as follows:
                - Analysis Summary
                - Critical Issues (if any)
                - High Priority Issues (if any)
                - Medium Priority Issues (if any)
                - Low Priority Issues (if any)
                - Recommendations for each issue
                - Best Practices and Improvements
            3. Provide the complete restructured code with all issues fixed
            4. Always provide code examples for fixes
            5. Follow sonarqube rules and code`  best practices
            5. Focus on:
                - Security vulnerabilities
                - Performance optimizations
                - Error handling
                - Code maintainability
               """
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