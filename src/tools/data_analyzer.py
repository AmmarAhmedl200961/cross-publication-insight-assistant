# This file will contain the data analysis tool.
from collections import Counter
from typing import List, Dict


def analyze_keywords(keywords: List[str]) -> Dict[str, int]:
    """
    Analyzes the frequency of keywords.

    Args:
        keywords: A list of keywords.

    Returns:
        A dictionary with the frequency of each keyword.
    """
    return Counter(keywords)
