import os

from pyzotero import zotero
from .format import format_to_apa
from ..params import PARAMS

# zot = zotero.Zotero(PARAMS['zotero_lib_id'], 'user', PARAMS['zotero_api_key'])

def create_zotero_entry(pdf_metadata, zot):
    if pdf_metadata is None: return
    
    # Check if the article already exists in the database
    if zot.items(q=pdf_metadata.get('title')): return

    item_entry = zot.item_template('journalArticle')
    # Input metadate directly from received dictionary
    item_entry['title'] = format_to_apa(pdf_metadata.get('title'))
    item_entry['publicationTitle'] = pdf_metadata.get('publication')
    item_entry['issue'] = pdf_metadata.get('issue')
    item_entry['volume'] = pdf_metadata.get('volume')
    item_entry['pages'] = pdf_metadata.get('page')
    item_entry['doi'] = pdf_metadata.get('doi')
    item_entry['date'] = pdf_metadata.get('date')
    item_entry['creators'] = [{'creatorType': 'author', 
                               'firstName': author.get("given"), 
                               'lastName': author.get("family")} 
                               for author in pdf_metadata.get('authors', [])]
    
    # Create zotero item entry
    response = zot.create_items([item_entry])
    file = [pdf_metadata.get('path')]

    # Upload corresponding file to zotero
    try:
        key = response.get('successful').get('0').get('key')
        attachment = zot.attachment_simple(file, key)
        zot.upload_attachments(attachment)
        # os.remove(file[0])
    except TypeError:
        # if os.path.exists(file[0]): os.remove(file[0])
        # print("Ignoring TypeError: Because the API uses a string for accessing a list")
        return