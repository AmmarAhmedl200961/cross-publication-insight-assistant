"""
Fact-Checker Agent
Specializes in verifying suggestions against actual repository content
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List
import logging

logger = logging.getLogger(__name__)


class FactCheckerAgent:
    """
    Agent responsible for verifying that all suggestions and recommendations
    are factually correct and align with the actual repository content.
    """
    
    def __init__(self, tools: List, llm: ChatOpenAI):
        """
        Initialize the Fact-Checker Agent.
        
        Args:
            tools: List of tools available to the agent
            llm: Language model instance
        """
        self.tools = tools
        self.llm = llm
        
        self.agent = Agent(
            role='Accuracy Verification Specialist',
            goal='Verify that all suggestions and recommendations are factually correct '
                 'and accurately represent the actual repository content and capabilities',
            backstory="""You are a detail-oriented verification specialist with strong 
                        analytical skills and experience in fact-checking technical content. 
                        You excel at cross-referencing information and ensuring accuracy 
                        in technical documentation and project descriptions.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
    
    def get_agent(self) -> Agent:
        """Return the CrewAI agent instance."""
        return self.agent
