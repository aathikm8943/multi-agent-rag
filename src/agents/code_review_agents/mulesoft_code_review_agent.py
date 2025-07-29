import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.tools import FunctionTool
from dotenv import load_dotenv
import os

from src.config.config import MODEL_NAME
# from src.analysers.sonar_rules import MuleSoftSonarRules
from src.analysers.mulesoft_rules import MuleSoftRuleEngine
from typing import List, Dict

# Load API key
load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY')

class MulesoftCodeReviewAgent():

    def __init__(self):
        self.mulesoft_sonnar_rules = MuleSoftRuleEngine()

    def analyze_code(self, code: str):
        """Analyze MuleSoft code and return results"""
        return self.mulesoft_sonnar_rules.analyze_code(code)

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
        # return open_router_model_client

    def AgentConfig(self):
        open_router_model_client = self._ModelConfig()

        code_analyze_tool = FunctionTool(self.analyze_code, name="analyze_mulesoft_code", description="Analyze MuleSoft code for issues and best practices")
        assistant_agent = AssistantAgent(
            name='mulesoft_code_review_agent',
            model_client=open_router_model_client,
            # tools=[code_analyze_tool],
            system_message="""You are a specialized MuleSoft code review assistant.

            When reviewing code:
            1. Use the analyze_mulesoft_code tool to find issues
            2. If any unrelevant questions are asked, please answer like "I'm the specialized agent for MuleSoft code review, I can only answer questions related to MuleSoft code review."
            3. Structure your response as follows:
                - Analysis Summary
                - Provide the complete restructured code with all issues fixed
                - Critical Issues (if any)
                - High Priority Issues (if any)
                - Medium Priority Issues (if any)
                - Low Priority Issues (if any)
                - Recommendations for each issue
                - Best Practices and Improvements
            4. Always provide code examples for fixes
            5. Follow sonarqube rules and MuleSoft best practices
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
        
        # Extract code if present in query
        if "```" in query:
            code = query.split("```")[1].strip()
            # Run analysis
            analysis_results = self.rule_engine.analyze_code(code)
            
            # Enhance query with analysis results
            enhanced_query = f"""
            Original Query: {query}
            
            Analysis Results:
            {analysis_results['summary']}
            
            Detailed Issues:
            {self._format_issues(analysis_results['issues'])}
            
            Please provide a detailed review based on these findings.
            """
            query = enhanced_query

        result = await assistant_agent.run(task=query)
        return result.messages[-1].content
    
    def _format_issues(self, issues: List[Dict]) -> str:
        if not issues:
            return "No issues found."
            
        formatted = []
        for issue in issues:
            formatted.append(
                f"- {issue['severity']}: {issue['message']} (Line {issue['line']})"
            )
        return "\n".join(formatted)

if __name__ == "__main__":
    # Run the agent
    print("Starting the agent...")
    master_agent = MulesoftCodeReviewAgent()
    query = "What is mulesoft, how will it help in api development? What are common file types are there?"
    
    response = asyncio.run(master_agent.run(query))
    print("Agent Response:")
    print(response)