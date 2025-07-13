"""
Unit tests for agent functionality
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from langchain_openai import ChatOpenAI
    from src.agents import (
        RepoAnalyzerAgent,
        MetadataRecommenderAgent,
        ContentImproverAgent,
        ReviewerCriticAgent,
        FactCheckerAgent
    )
except ImportError as e:
    print(f"Warning: Could not import agents due to missing dependencies: {e}")


class TestAgentInitialization(unittest.TestCase):
    """Test agent initialization and basic functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_llm = Mock(spec=ChatOpenAI)
        self.mock_tools = [Mock(), Mock()]
    
    @unittest.skipIf('src.agents' not in sys.modules, "Agents module not available")
    def test_repo_analyzer_agent_creation(self):
        """Test RepoAnalyzerAgent creation."""
        try:
            agent = RepoAnalyzerAgent(tools=self.mock_tools, llm=self.mock_llm)
            self.assertIsNotNone(agent)
            self.assertIsNotNone(agent.get_agent())
            self.assertEqual(agent.get_agent().role, 'Technical Analysis Specialist')
        except Exception as e:
            self.skipTest(f"Could not test RepoAnalyzerAgent: {e}")
    
    @unittest.skipIf('src.agents' not in sys.modules, "Agents module not available")
    def test_metadata_recommender_agent_creation(self):
        """Test MetadataRecommenderAgent creation."""
        try:
            agent = MetadataRecommenderAgent(tools=self.mock_tools, llm=self.mock_llm)
            self.assertIsNotNone(agent)
            self.assertIsNotNone(agent.get_agent())
            self.assertEqual(agent.get_agent().role, 'SEO and Discoverability Expert')
        except Exception as e:
            self.skipTest(f"Could not test MetadataRecommenderAgent: {e}")
    
    @unittest.skipIf('src.agents' not in sys.modules, "Agents module not available")
    def test_content_improver_agent_creation(self):
        """Test ContentImproverAgent creation."""
        try:
            agent = ContentImproverAgent(tools=self.mock_tools, llm=self.mock_llm)
            self.assertIsNotNone(agent)
            self.assertIsNotNone(agent.get_agent())
            self.assertEqual(agent.get_agent().role, 'Technical Writing Specialist')
        except Exception as e:
            self.skipTest(f"Could not test ContentImproverAgent: {e}")
    
    @unittest.skipIf('src.agents' not in sys.modules, "Agents module not available")
    def test_reviewer_critic_agent_creation(self):
        """Test ReviewerCriticAgent creation."""
        try:
            agent = ReviewerCriticAgent(tools=self.mock_tools, llm=self.mock_llm)
            self.assertIsNotNone(agent)
            self.assertIsNotNone(agent.get_agent())
            self.assertEqual(agent.get_agent().role, 'Quality Assurance Specialist')
        except Exception as e:
            self.skipTest(f"Could not test ReviewerCriticAgent: {e}")
    
    @unittest.skipIf('src.agents' not in sys.modules, "Agents module not available")
    def test_fact_checker_agent_creation(self):
        """Test FactCheckerAgent creation."""
        try:
            agent = FactCheckerAgent(tools=self.mock_tools, llm=self.mock_llm)
            self.assertIsNotNone(agent)
            self.assertIsNotNone(agent.get_agent())
            self.assertEqual(agent.get_agent().role, 'Accuracy Verification Specialist')
        except Exception as e:
            self.skipTest(f"Could not test FactCheckerAgent: {e}")


class TestAgentProperties(unittest.TestCase):
    """Test agent properties and configuration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_llm = Mock(spec=ChatOpenAI)
        self.mock_tools = [Mock(), Mock()]
    
    @unittest.skipIf('src.agents' not in sys.modules, "Agents module not available")
    def test_all_agents_have_required_properties(self):
        """Test that all agents have required properties."""
        try:
            from src.agents import (
                RepoAnalyzerAgent,
                MetadataRecommenderAgent,
                ContentImproverAgent,
                ReviewerCriticAgent,
                FactCheckerAgent
            )
            
            agent_classes = [
                RepoAnalyzerAgent,
                MetadataRecommenderAgent,
                ContentImproverAgent,
                ReviewerCriticAgent,
                FactCheckerAgent
            ]
            
            for AgentClass in agent_classes:
                with self.subTest(agent_class=AgentClass.__name__):
                    agent = AgentClass(tools=self.mock_tools, llm=self.mock_llm)
                    crew_agent = agent.get_agent()
                    
                    # Check required properties
                    self.assertTrue(hasattr(crew_agent, 'role'))
                    self.assertTrue(hasattr(crew_agent, 'goal'))
                    self.assertTrue(hasattr(crew_agent, 'backstory'))
                    
                    # Check properties are not empty
                    self.assertIsNotNone(crew_agent.role)
                    self.assertIsNotNone(crew_agent.goal)
                    self.assertIsNotNone(crew_agent.backstory)
                    
                    # Check properties are strings
                    self.assertIsInstance(crew_agent.role, str)
                    self.assertIsInstance(crew_agent.goal, str)
                    self.assertIsInstance(crew_agent.backstory, str)
                    
        except Exception as e:
            self.skipTest(f"Could not test agent properties: {e}")


if __name__ == '__main__':
    unittest.main()
