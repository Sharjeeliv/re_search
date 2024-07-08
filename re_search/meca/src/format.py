import spacy
import subprocess

def download_spacy_model(model_name: str):
    try: spacy.load(model_name)
    except OSError:
        print(f"Downloading Spacy model: {model_name}")
        subprocess.run(["python", "-m", "spacy", "download", model_name])
    return spacy.load(model_name)

nlp = download_spacy_model("en_core_web_sm")
pos_set = {'NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV', 'PRON'}
special_words = {'who', 'what', 'when', 'why', 'where', 'how'}

def is_major_word(token):
    if token.pos_ in pos_set: return True
    elif len(token) >= 4: return True
    return False

def format_title_to_apa(title: str)->str:
    doc = nlp(title.lower())
    
    title = []
    for token in doc:
        
        # Operate on compound words
        if title and token.pos_ == 'PART': 
            title[-1] = title[-1] + token.text 
            if len(title[-1]) >= 4: title[-1] = title[-1].capitalize()
            continue

        # Stylistically certain words are capitalized
        if token.text in special_words: title.append(token.text.capitalize())
        elif is_major_word(token): title.append(token.text.capitalize())
        elif token.pos_ == 'PUNCT': title[-1] = title[-1] + token.text
        elif title and title[-1][-1] in {':', '.'}: title.append(token.text.capitalize())
        else: title.append(token.text)

    title[0] = title[0].capitalize() 
    formatted_title = ' '.join(title)
    return formatted_title

if __name__ == '__main__':
    test_string = "Perspective: Teams Won’t Solve This Problem"
    print(format_title_to_apa(test_string))