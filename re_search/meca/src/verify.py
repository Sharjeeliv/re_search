# Third-party imports
import requests.exceptions
from habanero import Crossref

cr = Crossref()

def get_subtitle(message):
    return ": " + message.get('subtitle')[0] if len(message.get('subtitle')) else ""

def get_crossref_work(pdf_data):
    doi, pdf_path = pdf_data
    pdf_metadata = {}
    try:
        work = cr.works(ids=doi)

        pdf_metadata['title'] = work.get('message').get('title')[0] + get_subtitle(work.get('message'))
        pdf_metadata['publication'] = work.get('message').get('container-title')[0]
        pdf_metadata['issue'] = work.get('message').get('issue')
        pdf_metadata['volume'] = work.get('message').get('volume')
        pdf_metadata['page'] = work.get('message').get('page')
        pdf_metadata['date'] = work.get('message').get('created').get('date-time').split("-", 1)[0]
        pdf_metadata['doi'] = doi
        pdf_metadata['path'] = pdf_path
        
        authors = []
        for person in work.get('message').get('author'):
            author = {"family": person.get("family").title(), "given": person.get("given").title()}
            authors.append(author)
        pdf_metadata['authors'] = authors

        return pdf_metadata

    except requests.exceptions.HTTPError:
        print(f"Error verifying for doi: {doi}")
        return None