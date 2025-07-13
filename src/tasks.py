"""
Task definitions for the Publication Assistant crew
"""

from crewai import Task
from typing import List


class PublicationAssistantTasks:
    """
    Task definitions for the Publication Assistant multi-agent system.
    Each task corresponds to a specific agent's responsibilities.
    """
    
    @staticmethod
    def repository_analysis_task(agent, tools: List, repo_url: str, description: str = "") -> Task:
        """
        Task for analyzing the GitHub repository structure and content.
        
        Args:
            agent: The Repository Analyzer agent
            tools: List of tools available to the agent
            repo_url: GitHub repository URL to analyze
            description: Optional project description
            
        Returns:
            Task object for repository analysis
        """
        return Task(
            description=f"""
            Conduct a comprehensive analysis of the GitHub repository at {repo_url}.
            {f"Project description provided: {description}" if description else ""}
            
            Your analysis should include:
            1. Repository metadata and basic information
            2. Code structure and organization
            3. Technology stack and frameworks used
            4. README content and documentation quality
            5. Project type and complexity assessment
            6. File structure and important configuration files
            
            Use the GitHub Repository Reader tool to fetch all necessary information.
            Provide a detailed technical analysis that other agents can use to make recommendations.
            """,
            agent=agent,
            tools=tools,
            expected_output="""
            A comprehensive repository analysis report containing:
            - Repository metadata (name, description, stars, language, etc.)
            - Technology stack and frameworks identified
            - Code structure and organization assessment
            - Documentation quality evaluation
            - Project complexity and type classification
            - Key files and configurations found
            """
        )
    
    @staticmethod
    def metadata_recommendation_task(agent, tools: List, repo_analysis: str) -> Task:
        """
        Task for recommending metadata, tags, and keywords.
        
        Args:
            agent: The Metadata Recommender agent
            tools: List of tools available to the agent
            repo_analysis: Output from repository analysis task
            
        Returns:
            Task object for metadata recommendations
        """
        return Task(
            description=f"""
            Based on the repository analysis provided, recommend optimal metadata to improve
            the project's discoverability and categorization.
            
            Repository Analysis Context:
            {repo_analysis}
            
            Your recommendations should include:
            1. Relevant tags and topics for GitHub
            2. Category suggestions for project classification
            3. Keywords for better search visibility
            4. Target audience identification
            5. Competitive positioning insights
            
            Use the Web Search tool to research similar projects and trending keywords.
            Use the Keyword Extractor tool to identify technical terms and relevant keywords.
            """,
            agent=agent,
            tools=tools,
            expected_output="""
            A comprehensive metadata recommendation report containing:
            - Suggested GitHub topics and tags (prioritized list)
            - Project category recommendations
            - Target audience identification
            - Competitive analysis insights
            - SEO-optimized keywords and phrases
            - Trending topics relevant to the project
            """
        )
    
    @staticmethod
    def content_improvement_task(agent, tools: List, repo_analysis: str, metadata_recommendations: str) -> Task:
        """
        Task for improving project content and documentation.
        
        Args:
            agent: The Content Improver agent
            tools: List of tools available to the agent
            repo_analysis: Output from repository analysis task
            metadata_recommendations: Output from metadata recommendation task
            
        Returns:
            Task object for content improvements
        """
        return Task(
            description=f"""
            Enhance the project's presentation by improving titles, descriptions, and documentation
            based on the repository analysis and metadata recommendations.
            
            Repository Analysis Context:
            {repo_analysis}
            
            Metadata Recommendations Context:
            {metadata_recommendations}
            
            Your improvements should include:
            1. Enhanced project title suggestions
            2. Improved project description versions
            3. README content enhancement recommendations
            4. Documentation structure improvements
            5. Engagement and clarity optimizations
            
            Use the RAG Retriever tool to analyze current documentation against best practices.
            Focus on making the project more appealing and accessible to the target audience.
            """,
            agent=agent,
            tools=tools,
            expected_output="""
            A content improvement report containing:
            - Multiple enhanced project title options
            - Improved project descriptions (short and long versions)
            - README enhancement suggestions
            - Documentation structure recommendations
            - Clarity and engagement improvements
            - Professional presentation guidelines
            """
        )
    
    @staticmethod
    def review_and_critique_task(agent, tools: List, repo_analysis: str, content_improvements: str) -> Task:
        """
        Task for reviewing and critiquing the project documentation.
        
        Args:
            agent: The Reviewer/Critic agent
            tools: List of tools available to the agent
            repo_analysis: Output from repository analysis task
            content_improvements: Output from content improvement task
            
        Returns:
            Task object for review and critique
        """
        return Task(
            description=f"""
            Review the project documentation and proposed improvements to identify
            missing sections, unclear information, and areas needing attention.
            
            Repository Analysis Context:
            {repo_analysis}
            
            Content Improvements Context:
            {content_improvements}
            
            Your review should identify:
            1. Missing documentation sections
            2. Unclear or confusing parts
            3. Incomplete information areas
            4. User experience issues
            5. Professional presentation gaps
            6. Accessibility and inclusivity concerns
            
            Use the RAG Retriever tool to compare against documentation best practices.
            Provide constructive criticism and specific improvement suggestions.
            """,
            agent=agent,
            tools=tools,
            expected_output="""
            A comprehensive review report containing:
            - Missing documentation sections identified
            - Unclear or confusing areas highlighted
            - Incomplete information gaps noted
            - User experience improvement suggestions
            - Professional presentation recommendations
            - Prioritized list of issues to address
            """
        )
    
    @staticmethod
    def fact_checking_task(agent, tools: List, all_recommendations: str, repo_analysis: str) -> Task:
        """
        Task for fact-checking all recommendations against repository content.
        
        Args:
            agent: The Fact-Checker agent
            tools: List of tools available to the agent
            all_recommendations: Combined output from all previous tasks
            repo_analysis: Original repository analysis for verification
            
        Returns:
            Task object for fact-checking
        """
        return Task(
            description=f"""
            Verify the accuracy of all suggestions and recommendations against the actual
            repository content to ensure factual correctness and relevance.
            
            All Recommendations to Verify:
            {all_recommendations}
            
            Original Repository Analysis:
            {repo_analysis}
            
            Your verification should include:
            1. Accuracy of technical claims and capabilities
            2. Correctness of framework and technology identification
            3. Relevance of suggested tags and categories
            4. Appropriateness of improvement suggestions
            5. Consistency across all recommendations
            6. Identification of any contradictions or errors
            
            Use the GitHub Repository Reader tool to cross-reference claims with actual code.
            Flag any inaccurate or misleading recommendations for correction.
            """,
            agent=agent,
            tools=tools,
            expected_output="""
            A fact-checking verification report containing:
            - Accuracy assessment of all recommendations
            - Verification status for technical claims
            - Flagged inaccuracies or inconsistencies
            - Corrected information where needed
            - Overall confidence score for recommendations
            - Final validated recommendation set
            """
        )
    
    @staticmethod
    def final_compilation_task(agent, tools: List, fact_check_results: str) -> Task:
        """
        Task for compiling the final comprehensive report.
        
        Args:
            agent: Any agent can handle this compilation task
            tools: List of tools available
            fact_check_results: Output from fact-checking task
            
        Returns:
            Task object for final compilation
        """
        return Task(
            description=f"""
            Compile all verified recommendations into a comprehensive, actionable report
            for improving the project's publication and presentation.
            
            Fact-Checked Results:
            {fact_check_results}
            
            Create a final report that includes:
            1. Executive summary of all recommendations
            2. Prioritized action items
            3. Implementation guidelines
            4. Expected impact of improvements
            5. Next steps and follow-up suggestions
            
            Format the report to be immediately actionable for the project owner.
            """,
            agent=agent,
            tools=tools,
            expected_output="""
            A comprehensive final report containing:
            - Executive summary of key recommendations
            - Prioritized improvement checklist
            - Detailed implementation guidelines
            - Expected outcomes and benefits
            - Clear next steps for project enhancement
            - Professional formatting suitable for publication
            """
        )
