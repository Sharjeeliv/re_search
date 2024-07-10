# Firsty-party imports
import spacy
import subprocess

# Third-party imports
from spellchecker import SpellChecker

# *********************
# SETUP DECLARATIONS
# *********************
disable = ['ner', 'parser', 'lemmatizer', 'morphologizer', 'senter']
def download_spacy_model(model_name: str):
    try: spacy.load(model_name, disable=disable)
    except OSError:
        print(f"Downloading Spacy model: {model_name}")
        subprocess.run(["python", "-m", "spacy", "download", model_name])
    return spacy.load(model_name, disable=disable)

nlp = download_spacy_model("en_core_web_sm")
spell = SpellChecker()

POS_TAGS = {'NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV', 'PRON'}
Q_WORDS = {'who', 'what', 'when', 'why', 'where', 'how'}
NON_PARTICIPLE = {"to"}


# *********************
# FORMAT FUNCTIONS
# *********************
def is_major_word(token, tag):
    # Major words are nouns, proper nouns, verbs, adjectives, adverbs, and pronouns
    # And words that are at least 4 characters long
    return tag in POS_TAGS or len(token) >= 4
    
def format_to_apa(title: str)->str:
    doc = nlp(title.lower())
    tokens = [(token.text, token.pos_) for token in doc]
    words = [text for text, _ in tokens]
    errors = spell.unknown(words)
    
    title = []
    for token, tag in tokens:
        # Join compound words
        if title and tag == 'PART' and token not in NON_PARTICIPLE: 
            title[-1] = title[-1] + token
            if len(title[-1]) >= 4: title[-1] = title[-1].capitalize()
        # Capitalize non-dictionary words
        elif token in errors and tag == "VERB": title.append(token.upper())
        # Stylistically certain words are capitalized
        elif token in Q_WORDS: title.append(token.capitalize())
        elif is_major_word(token, tag): title.append(token.capitalize())
        elif tag == 'PUNCT': title[-1] = title[-1] + token
        elif title and title[-1][-1] in {':', '.'}: title.append(token.capitalize())
        else: title.append(token)

    title[0] = title[0].capitalize() 
    formatted_title = ' '.join(title)
    formatted_title = formatted_title.replace('- ', '-')
    return formatted_title
 

# *********************
# TEST FUNCTIONS
# *********************
def test_format_to_apa(strings: list):
    for string in strings: print(format_to_apa(string))

if __name__ == '__main__':
    test_strings = [
        "A Century of Work Teams in the Journal of Applied Psychology",
        "A Conceptual Review of Emergent State Measurement: Current Problems, Future Solutions",
        "A framework for testing meso-mediational relationships in Organizational Behavior",
        "A Review and Integration of Team Composition Models: Moving Toward a Dynamic and Temporal Framework",
        "BEYOND TEAM TYPES AND TAXONOMIES: A DIMENSIONAL SCALING CONCEPTUALIZATION FOR TEAM DESCRIPTION",
        "From causes to conditions in group research",
        "Leading Teams When the Time is Right: Finding the Best Moments to Act",
        "Learning more by crossing levels: evidence from airplanes, hospitals, and orchestras",
        "Perspective: Teams Won’t Solve This Problem",
        "Team Effectiveness 1997-2007: A Review of Recent Advancements and a Glimpse Into the Future",
        "Team Meeting Attitudes: Conceptualization and Investigation of a New Construct",
        "TEAMS IN ORGANIZATIONS: From Input-Process-Output Models to IMOI Models",
        "The Etiology of the Multilevel Paradigm in Management Research",
        "The Evolution of Work Team Research Since Hawthorne",
        "WHEN AND HOW TEAM LEADERS MATTER"
        ]
    
    test_format_to_apa(test_strings)
