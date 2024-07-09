# # First Party Imports
# import re

# # Third Party Imports
# import pytesseract
# from PyPDF2 import PdfReader
# from pdf2image import convert_from_path
# from concurrent.futures import ThreadPoolExecutor


# pytesseract.pytesseract.tesseract_cmd = "/Users/sharjeelmustafa/opt/anaconda3/envs/re_search/bin/tesseract"
# DOI_REGEX = re.compile(r"(10.\d{4,9}\/[-._;()\/:A-Z0-9]+|\/^10.1002\/[^\s]+$\/i)", re.IGNORECASE | re.MULTILINE)
# CLEAN_REGEX = re.compile(r"(20\d\d|[.a-z])+$", re.IGNORECASE | re.MULTILINE)

# # *********************
# # DOI FUNCTIONS
# # *********************
# def get_dois(files: str):
#     with ThreadPoolExecutor() as executor:
#         results = executor.map(extract_doi, files)
#         return results

# def extract_doi(file: str) -> str | None:
#     """Extract a DOI from a PDF file using text extraction and OCR."""
#     doi = text_extract(file)
#     return ocr_extract(file) if doi is None else doi

# def get_doi(text: str) -> str:
#     """Extract a DOI using a regex."""
#     doi = re.search(DOI_REGEX, text)
#     if doi is None: return None
#     doi = re.sub(CLEAN_REGEX, '', doi.group(0))
#     return doi

# def text_extract(file: str) -> str | None:
#     """Extract text from the first page of a PDF and search for a DOI."""
#     try:
#         reader = PdfReader(file)
#         text = reader.pages[0].extract_text()
#         return get_doi(text)
#     except Exception: return None

# def ocr_extract(file: str) -> str | None:
#     """Extract text from the first page of a PDF using OCR and search for a DOI."""
#     try:
#         image = convert_from_path(file, first_page=1, last_page=1)[0]
#         text = pytesseract.image_to_string(image)
#         return get_doi(text)
#     except Exception: return None


# # *********************
# # TEST FUNCTIONS
# # *********************
# @time_execution
# def test(path: str):
#     pdfs = search_pdfs(path)
#     doi = get_dois(pdfs)
#     if doi is None: return
#     for d in doi: print(d)
        

# # def single_test(path: str):
# #     doi = get_dois(path)
# #     if doi is not None: print(doi)

# if __name__ == '__main__':
#     path = "/Users/sharjeelmustafa/Documents/02_Work/01_Research/SEM_4_Kyle/Articles/00 - TEAMS/0 - 0 Team (Multilevel) Foundation _ Reviews"
    
    
#     test(path)
#     # single_test("/Users/sharjeelmustafa/Documents/02_Work/01_Research/SEM_4_Kyle/Articles/00 - TEAMS/0 - 0 Team (Multilevel) Foundation _ Reviews/Gonzalez-Roma _ Hernandez (2017)_AnnRevOB - Multilevel Modeling- Research-Based Lessons for Substantive Researchers.pdf")

from habanero import Crossref

cr = Crossref()

w = cr.works(ids="10.1146/annurev.psych.56.091103.070250")

w = w['message'].get("title")
print(w)