"""
Metadata Recommender Agent
Specializes in suggesting tags, categories, and keywords for projects
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List
import logging

logger = logging.getLogger(__name__)


class MetadataRecommenderAgent:
    """
    Agent responsible for recommending metadata, tags, categories,
    and keywords to improve project discoverability.
    """
    
    def __init__(self, tools: List, llm: ChatOpenAI):
        """
        Initialize the Metadata Recommender Agent.
        
        Args:
            tools: List of tools available to the agent
            llm: Language model instance
        """
        self.tools = tools
        self.llm = llm
        
        self.agent = Agent(
            role='SEO and Discoverability Expert',
            goal='Recommend optimal tags, categories, and keywords to maximize '
                 'project visibility and discoverability on platforms like GitHub',
            backstory="""You are a digital marketing specialist with extensive experience 
                        in SEO, content categorization, and technical project promotion. 
                        You understand how developers search for projects and what keywords 
                        drive discovery in the tech community.""",
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            llm=self.llm
        )
    
    def get_agent(self) -> Agent:
        """Return the CrewAI agent instance."""
        return self.agent
