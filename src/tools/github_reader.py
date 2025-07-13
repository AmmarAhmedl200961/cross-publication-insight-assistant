"""
GitHub Repository Reader Tool
Custom tool for fetching and parsing GitHub repository content
"""

from crewai.tools import BaseTool
from github import Github
import requests
import base64
import os
from typing import Dict, List, Any, Optional, Type
import logging
from pydantic import BaseModel, Field
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class GitHubReaderInput(BaseModel):
    """Input schema for GitHub Repository Reader Tool."""
    repo_url: str = Field(..., description="GitHub repository URL to analyze")


class GitHubReaderTool(BaseTool):
    """
    Custom tool for reading and analyzing GitHub repository content.
    Fetches README files, repository structure, and code files.
    """
    
    name: str = "GitHub Repository Reader"
    description: str = """
    Fetches and analyzes GitHub repository content including:
    - Repository metadata (description, topics, languages)
    - README files and documentation
    - Directory structure and file organization
    - Main code files and their content
    - Repository statistics and metrics
    
    Input should be a GitHub repository URL.
    """
    args_schema: Type[BaseModel] = GitHubReaderInput
    
    def _run(self, repo_url: str) -> str:
        """
        Execute the GitHub repository analysis.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Detailed analysis of the repository content
        """
        try:
            # Initialize GitHub client
            github_token = os.getenv("GITHUB_TOKEN")
            github_client = Github(github_token) if github_token else Github()
            
            # Parse repository URL
            repo_info = self._parse_repo_url(repo_url)
            if not repo_info:
                return "Error: Invalid GitHub repository URL"
            
            owner, repo_name = repo_info
            
            # Get repository object
            repo = github_client.get_repo(f"{owner}/{repo_name}")
            
            # Analyze repository
            analysis = {
                "repository_metadata": self._get_repo_metadata(repo),
                "readme_content": self._get_readme_content(repo),
                "directory_structure": self._get_directory_structure(repo),
                "code_analysis": self._analyze_code_files(repo),
                "repository_statistics": self._get_repo_statistics(repo)
            }
            
            return self._format_analysis_result(analysis)
            
        except Exception as e:
            logger.error(f"Error analyzing repository {repo_url}: {str(e)}")
            return f"Error analyzing repository: {str(e)}"
    
    def _parse_repo_url(self, url: str) -> Optional[tuple]:
        """Parse GitHub repository URL to extract owner and repo name."""
        try:
            # Handle various GitHub URL formats
            if "github.com" in url:
                parts = url.replace("https://", "").replace("http://", "").split("/")
                if len(parts) >= 3:
                    owner = parts[1]
                    repo_name = parts[2].replace(".git", "")
                    return (owner, repo_name)
            return None
        except Exception:
            return None
    
    def _get_repo_metadata(self, repo) -> Dict[str, Any]:
        """Extract repository metadata."""
        try:
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "language": repo.language,
                "languages": dict(repo.get_languages()),
                "topics": repo.get_topics(),
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "watchers": repo.watchers_count,
                "open_issues": repo.open_issues_count,
                "license": repo.license.name if repo.license else None,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat(),
                "size": repo.size,
                "default_branch": repo.default_branch,
                "archived": repo.archived,
                "fork": repo.fork,
                "has_wiki": repo.has_wiki,
                "has_pages": repo.has_pages,
                "has_issues": repo.has_issues,
                "has_projects": repo.has_projects
            }
        except Exception as e:
            logger.error(f"Error getting repo metadata: {str(e)}")
            return {}
    
    def _get_readme_content(self, repo) -> str:
        """Extract README file content."""
        try:
            readme_files = ["README.md", "README.rst", "README.txt", "README"]
            
            for readme_name in readme_files:
                try:
                    readme = repo.get_contents(readme_name)
                    if readme.type == "file":
                        content = base64.b64decode(readme.content).decode('utf-8')
                        return content
                except:
                    continue
            
            return "No README file found"
            
        except Exception as e:
            logger.error(f"Error getting README content: {str(e)}")
            return "Error reading README file"
    
    def _get_directory_structure(self, repo) -> Dict[str, Any]:
        """Analyze repository directory structure."""
        try:
            structure = {"files": [], "directories": []}
            
            def traverse_contents(contents, path=""):
                for content in contents:
                    if content.type == "dir":
                        structure["directories"].append({
                            "name": content.name,
                            "path": content.path,
                            "size": content.size
                        })
                        # Recursively traverse subdirectories (limit depth)
                        if path.count("/") < 2:  # Limit recursion depth
                            try:
                                subcontents = repo.get_contents(content.path)
                                traverse_contents(subcontents, content.path)
                            except:
                                pass
                    else:
                        structure["files"].append({
                            "name": content.name,
                            "path": content.path,
                            "size": content.size,
                            "extension": os.path.splitext(content.name)[1]
                        })
            
            # Get root contents
            contents = repo.get_contents("")
            traverse_contents(contents)
            
            return structure
            
        except Exception as e:
            logger.error(f"Error getting directory structure: {str(e)}")
            return {"files": [], "directories": []}
    
    def _analyze_code_files(self, repo) -> Dict[str, Any]:
        """Analyze key code files in the repository."""
        try:
            important_files = [
                "requirements.txt", "package.json", "setup.py", "Dockerfile",
                "docker-compose.yml", ".gitignore", "main.py", "app.py",
                "index.js", "index.html", "config.py", "settings.py"
            ]
            
            code_analysis = {"config_files": {}, "main_files": {}}
            
            for filename in important_files:
                try:
                    file_content = repo.get_contents(filename)
                    if file_content.type == "file" and file_content.size < 10000:  # Limit file size
                        content = base64.b64decode(file_content.content).decode('utf-8')
                        
                        if filename in ["requirements.txt", "package.json", "setup.py"]:
                            code_analysis["config_files"][filename] = content
                        else:
                            code_analysis["main_files"][filename] = content[:1000]  # Truncate large files
                            
                except:
                    continue
            
            return code_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing code files: {str(e)}")
            return {"config_files": {}, "main_files": {}}
    
    def _get_repo_statistics(self, repo) -> Dict[str, Any]:
        """Get repository statistics and metrics."""
        try:
            return {
                "commit_count": repo.get_commits().totalCount,
                "contributor_count": repo.get_contributors().totalCount,
                "branch_count": repo.get_branches().totalCount,
                "release_count": repo.get_releases().totalCount,
                "tag_count": repo.get_tags().totalCount
            }
        except Exception as e:
            logger.error(f"Error getting repo statistics: {str(e)}")
            return {}
    
    def _format_analysis_result(self, analysis: Dict[str, Any]) -> str:
        """Format the analysis result into a readable string."""
        result = []
        
        # Repository Metadata
        metadata = analysis.get("repository_metadata", {})
        if metadata:
            result.append("=== REPOSITORY METADATA ===")
            result.append(f"Name: {metadata.get('name', 'N/A')}")
            result.append(f"Description: {metadata.get('description', 'No description')}")
            result.append(f"Primary Language: {metadata.get('language', 'N/A')}")
            result.append(f"Languages Used: {', '.join(metadata.get('languages', {}).keys())}")
            result.append(f"Topics: {', '.join(metadata.get('topics', []))}")
            result.append(f"Stars: {metadata.get('stars', 0)}")
            result.append(f"Forks: {metadata.get('forks', 0)}")
            result.append(f"License: {metadata.get('license', 'No license')}")
            result.append("")
        
        # README Content
        readme = analysis.get("readme_content", "")
        if readme and readme != "No README file found":
            result.append("=== README CONTENT ===")
            result.append(readme[:2000])  # Limit README content
            if len(readme) > 2000:
                result.append("... (README truncated)")
            result.append("")
        
        # Directory Structure
        structure = analysis.get("directory_structure", {})
        if structure.get("files") or structure.get("directories"):
            result.append("=== REPOSITORY STRUCTURE ===")
            result.append(f"Total Files: {len(structure.get('files', []))}")
            result.append(f"Total Directories: {len(structure.get('directories', []))}")
            
            # List main directories
            main_dirs = [d['name'] for d in structure.get('directories', [])[:10]]
            if main_dirs:
                result.append(f"Main Directories: {', '.join(main_dirs)}")
            
            # List important files
            important_files = [f['name'] for f in structure.get('files', []) 
                             if f['name'].lower() in ['readme.md', 'license', 'requirements.txt', 
                                                    'package.json', 'dockerfile', 'setup.py']]
            if important_files:
                result.append(f"Important Files: {', '.join(important_files)}")
            result.append("")
        
        # Code Analysis
        code_analysis = analysis.get("code_analysis", {})
        if code_analysis.get("config_files") or code_analysis.get("main_files"):
            result.append("=== CODE ANALYSIS ===")
            
            config_files = code_analysis.get("config_files", {})
            if config_files:
                result.append("Configuration Files Found:")
                for filename in config_files.keys():
                    result.append(f"  - {filename}")
            
            main_files = code_analysis.get("main_files", {})
            if main_files:
                result.append("Main Code Files Found:")
                for filename in main_files.keys():
                    result.append(f"  - {filename}")
            result.append("")
        
        # Statistics
        stats = analysis.get("repository_statistics", {})
        if stats:
            result.append("=== REPOSITORY STATISTICS ===")
            for key, value in stats.items():
                result.append(f"{key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(result)
