from pyzotero import zotero
from ..src.text_processing import format_title_to_apa
from ..src.params import general

zot = zotero.Zotero(general['zotero_lib_id'], 'user', general['zotero_api_key'])


def create_zotero_entry(pdf_metadata):
    if pdf_metadata is None:
        print('Metadata is None')
        return

    if zot.items(doi=pdf_metadata.get('doi')):
        print("Article already exists, skipping entry")
        return

    item_entry = zot.item_template('journalArticle')
    # Input metadate directly from received dictionary
    item_entry['title'] = format_title_to_apa(pdf_metadata.get('title'))
    item_entry['publicationTitle'] = pdf_metadata.get('publisher')
    item_entry['issue'] = pdf_metadata.get('issue')
    item_entry['volume'] = pdf_metadata.get('volume')
    item_entry['pages'] = pdf_metadata.get('page')
    item_entry['doi'] = pdf_metadata.get('doi')
    item_entry['date'] = pdf_metadata.get('date_time')

    # Unpack authors and input metadata into zotero database
    authors = []
    for author in pdf_metadata.get('authors'):
        author = {'creatorType': 'author', 'firstName': author.get("given"), 'lastName': author.get("family")}
        authors.append(author)

    item_entry['creators'] = authors
    response = zot.create_items([item_entry])  # create the entry in zotero
    file = [pdf_metadata.get('path')]

    # print(response)

    # Upload corresponding file to zotero
    try:
        zot.upload_attachments(
            zot.attachment_simple(file, response.get('successful').get('0').get('key')))
    except TypeError:
        print("Ignoring TypeError: Because the API uses a string for accessing a list")