# This file will contain the keyword extraction tool.
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Download necessary NLTK data (if not already downloaded)
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


def extract_keywords(text: str, num_keywords: int = 10) -> list[str]:
    """
    Extracts the most common keywords from a given text.

    Args:
        text: The text to extract keywords from.
        num_keywords: The number of keywords to return.

    Returns:
        A list of the most common keywords.
    """
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stop words and punctuation
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [
        word for word in tokens if word.isalpha() and word not in stop_words
    ]

    # Get the most common keywords
    word_counts = Counter(filtered_tokens)
    return [word for word, _ in word_counts.most_common(num_keywords)]
