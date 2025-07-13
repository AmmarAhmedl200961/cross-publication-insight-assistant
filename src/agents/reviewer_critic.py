"""
Reviewer/Critic Agent
Specializes in identifying missing sections and areas for improvement
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List
import logging

logger = logging.getLogger(__name__)


class ReviewerCriticAgent:
    """
    Agent responsible for reviewing project documentation and
    identifying missing sections or areas that need improvement.
    """
    
    def __init__(self, tools: List, llm: ChatOpenAI):
        """
        Initialize the Reviewer/Critic Agent.
        
        Args:
            tools: List of tools available to the agent
            llm: Language model instance
        """
        self.tools = tools
        self.llm = llm
        
        self.agent = Agent(
            role='Quality Assurance Specialist',
            goal='Review project documentation and identify missing sections, '
                 'unclear information, and areas that need improvement',
            backstory="""You are a meticulous quality assurance specialist and project 
                        reviewer with extensive experience in software documentation standards. 
                        You have a keen eye for detail and understand what makes project 
                        documentation complete, clear, and user-friendly.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
    
    def get_agent(self) -> Agent:
        """Return the CrewAI agent instance."""
        return self.agent
