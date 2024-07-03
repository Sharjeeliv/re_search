# Local Imports
import time
from rq import get_current_job

def sub_task(file):
    # Simulate file processing
    time.sleep(1)  # Simulate some processing time
    return file

def api_task(files):
    job = get_current_job()
    total_files = len(files)
    results = []

    for index, file in enumerate(files):
        result = sub_task(file)
        results.append(result)
        # Update progress
        job.meta['progress'] = (index + 1) / total_files * 100
        job.save_meta()
    
    return results