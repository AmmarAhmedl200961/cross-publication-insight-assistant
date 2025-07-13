"""
RAG Retriever Tool
Tool for analyzing and retrieving insights from documentation using RAG
"""

from crewai.tools import BaseTool
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Any, Optional, Type
import logging
import re
import os
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class RAGRetrieverInput(BaseModel):
    """Input schema for RAG Retriever Tool."""
    query: str = Field(..., description="Content to analyze or question to answer about the project")


class RAGRetrieverTool(BaseTool):
    """
    Custom RAG (Retrieval Augmented Generation) tool for analyzing documentation
    and retrieving relevant insights about project structure and best practices.
    """
    
    name: str = "RAG Content Retriever"
    description: str = """
    Analyzes repository documentation using RAG (Retrieval Augmented Generation)
    to extract insights and provide intelligent recommendations.
    
    Useful for:
    - Analyzing documentation patterns
    - Finding missing information sections
    - Comparing against best practices
    - Extracting key project insights
    - Identifying documentation gaps
    
    Input should be documentation content or specific queries about the project.
    """
    args_schema: Type[BaseModel] = RAGRetrieverInput
    
    def _get_model(self):
        """Get or initialize the sentence transformer model."""
        try:
            return SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.error(f"Error initializing RAG model: {str(e)}")
            return None
    
    def _get_best_practices_knowledge(self):
        """Get knowledge base of documentation best practices."""
        return [
            {
                "category": "README Structure",
                "content": "A good README should include project title, description, installation instructions, usage examples, API documentation, contributing guidelines, and license information.",
                "keywords": ["readme", "documentation", "structure", "installation", "usage"]
            },
            {
                "category": "Installation Guide",
                "content": "Installation instructions should be clear, step-by-step, include prerequisites, dependency management, and platform-specific instructions.",
                "keywords": ["installation", "setup", "dependencies", "requirements", "getting started"]
            },
            {
                "category": "Usage Examples",
                "content": "Usage examples should provide clear, executable code snippets that demonstrate main functionality and common use cases.",
                "keywords": ["usage", "examples", "tutorial", "quickstart", "demo"]
            },
            {
                "category": "API Documentation",
                "content": "API documentation should include endpoint descriptions, request/response formats, authentication methods, and error handling.",
                "keywords": ["api", "endpoints", "authentication", "requests", "responses"]
            },
            {
                "category": "Contributing Guidelines",
                "content": "Contributing guidelines should explain how to set up development environment, coding standards, pull request process, and issue reporting.",
                "keywords": ["contributing", "development", "pull request", "issues", "coding standards"]
            },
            {
                "category": "License and Legal",
                "content": "Projects should include clear license information, copyright notices, and any legal requirements or disclaimers.",
                "keywords": ["license", "copyright", "legal", "terms", "disclaimer"]
            },
            {
                "category": "Project Metadata",
                "content": "Projects should have relevant tags, topics, description, and keywords that help with discoverability and categorization.",
                "keywords": ["tags", "topics", "metadata", "keywords", "discoverability"]
            },
            {
                "category": "Testing and Quality",
                "content": "Projects should include information about testing procedures, code quality tools, continuous integration, and build status.",
                "keywords": ["testing", "quality", "ci", "build", "coverage"]
            },
            {
                "category": "Deployment and Production",
                "content": "Deployment documentation should cover production setup, configuration, environment variables, and scalability considerations.",
                "keywords": ["deployment", "production", "configuration", "environment", "scaling"]
            },
            {
                "category": "Architecture and Design",
                "content": "Technical projects should explain system architecture, design decisions, technology stack, and data flow.",
                "keywords": ["architecture", "design", "technology stack", "system", "data flow"]
            }
        ]
    
    def _run(self, query: str) -> str:
        """
        Analyze content or answer queries using RAG.
        
        Args:
            query: Content to analyze or question to answer
            
        Returns:
            RAG-based analysis and recommendations
        """
        try:
            model = self._get_model()
            if not model:
                return "RAG model not properly initialized"
            
            best_practices = self._get_best_practices_knowledge()
            
            # Determine if this is a content analysis or a specific query
            if len(query) > 500:  # Likely content to analyze
                return self._analyze_content(query, model, best_practices)
            else:  # Likely a specific query
                return self._answer_query(query, model, best_practices)
                
        except Exception as e:
            logger.error(f"Error in RAG retrieval: {str(e)}")
            return f"Error in RAG analysis: {str(e)}"
    
    def _analyze_content(self, content: str, model, best_practices: List[Dict]) -> str:
        """Analyze content against best practices."""
        try:
            results = []
            results.append("=== RAG CONTENT ANALYSIS ===\n")
            
            # Split content into sections
            sections = self._extract_sections(content)
            
            # Analyze each section
            section_analysis = self._analyze_sections(sections, model, best_practices)
            if section_analysis:
                results.append(f"=== SECTION ANALYSIS ===\n{section_analysis}\n")
            
            # Find missing elements
            missing_elements = self._find_missing_elements(content, best_practices)
            if missing_elements:
                results.append(f"=== MISSING ELEMENTS ===\n{missing_elements}\n")
            
            # Get improvement suggestions
            improvements = self._suggest_improvements(content, best_practices)
            if improvements:
                results.append(f"=== IMPROVEMENT SUGGESTIONS ===\n{improvements}\n")
            
            # Quality score
            quality_score = self._calculate_quality_score(content, best_practices)
            results.append(f"=== QUALITY ASSESSMENT ===\nOverall Quality Score: {quality_score}/10\n")
            
            return "\n".join(results)
            
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            return f"Error analyzing content: {str(e)}"
    
    def _answer_query(self, query: str, model, best_practices: List[Dict]) -> str:
        """Answer specific queries using RAG retrieval."""
        try:
            # Create embeddings for best practices if not using FAISS
            documents = [bp["content"] for bp in best_practices]
            doc_embeddings = model.encode(documents)
            
            # Encode query
            query_embedding = model.encode([query])
            
            # Calculate similarities
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
            
            # Get top 3 most similar documents
            top_indices = similarities.argsort()[-3:][::-1]
            
            results = []
            results.append(f"=== RAG QUERY RESPONSE ===\nQuery: {query}\n")
            
            # Format results
            for i, idx in enumerate(top_indices):
                score = similarities[idx]
                if score > 0.3:  # Relevance threshold
                    best_practice = best_practices[idx]
                    results.append(
                        f"Relevant Practice {i+1} (Similarity: {score:.2f}):\n"
                        f"Category: {best_practice['category']}\n"
                        f"Guidance: {best_practice['content']}\n"
                    )
            
            if len([r for r in results if "Relevant Practice" in r]) == 0:  # No relevant results found
                results.append("No highly relevant guidance found for this query.")
            
            return "\n".join(results)
            
        except Exception as e:
            logger.error(f"Error answering query: {str(e)}")
            return f"Error processing query: {str(e)}"
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract sections from content based on markdown headers."""
        try:
            sections = {}
            current_section = "introduction"
            current_content = []
            
            lines = content.split('\n')
            
            for line in lines:
                # Check for markdown headers
                if line.strip().startswith('#'):
                    # Save previous section
                    if current_content:
                        sections[current_section] = '\n'.join(current_content).strip()
                    
                    # Start new section
                    current_section = line.strip('#').strip().lower()
                    current_content = []
                else:
                    current_content.append(line)
            
            # Save last section
            if current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            return sections
            
        except Exception as e:
            logger.error(f"Error extracting sections: {str(e)}")
            return {"content": content}
    
    def _analyze_sections(self, sections: Dict[str, str], model, best_practices: List[Dict]) -> str:
        """Analyze individual sections against best practices."""
        try:
            analysis = []
            
            for section_name, section_content in sections.items():
                if len(section_content.strip()) > 10:  # Skip empty sections
                    # Simple keyword matching for section analysis
                    section_lower = section_content.lower()
                    best_match = None
                    best_score = 0
                    
                    for practice in best_practices:
                        # Count keyword matches
                        matches = sum(1 for keyword in practice['keywords'] if keyword in section_lower)
                        score = matches / len(practice['keywords'])
                        
                        if score > best_score:
                            best_score = score
                            best_match = practice
                    
                    if best_match and best_score > 0.2:
                        analysis.append(
                            f"• {section_name.title()}:\n"
                            f"  Matches: {best_match['category']}\n"
                            f"  Quality: {'Good' if best_score > 0.5 else 'Needs Improvement'}\n"
                        )
            
            return "\n".join(analysis) if analysis else "No clear sections identified"
            
        except Exception as e:
            logger.error(f"Error analyzing sections: {str(e)}")
            return "Error analyzing sections"
    
    def _find_missing_elements(self, content: str, best_practices: List[Dict]) -> str:
        """Find missing documentation elements."""
        try:
            content_lower = content.lower()
            missing = []
            
            # Check for common documentation elements
            checks = [
                ("Installation instructions", ["install", "setup", "getting started"]),
                ("Usage examples", ["usage", "example", "quickstart", "tutorial"]),
                ("API documentation", ["api", "endpoint", "method", "function"]),
                ("Contributing guidelines", ["contribut", "develop", "pull request"]),
                ("License information", ["license", "copyright", "legal"]),
                ("Testing information", ["test", "testing", "coverage", "ci"]),
                ("Configuration details", ["config", "environment", "settings"]),
                ("Deployment instructions", ["deploy", "production", "server"])
            ]
            
            for element_name, keywords in checks:
                if not any(keyword in content_lower for keyword in keywords):
                    missing.append(f"• {element_name}")
            
            return "\n".join(missing) if missing else "No major elements appear to be missing"
            
        except Exception as e:
            logger.error(f"Error finding missing elements: {str(e)}")
            return "Error checking for missing elements"
    
    def _suggest_improvements(self, content: str, best_practices: List[Dict]) -> str:
        """Suggest specific improvements based on analysis."""
        try:
            suggestions = []
            content_lower = content.lower()
            
            # Length-based suggestions
            if len(content) < 500:
                suggestions.append("• Consider expanding the documentation with more detailed explanations")
            
            # Structure suggestions
            if content.count('#') < 3:
                suggestions.append("• Add more section headers to improve document structure")
            
            # Code examples
            if '```' not in content and '`' not in content:
                suggestions.append("• Include code examples to demonstrate usage")
            
            # Links and references
            if 'http' not in content_lower and 'www' not in content_lower:
                suggestions.append("• Consider adding relevant links to documentation or resources")
            
            # Images and diagrams
            if '![' not in content and 'image' not in content_lower:
                suggestions.append("• Consider adding diagrams, screenshots, or visual aids")
            
            # Contact information
            if 'contact' not in content_lower and 'email' not in content_lower:
                suggestions.append("• Include contact information or support channels")
            
            return "\n".join(suggestions) if suggestions else "Documentation appears comprehensive"
            
        except Exception as e:
            logger.error(f"Error suggesting improvements: {str(e)}")
            return "Error generating improvement suggestions"
    
    def _calculate_quality_score(self, content: str, best_practices: List[Dict]) -> int:
        """Calculate a quality score from 1-10."""
        try:
            score = 0
            content_lower = content.lower()
            
            # Length factor (0-2 points)
            if len(content) > 1000:
                score += 2
            elif len(content) > 500:
                score += 1
            
            # Structure factor (0-2 points)
            header_count = content.count('#')
            if header_count >= 5:
                score += 2
            elif header_count >= 3:
                score += 1
            
            # Code examples (0-1 point)
            if '```' in content or content.count('`') > 5:
                score += 1
            
            # Essential sections (0-3 points)
            essential_keywords = [
                ["install", "setup"],
                ["usage", "example"],
                ["license", "copyright"]
            ]
            
            for keywords in essential_keywords:
                if any(keyword in content_lower for keyword in keywords):
                    score += 1
            
            # Links and references (0-1 point)
            if 'http' in content_lower or 'www' in content_lower:
                score += 1
            
            # Professional presentation (0-1 point)
            if not any(word in content_lower for word in ['todo', 'fixme', 'hack', 'temporary']):
                score += 1
            
            return min(score, 10)  # Cap at 10
            
        except Exception as e:
            logger.error(f"Error calculating quality score: {str(e)}")
            return 5  # Default score
