# First Party Imports
import time
import concurrent.futures

# Third Party Imports
from pyzotero import zotero

# Local Imports
from .src.utils import get_pdfs, time_execution
from .src.extract import get_dois
from .src.verify import get_crossref_work
from .src.upload import create_zotero_entry
from .params import PARAMS


def filter_none(pdf_data):
    # Remove all none values from the list
    return pdf_data[0] is not None

def api(files: list, lib_key: str, lib_id: str):
    

    PARAMS['zotero_api_key'], PARAMS['zotero_lib_id'] = lib_key, lib_id
    print(PARAMS['zotero_api_key'], PARAMS['zotero_lib_id'])

    zot = zotero.Zotero(PARAMS['zotero_lib_id'], 'user', PARAMS['zotero_api_key'])
    start = time.time()
    pdfs_data = filter(lambda result: filter_none(result), get_dois(files))
    pdfs_metadata = [get_crossref_work(pdf_data) for pdf_data in pdfs_data]  # Iterator object
    [create_zotero_entry(pdf_metadata) for pdf_metadata in pdfs_metadata]
    end = time.time()
    print(f"Time to complete: {round(end - start, 2)}s")
    return 0


@time_execution
def app(path: str):
    start = time.time()
    pdfs = get_pdfs(path)
    print(f"get_pdfs: {round(time.time() - start, 2)}")

    start = time.time()
    pdfs_data = filter(lambda result: filter_none(result), get_dois(pdfs))
    print(f"get_dois: {round(time.time() - start, 2)}")

    start = time.time()
    pdfs_metadata = [get_crossref_work(pdf_data) for pdf_data in pdfs_data]
    print(f"get_crossref_work: {round(time.time() - start, 2)}")

    start = time.time()
    [create_zotero_entry(pdf_metadata) for pdf_metadata in pdfs_metadata]
    print(f"format & upload: {round(time.time() - start, 2)}")


if __name__ == '__main__':
    test_path = "/Users/sharjeelmustafa/Documents/02_Work/01_Research/SEM_4_Kyle/Articles/00 - TEAMS/0 - 0 Team (Multilevel) Foundation _ Reviews"
    app(test_path)