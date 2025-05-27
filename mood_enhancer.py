from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Ensure the lexicon is downloaded
nltk.download("vader_lexicon")

# Initialize once
analyzer = SentimentIntensityAnalyzer()

def analyze_text_mood(text: str) -> str:
    if not text:
        return "neutral"

    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    if compound >= 0.5:
        return "hype"
    elif compound >= 0.1:
        return "happy"
    elif compound > -0.1:
        return "chill"
    elif compound > -0.5:
        return "sad"
    else:
        return "dark"
