"""
Repository Analyzer Agent
Specializes in parsing and analyzing GitHub repository content
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List
import logging

logger = logging.getLogger(__name__)


class RepoAnalyzerAgent:
    """
    Agent responsible for analyzing GitHub repository structure, 
    README files, and codebase to understand project characteristics.
    """
    
    def __init__(self, tools: List, llm: ChatOpenAI):
        """
        Initialize the Repository Analyzer Agent.
        
        Args:
            tools: List of tools available to the agent
            llm: Language model instance
        """
        self.tools = tools
        self.llm = llm
        
        self.agent = Agent(
            role='Technical Analysis Specialist',
            goal='Analyze GitHub repositories to understand project structure, '
                 'technologies used, and overall project characteristics',
            backstory="""You are an experienced software engineer and technical analyst 
                        with deep expertise in various programming languages, frameworks, 
                        and software architectures. You excel at quickly understanding 
                        codebases and identifying key technical aspects of projects.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
    
    def get_agent(self) -> Agent:
        """Return the CrewAI agent instance."""
        return self.agent
