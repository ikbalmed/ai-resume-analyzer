import nltk
from nltk.corpus import stopwords
from collections import Counter
import re

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def extract_keywords(text, num_keywords=10):
    words = re.findall(r'\b\w+\b', text.lower())
    words = [word for word in words if word not in stop_words]
    return [word for word, _ in Counter(words).most_common(num_keywords)]
