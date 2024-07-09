# First Party Imports
import re

# Third Party Imports
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor


pytesseract.pytesseract.tesseract_cmd = "/Users/sharjeelmustafa/opt/anaconda3/envs/re_search/bin/tesseract"
DOI_REGEX = re.compile(r"(10.\d{4,9}\/[-._;()\/:A-Z0-9]+|\/^10.1002\/[^\s]+$\/i)", re.IGNORECASE | re.MULTILINE)
CLEAN_REGEX = re.compile(r"(20\d\d|[.a-z])+$", re.IGNORECASE | re.MULTILINE)

# *********************
# DOI FUNCTIONS
# *********************
def get_dois(files: str):
    with ThreadPoolExecutor() as executor:
        results = executor.map(extract_doi, files)
        return results

def extract_doi(file: str) -> str | None:
    """Extract a DOI from a PDF file using text extraction and OCR."""
    doi = text_extract(file) or ocr_extract(file)
    return doi, file

def get_doi(text: str) -> str:
    """Extract a DOI using a regex."""
    doi = re.search(DOI_REGEX, text)
    if doi is None: return None
    doi = re.sub(CLEAN_REGEX, '', doi.group(0))
    if doi[-1] in ['.', ',', '-']: return None
    return doi

def text_extract(file: str) -> str | None:
    """Extract text from the first page of a PDF and search for a DOI."""
    try:
        reader = PdfReader(file)
        text = reader.pages[0].extract_text()
        return get_doi(text)
    except Exception: return None

def ocr_extract(file: str) -> str | None:
    """Extract text from the first page of a PDF using OCR and search for a DOI."""
    try:
        image = convert_from_path(file, first_page=1, last_page=1)[0]
        text = pytesseract.image_to_string(image)
        return get_doi(text)
    except Exception: return None