"""
Content Improver Agent
Specializes in enhancing project descriptions, titles, and documentation
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List
import logging

logger = logging.getLogger(__name__)


class ContentImproverAgent:
    """
    Agent responsible for enhancing project titles, descriptions,
    and documentation to make them more engaging and clear.
    """
    
    def __init__(self, tools: List, llm: ChatOpenAI):
        """
        Initialize the Content Improver Agent.
        
        Args:
            tools: List of tools available to the agent
            llm: Language model instance
        """
        self.tools = tools
        self.llm = llm
        
        self.agent = Agent(
            role='Technical Writing Specialist',
            goal='Enhance project titles, descriptions, and documentation to make '
                 'them more engaging, clear, and professionally presented',
            backstory="""You are a technical writer and communications specialist with 
                        years of experience in making complex technical projects accessible 
                        and appealing to diverse audiences. You excel at crafting compelling 
                        narratives around technology while maintaining technical accuracy.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
    
    def get_agent(self) -> Agent:
        """Return the CrewAI agent instance."""
        return self.agent
