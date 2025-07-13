"""
Main entry point for the Publication Assistant system
"""

import argparse
import json
import logging
import sys
from typing import Optional
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.crew import PublicationAssistantCrew
from src.config import LOGGING_CONFIG


def setup_logging():
    """Set up logging configuration."""
    # Create logs directory if it doesn't exist
    log_file = Path(LOGGING_CONFIG["file_path"])
    log_file.parent.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG["level"]),
        format=LOGGING_CONFIG["format"],
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )


def validate_github_url(url: str) -> bool:
    """
    Validate if the provided URL is a valid GitHub repository URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid GitHub repository URL, False otherwise
    """
    if not url:
        return False
    
    # Check for GitHub domain
    if "github.com" not in url.lower():
        return False
    
    # Basic URL structure check
    url_parts = url.replace("https://", "").replace("http://", "").split("/")
    if len(url_parts) < 3:
        return False
    
    return True


def main():
    """Main function to run the Publication Assistant."""
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Publication Assistant for AI Projects - Multi-Agent Analysis System"
    )
    parser.add_argument(
        "--repo-url",
        required=True,
        help="GitHub repository URL to analyze"
    )
    parser.add_argument(
        "--description",
        default="",
        help="Optional project description for additional context"
    )
    parser.add_argument(
        "--output-file",
        help="Optional output file to save results (JSON format)"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate system setup without running analysis"
    )
    parser.add_argument(
        "--crew-info",
        action="store_true",
        help="Display crew configuration information"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate GitHub URL
    if not validate_github_url(args.repo_url):
        print("❌ Error: Invalid GitHub repository URL")
        print("   Please provide a valid GitHub repository URL (e.g., https://github.com/owner/repo)")
        sys.exit(1)
    
    try:
        # Initialize the crew
        print("🚀 Initializing Publication Assistant Multi-Agent System...")
        crew = PublicationAssistantCrew()
        
        # Validate setup if requested
        if args.validate_only:
            print("🔍 Validating system setup...")
            validation = crew.validate_setup()
            
            print("\\n📋 System Validation Results:")
            for component, status in validation.items():
                status_icon = "✅" if status else "❌"
                print(f"   {status_icon} {component.replace('_', ' ').title()}")
            
            if validation["all_systems_ready"]:
                print("\\n🎉 All systems ready! You can now run repository analysis.")
            else:
                print("\\n⚠️  Some components are not properly configured.")
                print("   Please check your environment variables and dependencies.")
            
            sys.exit(0)
        
        # Display crew info if requested
        if args.crew_info:
            print("🔧 Crew Configuration Information:")
            crew_info = crew.get_crew_info()
            
            print("\\n👥 Agents:")
            for name, info in crew_info["agents"].items():
                print(f"   • {name.replace('_', ' ').title()}")
                print(f"     Role: {info['role']}")
                print(f"     Goal: {info['goal'][:80]}...")
                print()
            
            print("🛠️  Tools:")
            for tool in crew_info["tools"]:
                print(f"   • {tool['name']}")
                print(f"     {tool['description'][:80]}...")
                print()
            
            print(f"🤖 LLM Model: {crew_info['llm_model']}")
            print(f"⚙️  Process: {crew_info['process']}")
            
            sys.exit(0)
        
        # Run the analysis
        print(f"🔍 Analyzing repository: {args.repo_url}")
        if args.description:
            print(f"📝 Project description: {args.description}")
        
        print("\\n⏳ Starting multi-agent analysis...")
        print("   This may take several minutes as agents collaborate...")
        
        # Execute analysis
        results = crew.analyze_repository(
            repo_url=args.repo_url,
            description=args.description
        )
        
        # Check for errors
        if "error" in results:
            print(f"\\n❌ Analysis failed: {results['error']}")
            sys.exit(1)
        
        # Display results
        print("\\n🎉 Analysis completed successfully!")
        print(f"📊 Status: {results['status']}")
        print(f"⏰ Completed at: {results['timestamp']}")
        
        if args.verbose:
            print(f"\\n👥 Agents involved: {', '.join(results['agents_involved'])}")
            print(f"🛠️  Tools used: {', '.join(results['tools_used'])}")
        
        # Display summary
        print("\\n📋 Analysis Summary:")
        print("=" * 50)
        print(results.get('summary', 'No summary available'))
        
        # Display detailed results if verbose
        if args.verbose and 'detailed_results' in results:
            print("\\n📖 Detailed Results:")
            print("=" * 50)
            for task_name, task_result in results['detailed_results'].items():
                print(f"\\n🔸 {task_name.replace('_', ' ').title()}:")
                print("-" * 40)
                print(task_result[:500] + "..." if len(task_result) > 500 else task_result)
        
        # Save to file if requested
        if args.output_file:
            output_path = Path(args.output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\\n💾 Results saved to: {output_path}")
        
        print("\\n✨ Publication Assistant analysis complete!")
        print("   Use the recommendations to enhance your project's presentation.")
        
    except KeyboardInterrupt:
        print("\\n⏹️  Analysis interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\\n💥 Unexpected error occurred: {str(e)}")
        print("   Check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
