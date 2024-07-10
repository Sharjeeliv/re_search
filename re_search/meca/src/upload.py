# First-party imports
from math import e
import os
from typing import Dict

# Local Imports
from .format import format_to_apa


# *********************
# HELPER FUNCTIONS
# *********************
def is_storage(file_path: str) -> bool:
    """Check if the file is in the storage"""
    if not os.path.exists(file_path): return False
    base_path = os.path.split(file_path)[0]
    directory = os.path.split(base_path)[1]
    return directory == 'storage'

def teardown(data):
    path = data.get('path')
    file_name = os.path.split(path)[1]
    if is_storage(path): os.remove(path)
    return file_name, data.get('doi')

# *********************
# ZOTERO FUNCTIONS
# *********************
def create_zotero_entry(pdf_metadata: Dict, zot):
    if pdf_metadata is None: return

    # Check if the article already exists in the database
    title = format_to_apa(pdf_metadata.get('title'))
    if zot.items(q=title): return teardown(pdf_metadata)

    item_entry = zot.item_template('journalArticle')
    # Input metadate directly from received dictionary
    item_entry['title'] = title
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
    except TypeError: pass
    finally: teardown(pdf_metadata)