# This file will be the main entry point for our application.

from .agents.publication_analyzer import PublicationAnalyzer
from .agents.trend_aggregator import TrendAggregator
from .agents.insight_generator import InsightGenerator


def main():
    """
    Main function to run the multi-agent system.
    """
    # List of publications to analyze
    publications = [
        {
            "url": "https://app.readytensor.ai/publications/agentconnect-decentralized-collaboration-framework-for-independent-ai-agents-RLFuglEDiwwS",
            "selector": "ul._cx",
        },
        {
            "url": "https://blog.langchain.dev/langgraph-multi-agent-workflows/",
            "selector": "article",  # A reasonable default for blog posts
        },
        # Add more URLs here
    ]

    all_keywords = []
    for pub in publications:
        analyzer = PublicationAnalyzer(pub["url"], pub.get("selector"))
        keywords = analyzer.analyze()
        if keywords:
            all_keywords.append(keywords)

    if not all_keywords:
        print("No keywords were extracted from any of the publications.")
        return

    aggregator = TrendAggregator(all_keywords)
    trends = aggregator.aggregate()

    insight_generator = InsightGenerator(trends)
    insights = insight_generator.generate()

    print("\n--- Insights ---")
    print(insights)


if __name__ == "__main__":
    main()
