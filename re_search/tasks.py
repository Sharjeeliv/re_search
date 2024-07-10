# First Party
import os

# Third Party
from rq import get_current_job

# Local
from meca.main import api
from report import generate_report



def api_task(files, lib_key, lib_id):
    
    job = get_current_job()
    total_files = len(files)
    results, fails = [], []
    packet_size = 8

    # Process files in packets
    for i in range(0, total_files, packet_size):

        packet = files[i:i + packet_size]
        f, r =  api(packet, lib_key, lib_id)
        results.extend(r)
        fails.extend(f)
        
        # Update progress
        job.meta['progress'] = (i + 1) / total_files * 100
        job.save_meta()

    # Failure report
    out_dir, out_name = 'reports', 'failures.pdf'
    os.makedirs(out_dir, exist_ok=True)
    report_path = os.path.join(out_dir, out_name)
    generate_report(results, report_path)

    # Return the path to the failure report
    return out_name
