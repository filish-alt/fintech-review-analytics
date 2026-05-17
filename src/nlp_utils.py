import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure NLTK resources are downloaded (usually done manually, but safe to include)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """
    Cleans text by removing punctuation, converting to lowercase, 
    and stripping extra whitespace.
    """
    if not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers (optional, but good for themes)
    text = re.sub(r'\d+', '', text)
    
    # Strip extra whitespace
    text = " ".join(text.split())
    
    return text

def tokenize_and_lemmatize(text):
    """
    Tokenizes, removes stop words, and lemmatizes text.
    """
    tokens = nltk.word_tokenize(text)
    
    # Remove stop words and short words
    filtered_tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    
    # Lemmatize
    lemmatized = [lemmatizer.lemmatize(t) for t in filtered_tokens]
    
    return " ".join(lemmatized)

def preprocess_pipeline(text):
    """
    Complete NLP preprocessing pipeline.
    """
    cleaned = clean_text(text)
    return tokenize_and_lemmatize(cleaned)
