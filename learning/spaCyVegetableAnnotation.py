import spacy
from spacy import displacy

# Load base spaCy model
nlp = spacy.blank("en")

# The raw text to annotate
text = """I prefer recipes with spinach, potatoes, and carrots. Aloo gobi is my favorite dish."""

# Process the text using spaCy's model
doc = nlp(text)

# Visualize the text in a browser for manual annotation
displacy.serve(doc, style="ent")

# Add manual annotations by editing text (as a JSON file or otherwise)
# Example: Annotated JSON format
TRAINING_DATA = [
    (text, {"entities": [(16, 25, "VEGETABLE"), (27, 35, "VEGETABLE"), (41, 48, "VEGETABLE")]}),
]

# Save this data for later use in spaCy training
print(TRAINING_DATA)