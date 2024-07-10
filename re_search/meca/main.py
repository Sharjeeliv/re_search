# First Party Imports
import os
from typing import List, Tuple

# Third Party Imports
from pyzotero import zotero

# Local Imports
from .src.utils import get_pdfs, time_execution
from .src.extract import get_dois
from .src.verify import get_crossref_work
from .src.upload import create_zotero_entry
from .params import PARAMS


# *********************  
# HELPER FUNCTIONS
# *********************
def filter_none(pdf_data: List[str]): 
    """Remove all none values from the list"""
    return pdf_data[0] is not None

# *********************  
# ENTRY FUNCTIONS
# *********************
def api(files: list, lib_key: str, lib_id: str) -> Tuple[List[str], List[Tuple[str, str]]]:
    # Set the zotero api key and library id
    zot = zotero.Zotero(lib_id, 'user', lib_key)
    
    file_data = filter(lambda result: filter_none(result), get_dois(files))
    metadata = [get_crossref_work(data) for data in file_data]
    results = [create_zotero_entry(pdf_metadata, zot) for pdf_metadata in metadata]
    
    if results is None: return None, None
    sucess = [result for result, _ in results]
    fails = list(set(files)-set(sucess))
    return fails, results


@time_execution
def app(path: str) -> Tuple[List[str], List[Tuple[str, str]]]:
    zot = zotero.Zotero(PARAMS['zotero_lib_id'], 'user', PARAMS['zotero_api_key'])
    
    file_paths = get_pdfs(path)
    file_data = filter(lambda result: filter_none(result), get_dois(file_paths))
    metadata = [get_crossref_work(data) for data in file_data]
    results = [create_zotero_entry(pdf_metadata, zot) for pdf_metadata in metadata]
    
    files = [os.path.split(file)[1] for file in file_paths]
    if results[0] is None: return files, []

    sucess = [result for result, _ in results]
    fails = list(set(files)-set(sucess))
    return fails, results


# *********************  
# TEST FUNCTIONS
# *********************
if __name__ == '__main__':
    test_path = "/Users/sharjeelmustafa/Documents/02_Work/01_Research/SEM_4_Kyle/Articles/00 - TEAMS/0 - 0 Team (Multilevel) Foundation _ Reviews"
    f, r = app(test_path)

    for fail in f: print(fail)
    for result, doi in r: print(result, doi)