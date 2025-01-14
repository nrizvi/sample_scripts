"""
PLEASE NOTE: THIS CODE HAS LOW ACCURACY WITH RECOGNIZING WESTERN MISSPELLINGS OF EASTERN NAMES
"""
import nltk
from nltk.metrics.distance import edit_distance
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

# Download necessary NLTK resources if not already available
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def calculate_edit_distance(s1, s2):
    """Calculate the normalized edit distance between two strings."""
    return edit_distance(s1, s2) / max(len(s1), len(s2))


def replace_misspelled_names(input_string, names):
    sentences = sent_tokenize(input_string)
    replaced_sentences = []

    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged_tokens = pos_tag(tokens)
        for i, (word, tag) in enumerate(tagged_tokens):
            # Look for potential name positions based on tags and patterns
            if tag in ['NNP', 'NN'] or (tag in ['DT', 'PRP$', 'VBZ'] and i < len(tagged_tokens) - 1):
                for name in names:
                    # Check both the current token and the next one together for multi-word names
                    potential_name = word
                    if i + 1 < len(tokens):
                        potential_name += " " + tokens[i + 1]

                    # Calculate edit distance to each name
                    if calculate_edit_distance(potential_name.lower(), name.lower()) < 0.5:
                        # Replace the token(s) with the correct name
                        tokens[i] = name
                        if " " in name:
                            # Prevent duplication of last name if the name was split
                            tokens[i + 1] = ""
                        break

        replaced_sentences.append(' '.join(tokens).replace("  ", " "))

    return ' '.join(replaced_sentences)


# Input string and names list
input_string = "hi everyone my name is number rizvi and I'm doing this test my husband's name is Caroline Rini and I also really love the name Roxana and yeah I'm just testing different Brown names though Timothy isn't one of them"
names = ["Naba Rizvi", "Beyonkay Canoles", "Khalil Mrini", "Jimothy WhatsHisFace", "Roxanna"]

# Perform replacement
output_string = replace_misspelled_names(input_string, names)
print(output_string)
