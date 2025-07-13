# This file will contain the TrendAggregator agent.

from typing import List, Dict
from ..tools.data_analyzer import analyze_keywords


class TrendAggregator:
    def __init__(self, all_keywords: List[List[str]]):
        self.all_keywords = all_keywords

    def aggregate(self) -> Dict[str, int]:
        """
        Aggregates keywords from multiple publications to find trends.

        Returns:
            A dictionary with the frequency of each keyword across all publications.
        """
        print("Aggregating keywords...")
        flat_keywords = [
            keyword for sublist in self.all_keywords for keyword in sublist
        ]
        return analyze_keywords(flat_keywords)
