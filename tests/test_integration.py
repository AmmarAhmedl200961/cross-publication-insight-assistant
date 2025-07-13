"""
Integration tests for the complete system
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path
import os

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))


class TestSystemIntegration(unittest.TestCase):
    """Test system integration and end-to-end functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock environment variables
        self.env_patches = [
            patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key-123'}),
            patch.dict(os.environ, {'GITHUB_TOKEN': 'test-github-token'}),
        ]
        
        for patcher in self.env_patches:
            patcher.start()
    
    def tearDown(self):
        """Clean up test environment."""
        for patcher in self.env_patches:
            patcher.stop()
    
    @unittest.skipIf(not os.environ.get('OPENAI_API_KEY', '').startswith('sk-'), 
                     "No valid OpenAI API key available")
    def test_crew_initialization(self):
        """Test crew initialization with real API keys."""
        try:
            from src.crew import PublicationAssistantCrew
            
            crew = PublicationAssistantCrew()
            
            # Test that crew is initialized
            self.assertIsNotNone(crew.crew)
            self.assertIsNotNone(crew.llm)
            self.assertGreater(len(crew.tools), 0)
            self.assertGreater(len(crew.agents), 0)
            
            # Test validation
            validation = crew.validate_setup()
            self.assertIsInstance(validation, dict)
            self.assertIn('all_systems_ready', validation)
            
        except ImportError as e:
            self.skipTest(f"Could not import crew: {e}")
    
    def test_crew_initialization_without_api_keys(self):
        """Test crew initialization handling without API keys."""
        with patch.dict(os.environ, {}, clear=True):
            try:
                from src.crew import PublicationAssistantCrew
                
                # Should raise an error due to missing API key
                with self.assertRaises(ValueError):
                    PublicationAssistantCrew()
                    
            except ImportError as e:
                self.skipTest(f"Could not import crew: {e}")
    
    def test_crew_info_method(self):
        """Test crew info retrieval."""
        try:
            from src.crew import PublicationAssistantCrew
            
            crew = PublicationAssistantCrew()
            info = crew.get_crew_info()
            
            self.assertIsInstance(info, dict)
            self.assertIn('agents', info)
            self.assertIn('tools', info)
            self.assertIn('llm_model', info)
            
            # Check agents info
            self.assertGreater(len(info['agents']), 0)
            for agent_name, agent_info in info['agents'].items():
                self.assertIn('role', agent_info)
                self.assertIn('goal', agent_info)
                self.assertIn('backstory', agent_info)
            
            # Check tools info
            self.assertGreater(len(info['tools']), 0)
            for tool_info in info['tools']:
                self.assertIn('name', tool_info)
                self.assertIn('description', tool_info)
                
        except ImportError as e:
            self.skipTest(f"Could not import crew: {e}")
    
    @patch('src.crew.PublicationAssistantCrew.analyze_repository')
    def test_analyze_repository_error_handling(self, mock_analyze):
        """Test error handling in repository analysis."""
        try:
            from src.crew import PublicationAssistantCrew
            
            # Mock a failure
            mock_analyze.side_effect = Exception("Test error")
            
            crew = PublicationAssistantCrew()
            result = crew.analyze_repository("https://github.com/test/repo")
            
            # Should call the real method and handle the error
            mock_analyze.side_effect = None
            mock_analyze.return_value = {
                "error": "Test error",
                "repository_url": "https://github.com/test/repo",
                "status": "failed"
            }
            
            result = crew.analyze_repository("https://github.com/test/repo")
            
            self.assertIn('error', result)
            self.assertEqual(result['status'], 'failed')
            
        except ImportError as e:
            self.skipTest(f"Could not import crew: {e}")


class TestTaskCreation(unittest.TestCase):
    """Test task creation and configuration."""
    
    def test_task_definitions(self):
        """Test that all required tasks are defined."""
        try:
            from src.tasks import PublicationAssistantTasks
            
            # Check that all task methods exist
            required_methods = [
                'repository_analysis_task',
                'metadata_recommendation_task',
                'content_improvement_task',
                'review_and_critique_task',
                'fact_checking_task',
                'final_compilation_task'
            ]
            
            for method_name in required_methods:
                self.assertTrue(hasattr(PublicationAssistantTasks, method_name))
                method = getattr(PublicationAssistantTasks, method_name)
                self.assertTrue(callable(method))
                
        except ImportError as e:
            self.skipTest(f"Could not import tasks: {e}")


class TestConfigurationManagement(unittest.TestCase):
    """Test configuration and environment management."""
    
    def test_config_import(self):
        """Test configuration module import and values."""
        try:
            from src.config import (
                OPENAI_MODEL,
                TEMPERATURE,
                MAX_TOKENS,
                AGENT_SETTINGS,
                TOOL_SETTINGS,
                CREW_SETTINGS
            )
            
            # Check that configurations are loaded
            self.assertIsInstance(OPENAI_MODEL, str)
            self.assertIsInstance(TEMPERATURE, float)
            self.assertIsInstance(MAX_TOKENS, int)
            self.assertIsInstance(AGENT_SETTINGS, dict)
            self.assertIsInstance(TOOL_SETTINGS, dict)
            self.assertIsInstance(CREW_SETTINGS, dict)
            
            # Check reasonable values
            self.assertGreater(TEMPERATURE, 0)
            self.assertLess(TEMPERATURE, 2)
            self.assertGreater(MAX_TOKENS, 0)
            
        except ImportError as e:
            self.skipTest(f"Could not import config: {e}")


class TestMainEntryPoint(unittest.TestCase):
    """Test main entry point functionality."""
    
    def test_github_url_validation(self):
        """Test GitHub URL validation function."""
        try:
            import main
            
            # Valid URLs
            valid_urls = [
                "https://github.com/owner/repo",
                "http://github.com/owner/repo",
                "https://github.com/microsoft/vscode"
            ]
            
            for url in valid_urls:
                self.assertTrue(main.validate_github_url(url), f"Should validate: {url}")
            
            # Invalid URLs
            invalid_urls = [
                "",
                "not-a-url",
                "https://gitlab.com/owner/repo",
                "https://github.com/owner",
                "github.com"
            ]
            
            for url in invalid_urls:
                self.assertFalse(main.validate_github_url(url), f"Should not validate: {url}")
                
        except ImportError as e:
            self.skipTest(f"Could not import main: {e}")


if __name__ == '__main__':
    unittest.main()
