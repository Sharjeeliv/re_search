import os
import time

# *********************
# HELPER FUNCTIONS
# *********************
def get_pdfs(path: str) -> list:
    """Return a list of PDF file paths found in the given directory and its subdirectories."""
    pdf_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if not file.endswith('.pdf'): continue
            pdf_files.append(os.path.join(root, file))
    return pdf_files

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        m, s = divmod(execution_time, 60)
        ms = (execution_time - int(execution_time)) * 1000
        print(f"\033[91;1mEXECUTION TIME: {int(m):02}:{int(s):02}.{int(ms):03}\033[0m")
        return result
    return wrapper