# This file will contain the InsightGenerator agent.

from typing import Dict


class InsightGenerator:
    def __init__(self, keyword_trends: Dict[str, int]):
        self.keyword_trends = keyword_trends

    def generate(self) -> str:
        """
        Generates insights from keyword trends.

        Returns:
            A string containing the generated insights.
        """
        print("Generating insights...")
        if not self.keyword_trends:
            return "No trends found."

        sorted_trends = sorted(
            self.keyword_trends.items(), key=lambda item: item[1], reverse=True
        )

        insights = "Top 5 Keyword Trends:\n"
        for keyword, count in sorted_trends[:5]:
            insights += f"- {keyword}: {count} mentions\n"

        return insights
