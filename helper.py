import re
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# --- Setup (run once) ---
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
# --- End Setup ---

def get_wordnet_pos(word):
    """Map NLTK POS tag to WordNet POS tag."""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def normalize_query(q: str) -> str:
    """
    Creates a canonical, exact cache key from a query.
    - Lowercases
    - Removes punctuation
    - Normalizes whitespace
    - Lemmatizes verbs/nouns (e.g., "doing" -> "do", "names" -> "name")
    """
    q = q.lower().strip()
    q = re.sub(r"[^\w\s]", "", q)# Replace punctuation with a space
    q = " ".join(q.split())          # Normalize all internal whitespace
    
    words = nltk.word_tokenize(q)
    
    # Lemmatize with POS tagging to reduce verbs
    normalized_words = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in words]
    
    return " ".join(normalized_words)

if __name__== "__main__":
    # --- Example ---
    query1 = "what is your namesdf   "
    query2 = "what is your name?"

    key1 = normalize_query(query1)
    key2 = normalize_query(query2)

    print(f"query1: {query1} ")
    print(f"Key 1: {key1}")
    print(f"query1: {query2} ")

    print(f"Key 2: {key2}")
    print(f"Keys are identical: {key1 == key2}")