"""
Sample usage of the Publication Assistant system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.crew import PublicationAssistantCrew


def main():
    """Demonstrate basic usage of the Publication Assistant."""
    
    # Initialize the crew
    print("🚀 Initializing Publication Assistant...")
    crew = PublicationAssistantCrew()
    
    # Validate setup
    validation = crew.validate_setup()
    print(f"✅ System validation: {validation['all_systems_ready']}")
    
    if not validation['all_systems_ready']:
        print("❌ System not ready. Please check your configuration.")
        return
    
    # Example repository analysis
    repo_url = "https://github.com/microsoft/vscode"
    description = "Visual Studio Code - A popular code editor"
    
    print(f"🔍 Analyzing repository: {repo_url}")
    
    try:
        # Run analysis
        results = crew.analyze_repository(
            repo_url=repo_url,
            description=description
        )
        
        # Display results
        print("\\n📊 Analysis Results:")
        print("=" * 50)
        print(f"Status: {results['status']}")
        print(f"Repository: {results['repository_url']}")
        print(f"Timestamp: {results['timestamp']}")
        
        if 'summary' in results:
            print(f"\\nSummary:\\n{results['summary']}")
        
        if 'detailed_results' in results:
            print("\\n📖 Detailed Results:")
            for task_name, task_result in results['detailed_results'].items():
                print(f"\\n🔸 {task_name.replace('_', ' ').title()}:")
                print("-" * 40)
                # Show first 500 characters of each result
                preview = task_result[:500] + "..." if len(task_result) > 500 else task_result
                print(preview)
        
        print("\\n✨ Analysis complete!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")


if __name__ == "__main__":
    main()
