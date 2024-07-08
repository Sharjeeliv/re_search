import os
import re
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from ..params import PARAMS

pytesseract.pytesseract.tesseract_cmd = PARAMS['tesseract_path']
regex = PARAMS["regex"]
clean = re.compile(r"(20\d\d|[.a-z])+$", re.IGNORECASE | re.MULTILINE)


def text_extract(pdf_name):
    _, file_name = os.path.split(pdf_name)
    # print(f"\033[1;36mTXT \033[1;34m{file_name}\033[0;0m")  # For logging print name
    # with open(pdf_name, "rb") as file:
    try:
        reader = PdfReader(pdf_name, strict=False)
        first_page = reader.pages[0]
        text = first_page.extract_text()
    except Exception:
        text = ""
    return get_doi(str(text))


def clean_doi(doi):
    # print(re.search(clean, doi))
    return re.sub(clean, '', doi)


def get_doi(text):
    matches = re.search(regex, text, re.IGNORECASE | re.MULTILINE)
    if matches is None:
        # print(f"\033[1;31mNo regex match, text dump:\033[0;0m\n")
        return None
    doi = clean_doi(matches.group(0))
    # print(f"\033[1;32mRegex matches, DOI found:\033[0;0m {doi}\n")
    return doi


def ocr_extract(pdf_name):
    pdf_file = convert_from_path(pdf_name, first_page=0, last_page=1)
    # print(f"\033[1;35mOCR \033[1;34m{file_name}\033[0;0m")  # For logging print name

    page_data = pdf_file[0]
    text = pytesseract.image_to_string(page_data)
    text = re.sub("\n-", "", text)
    doi = get_doi(text)
    return doi