import os

PARAMS = {
    'regex': r"(10.\d{4,9}\/[-._;()\/:A-Z0-9]+|\/^10.1002\/[^\s]+$\/i)",
    'path': '',
    'tesseract_path': '/Users/sharjeelmustafa/opt/anaconda3/envs/re_search/bin/tesseract',
    'zotero_lib_id': os.getenv('ZOTERO_LIB_ID'),
    'zotero_api_key': os.getenv('ZOTERO_API_KEY'),
}