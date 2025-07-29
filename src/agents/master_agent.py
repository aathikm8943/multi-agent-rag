import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.ollama import OllamaChatCompletionClient
from dotenv import load_dotenv
import os
import datetime
import re

from src.agents.code_review_agents.mulesoft_code_review_agent import MulesoftCodeReviewAgent
from src.agents.code_review_agents.general_code_review_agent import GeneralCodeReviewAgent

# Load API key
load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY')

mulesoft_code_review_agent = MulesoftCodeReviewAgent()
general_code_review_agent = GeneralCodeReviewAgent()

class MasterAgent():

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
        model_client = self._ModelConfig()

        assistant_agent = AssistantAgent(
            name = 'master_agent',
            model_client = model_client,
            system_message="""
                You are a helpful assistant Agent for code review. You will assist in reviewing code and providing suggestions.
            """
        )

        return assistant_agent
    
    async def GroupChatConfig(self):
        model_client = self._ModelConfig()

        selector_prompt = """
        You are a router. Select the best agent for the user's query:
        - If the query is general and not specific to coding or programming languages, then answer by yourself don't dicuss with any agents.
        - If the query is about MuleSoft, DataWeave, Anypoint Studio, or MuleSoft file types (.xml, .dwl, .json), select 'mulesoft_code_review_agent'.
        - For all other code or programming questions apart from the mulesoft, select 'common_code_review_agent'.
        Respond with only the agent name.
        """

        # Create a SelectorGroupChat with the model client
        selector_group_chat = SelectorGroupChat(
            name = "Code Review Agent",
            selector_prompt=selector_prompt,
            participants=[mulesoft_code_review_agent.AgentConfig(), general_code_review_agent.AgentConfig()],
            model_client=model_client,
            termination_condition=TextMentionTermination('stop'),
            max_turns=1
        )

        return selector_group_chat

    async def run_agent(self, query):
        assistant_agent = await self.GroupChatConfig()
        # assistant_agent = self.AgentConfig()
        print("Running the agent...")
        print("Query:", query)

        # Run the agent with the provided query
        result = await assistant_agent.run(task=query)

        ## Clean up the result to remove any unnecessary formatting
        response = result.messages[-1].content

        cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)

        return cleaned_response.strip()

if __name__ == "__main__":
    start = datetime.datetime.now()
    # Run the agent
    print("Starting the agent...")
    master_agent = MasterAgent()
    query = """<flow name="testFlow">
        <db:mysql-connection username="admin" password="123456"/>
    </flow>"""
    # query = "What is mulesoft?"
    # query = "What is mulesoft, how will it help in api development? What are common file types are there?"
    query = """
       Please review this MuleSoft code: 
        ```
        <flow name="myFlow">
            <http:listener path="/api/*"/>
            <db:select>
                <db:sql>SELECT * FROM users</db:sql>
            </db:select>
        </flow>
        ```
        """
    response = asyncio.run(master_agent.run_agent(query=query))
    end = datetime.datetime.now()
    print("Agent Response:")
    print(response)

    print(f"Time taken: {end - start} seconds")