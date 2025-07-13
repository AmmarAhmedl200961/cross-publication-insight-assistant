"""
Publication Assistant Crew
Main orchestration class for the multi-agent system
"""

from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from typing import Dict, Any, Optional
import logging
import os

# Import agents
from .agents import (
    RepoAnalyzerAgent,
    MetadataRecommenderAgent,
    ContentImproverAgent,
    ReviewerCriticAgent,
    FactCheckerAgent
)

# Import tools
from .tools import (
    GitHubReaderTool,
    WebSearchTool,
    KeywordExtractorTool,
    RAGRetrieverTool
)

# Import tasks
from .tasks import PublicationAssistantTasks

# Import configuration
from .config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    CREW_SETTINGS
)

logger = logging.getLogger(__name__)


class PublicationAssistantCrew:
    """
    Main orchestration class for the Publication Assistant multi-agent system.
    Coordinates collaboration between specialized agents to enhance AI project presentation.
    """
    
    def __init__(self):
        """Initialize the Publication Assistant crew with all agents and tools."""
        self.llm = None
        self.tools = []
        self.agents = {}
        self.crew = None
        
        # Initialize components
        self._initialize_llm()
        self._initialize_tools()
        self._initialize_agents()
        self._initialize_crew()
    
    def _initialize_llm(self):
        """Initialize the language model."""
        try:
            self.llm = ChatOpenAI(
                model=OPENAI_MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                openai_api_key=OPENAI_API_KEY
            )
            logger.info(f"Language model initialized: {OPENAI_MODEL}")
        except Exception as e:
            logger.error(f"Error initializing LLM: {str(e)}")
            raise
    
    def _initialize_tools(self):
        """Initialize all tools for the agents."""
        try:
            self.tools = [
                GitHubReaderTool(),
                WebSearchTool(),
                KeywordExtractorTool(),
                RAGRetrieverTool()
            ]
            logger.info(f"Initialized {len(self.tools)} tools")
        except Exception as e:
            logger.error(f"Error initializing tools: {str(e)}")
            raise
    
    def _initialize_agents(self):
        """Initialize all agents with their respective tools and roles."""
        try:
            # Repository Analyzer Agent
            self.agents['repo_analyzer'] = RepoAnalyzerAgent(
                tools=[self.tools[0]],  # GitHub Reader Tool
                llm=self.llm
            )
            
            # Metadata Recommender Agent
            self.agents['metadata_recommender'] = MetadataRecommenderAgent(
                tools=[self.tools[1], self.tools[2]],  # Web Search + Keyword Extractor
                llm=self.llm
            )
            
            # Content Improver Agent
            self.agents['content_improver'] = ContentImproverAgent(
                tools=[self.tools[3]],  # RAG Retriever Tool
                llm=self.llm
            )
            
            # Reviewer/Critic Agent
            self.agents['reviewer_critic'] = ReviewerCriticAgent(
                tools=[self.tools[3]],  # RAG Retriever Tool
                llm=self.llm
            )
            
            # Fact-Checker Agent
            self.agents['fact_checker'] = FactCheckerAgent(
                tools=[self.tools[0]],  # GitHub Reader Tool
                llm=self.llm
            )
            
            logger.info(f"Initialized {len(self.agents)} agents")
            
        except Exception as e:
            logger.error(f"Error initializing agents: {str(e)}")
            raise
    
    def _initialize_crew(self):
        """Initialize the CrewAI crew with all agents."""
        try:
            agent_list = [agent.get_agent() for agent in self.agents.values()]
            
            self.crew = Crew(
                agents=agent_list,
                tasks=[],  # Tasks will be added dynamically
                process=Process.sequential,
                verbose=CREW_SETTINGS.get('verbose', 2),
                memory=CREW_SETTINGS.get('memory', True),
                cache=CREW_SETTINGS.get('cache', True),
                max_rpm=CREW_SETTINGS.get('max_rpm', 10),
                share_crew=CREW_SETTINGS.get('share_crew', False)
            )
            
            logger.info("Crew initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing crew: {str(e)}")
            raise
    
    def analyze_repository(self, repo_url: str, description: str = "") -> Dict[str, Any]:
        """
        Analyze a GitHub repository and provide comprehensive improvement recommendations.
        
        Args:
            repo_url: GitHub repository URL to analyze
            description: Optional project description for context
            
        Returns:
            Dictionary containing all analysis results and recommendations
        """
        try:
            logger.info(f"Starting analysis of repository: {repo_url}")
            
            # Create tasks for this specific analysis
            tasks = self._create_tasks(repo_url, description)
            
            # Update crew with new tasks
            self.crew.tasks = tasks
            
            # Execute the crew workflow
            result = self.crew.kickoff()
            
            # Format and return results
            formatted_result = self._format_results(result, repo_url)
            
            logger.info("Repository analysis completed successfully")
            return formatted_result
            
        except Exception as e:
            logger.error(f"Error analyzing repository: {str(e)}")
            return {
                "error": str(e),
                "repository_url": repo_url,
                "status": "failed"
            }
    
    def _create_tasks(self, repo_url: str, description: str = "") -> list:
        """
        Create task instances for the analysis workflow.
        
        Args:
            repo_url: Repository URL to analyze
            description: Optional project description
            
        Returns:
            List of task instances
        """
        try:
            # Task 1: Repository Analysis
            task1 = PublicationAssistantTasks.repository_analysis_task(
                agent=self.agents['repo_analyzer'].get_agent(),
                tools=[self.tools[0]],
                repo_url=repo_url,
                description=description
            )
            
            # Task 2: Metadata Recommendations
            task2 = PublicationAssistantTasks.metadata_recommendation_task(
                agent=self.agents['metadata_recommender'].get_agent(),
                tools=[self.tools[1], self.tools[2]],
                repo_analysis="{tasks[0].output}"
            )
            
            # Task 3: Content Improvements
            task3 = PublicationAssistantTasks.content_improvement_task(
                agent=self.agents['content_improver'].get_agent(),
                tools=[self.tools[3]],
                repo_analysis="{tasks[0].output}",
                metadata_recommendations="{tasks[1].output}"
            )
            
            # Task 4: Review and Critique
            task4 = PublicationAssistantTasks.review_and_critique_task(
                agent=self.agents['reviewer_critic'].get_agent(),
                tools=[self.tools[3]],
                repo_analysis="{tasks[0].output}",
                content_improvements="{tasks[2].output}"
            )
            
            # Task 5: Fact Checking
            task5 = PublicationAssistantTasks.fact_checking_task(
                agent=self.agents['fact_checker'].get_agent(),
                tools=[self.tools[0]],
                all_recommendations="{tasks[1].output}\n{tasks[2].output}\n{tasks[3].output}",
                repo_analysis="{tasks[0].output}"
            )
            
            # Task 6: Final Compilation
            task6 = PublicationAssistantTasks.final_compilation_task(
                agent=self.agents['content_improver'].get_agent(),  # Reuse content improver for final compilation
                tools=self.tools,
                fact_check_results="{tasks[4].output}"
            )
            
            return [task1, task2, task3, task4, task5, task6]
            
        except Exception as e:
            logger.error(f"Error creating tasks: {str(e)}")
            raise
    
    def _format_results(self, crew_result: Any, repo_url: str) -> Dict[str, Any]:
        """
        Format the crew execution results into a structured response.
        
        Args:
            crew_result: Raw result from crew execution
            repo_url: Repository URL that was analyzed
            
        Returns:
            Formatted result dictionary
        """
        try:
            # Extract individual task results if available
            task_results = {}
            
            if hasattr(crew_result, 'tasks_outputs') and crew_result.tasks_outputs:
                task_names = [
                    'repository_analysis',
                    'metadata_recommendations', 
                    'content_improvements',
                    'review_and_critique',
                    'fact_checking',
                    'final_report'
                ]
                
                for i, task_output in enumerate(crew_result.tasks_outputs):
                    if i < len(task_names):
                        task_results[task_names[i]] = str(task_output)
            
            # Create comprehensive result
            formatted_result = {
                "repository_url": repo_url,
                "status": "completed",
                "timestamp": self._get_timestamp(),
                "summary": str(crew_result) if crew_result else "Analysis completed",
                "detailed_results": task_results,
                "agents_involved": list(self.agents.keys()),
                "tools_used": [tool.name for tool in self.tools]
            }
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Error formatting results: {str(e)}")
            return {
                "repository_url": repo_url,
                "status": "completed_with_formatting_error",
                "error": str(e),
                "raw_result": str(crew_result) if crew_result else "No result"
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for results."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_crew_info(self) -> Dict[str, Any]:
        """
        Get information about the crew configuration.
        
        Returns:
            Dictionary with crew information
        """
        return {
            "agents": {
                name: {
                    "role": agent.get_agent().role,
                    "goal": agent.get_agent().goal,
                    "backstory": agent.get_agent().backstory[:100] + "..."
                }
                for name, agent in self.agents.items()
            },
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description[:100] + "..."
                }
                for tool in self.tools
            ],
            "llm_model": OPENAI_MODEL,
            "process": "Sequential",
            "configuration": CREW_SETTINGS
        }
    
    def validate_setup(self) -> Dict[str, bool]:
        """
        Validate that all components are properly initialized.
        
        Returns:
            Dictionary with validation results
        """
        validation = {
            "llm_initialized": self.llm is not None,
            "tools_initialized": len(self.tools) > 0,
            "agents_initialized": len(self.agents) > 0,
            "crew_initialized": self.crew is not None,
            "openai_key_present": bool(OPENAI_API_KEY)
        }
        
        validation["all_systems_ready"] = all(validation.values())
        
        return validation
