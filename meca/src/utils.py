import os
import shutil

# This section needs to be cleaned up
def search_pdfs(path: str) -> [str]:  # Takes path input and returns a list of names
    folders, pdf_files = [], []
    folders.append(path)

    for folder in folders:
        for file in os.listdir(folder):  # Returns all items in a path
            if file.endswith('.pdf'):
                pdf_files.append("/" + folder + "/" + file)
            elif os.path.isdir(folder + "/" + file):
                folders.append(folder + "/" + file + "/")
                print(f"{file} is a folder")
    return pdf_files


def move_pdf(pdf_path: str):
    try:
        dest = os.getcwd() + "/manual"
        pdf_name = pdf_path.rsplit('/', 1)[1]
        if os.path.exists(dest):  # Move to Manual search folder
            shutil.copy2(pdf_path, dest + '/' + pdf_name)
        else:  # Create Manual search folder
            os.mkdir(dest)
            shutil.copy2(pdf_path, dest + '/' + pdf_name)
    except FileNotFoundError:
        print("File to move was not found")


if __name__ == '__main__':
    search_pdfs('/Users/sharjeelmustafa/Documents/03 Projects/Development/zotero_tool/pdfs')