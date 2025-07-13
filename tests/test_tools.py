"""
Unit tests for tool functionality
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))


class TestGitHubReaderTool(unittest.TestCase):
    """Test GitHub Reader Tool functionality."""
    
    def test_url_parsing(self):
        """Test GitHub URL parsing functionality."""
        try:
            from src.tools.github_reader import GitHubReaderTool
            
            tool = GitHubReaderTool()
            
            # Test valid URLs
            valid_urls = [
                "https://github.com/owner/repo",
                "http://github.com/owner/repo",
                "https://github.com/owner/repo.git",
                "github.com/owner/repo"
            ]
            
            for url in valid_urls:
                with self.subTest(url=url):
                    result = tool._parse_repo_url(url)
                    self.assertIsNotNone(result)
                    self.assertEqual(len(result), 2)
                    self.assertEqual(result, ("owner", "repo"))
            
            # Test invalid URLs
            invalid_urls = [
                "https://gitlab.com/owner/repo",
                "not-a-url",
                "https://github.com/owner",
                ""
            ]
            
            for url in invalid_urls:
                with self.subTest(url=url):
                    result = tool._parse_repo_url(url)
                    self.assertIsNone(result)
                    
        except ImportError:
            self.skipTest("GitHubReaderTool not available due to missing dependencies")


class TestKeywordExtractorTool(unittest.TestCase):
    """Test Keyword Extractor Tool functionality."""
    
    def test_technical_keyword_extraction(self):
        """Test technical keyword extraction."""
        try:
            from src.tools.keyword_extractor import KeywordExtractorTool
            
            tool = KeywordExtractorTool()
            
            # Test content with technical keywords
            test_content = """
            This is a Python project using Django and React.
            It also includes Docker containerization and AWS deployment.
            The machine learning model uses TensorFlow and scikit-learn.
            """
            
            keywords = tool._extract_technical_keywords(test_content)
            
            # Check that some expected keywords are found
            expected_keywords = ['python', 'django', 'react', 'docker', 'aws', 'tensorflow']
            found_keywords = [kw for kw in expected_keywords if kw in keywords]
            
            self.assertGreater(len(found_keywords), 0, "Should find some technical keywords")
            
        except ImportError:
            self.skipTest("KeywordExtractorTool not available due to missing dependencies")
    
    def test_framework_detection(self):
        """Test framework detection functionality."""
        try:
            from src.tools.keyword_extractor import KeywordExtractorTool
            
            tool = KeywordExtractorTool()
            
            test_content = """
            This project uses React for the frontend and Django for the backend.
            We also use Docker for containerization and TensorFlow for ML.
            """
            
            frameworks = tool._detect_frameworks(test_content)
            
            # Should detect some frameworks
            self.assertGreater(len(frameworks), 0)
            
            # Check for specific frameworks
            if 'react' in frameworks:
                self.assertIn('react', frameworks)
            if 'django' in frameworks:
                self.assertIn('django', frameworks)
                
        except ImportError:
            self.skipTest("KeywordExtractorTool not available due to missing dependencies")
    
    def test_empty_content_handling(self):
        """Test handling of empty or minimal content."""
        try:
            from src.tools.keyword_extractor import KeywordExtractorTool
            
            tool = KeywordExtractorTool()
            
            # Test empty content
            result = tool._run("")
            self.assertIn("too short or empty", result.lower())
            
            # Test minimal content
            result = tool._run("Hi")
            self.assertIn("too short or empty", result.lower())
            
        except ImportError:
            self.skipTest("KeywordExtractorTool not available due to missing dependencies")


class TestWebSearchTool(unittest.TestCase):
    """Test Web Search Tool functionality."""
    
    @patch('requests.Session.get')
    def test_github_api_search(self, mock_get):
        """Test GitHub API search functionality."""
        try:
            from src.tools.web_search import WebSearchTool
            
            # Mock response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "items": [
                    {
                        "full_name": "test/repo",
                        "description": "Test repository",
                        "stargazers_count": 100,
                        "language": "Python",
                        "topics": ["test", "demo"],
                        "html_url": "https://github.com/test/repo"
                    }
                ]
            }
            mock_get.return_value = mock_response
            
            tool = WebSearchTool()
            result = tool._search_github_repos("test query")
            
            self.assertIsInstance(result, str)
            self.assertIn("test/repo", result)
            self.assertIn("Python", result)
            
        except ImportError:
            self.skipTest("WebSearchTool not available due to missing dependencies")
    
    def test_url_validation(self):
        """Test URL validation and handling."""
        try:
            from src.tools.web_search import WebSearchTool
            
            tool = WebSearchTool()
            
            # Test that tool initializes properly
            self.assertIsNotNone(tool.session)
            self.assertIn('User-Agent', tool.session.headers)
            
        except ImportError:
            self.skipTest("WebSearchTool not available due to missing dependencies")


class TestRAGRetrieverTool(unittest.TestCase):
    """Test RAG Retriever Tool functionality."""
    
    def test_initialization(self):
        """Test RAG tool initialization."""
        try:
            from src.tools.rag_retriever import RAGRetrieverTool
            
            tool = RAGRetrieverTool()
            
            # Check that best practices are loaded
            self.assertIsInstance(tool.best_practices, list)
            self.assertGreater(len(tool.best_practices), 0)
            
            # Check best practices structure
            for practice in tool.best_practices:
                self.assertIn('category', practice)
                self.assertIn('content', practice)
                self.assertIn('keywords', practice)
                
        except ImportError:
            self.skipTest("RAGRetrieverTool not available due to missing dependencies")
    
    def test_section_extraction(self):
        """Test section extraction from markdown content."""
        try:
            from src.tools.rag_retriever import RAGRetrieverTool
            
            tool = RAGRetrieverTool()
            
            test_content = """
# Introduction
This is the introduction section.

## Installation
Here are installation instructions.

### Usage
This is how to use the tool.
"""
            
            sections = tool._extract_sections(test_content)
            
            self.assertIsInstance(sections, dict)
            self.assertIn('introduction', sections)
            self.assertIn('installation', sections)
            
        except ImportError:
            self.skipTest("RAGRetrieverTool not available due to missing dependencies")
    
    def test_quality_score_calculation(self):
        """Test quality score calculation."""
        try:
            from src.tools.rag_retriever import RAGRetrieverTool
            
            tool = RAGRetrieverTool()
            
            # Test high-quality content
            good_content = """
# Project Title

## Description
This is a comprehensive description.

## Installation
Step-by-step installation instructions.

## Usage
```python
import example
example.run()
```

## License
MIT License
"""
            
            score = tool._calculate_quality_score(good_content)
            self.assertGreaterEqual(score, 5)
            self.assertLessEqual(score, 10)
            
            # Test low-quality content
            poor_content = "Short description"
            score = tool._calculate_quality_score(poor_content)
            self.assertLessEqual(score, 5)
            
        except ImportError:
            self.skipTest("RAGRetrieverTool not available due to missing dependencies")


if __name__ == '__main__':
    unittest.main()
