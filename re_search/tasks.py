# First Party
import time
import os

# Third Party
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rq import get_current_job

# Local
from meca import api


def sub_task(file):
    # Simulate file processing
    time.sleep(1)  # Simulate some processing time
    return file

def generate_pdf(filenames, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter  # Keep the dimensions in case needed
    
    c.drawString(72, height - 72, "Processed Files:")
    
    y_position = height - 100
    for filename in filenames:
        c.drawString(72, y_position, filename)
        y_position -= 15
    
    c.save()

def api_task(files):
    job = get_current_job()
    total_files = len(files)
    results = []

    packet_size = 4
    for i in range(0, total_files, packet_size):
        # divide into packets
        packet = files[i:i + packet_size]
        print(packet)
        # pass to api

        # save to results

        job.meta['progress'] = (i + 1) / total_files * 100
        job.save_meta()

    
    # for index, file in enumerate(files):
    #     result = sub_task(file)
    #     results.append(result)
    #     # Update progress
    #     job.meta['progress'] = (index + 1) / total_files * 100
    #     job.save_meta()
    

    # Path where PDFs will be saved
    pdf_directory = 'reports'  # Ensure this directory exists or create it
    os.makedirs(pdf_directory, exist_ok=True)
    # Generate PDF with the filenames
    pdf_filename = 'file_names.pdf'
    pdf_path = os.path.join(pdf_directory, pdf_filename)
    generate_pdf(results, pdf_path)
    
    # Return the path or URL of the generated PDF
    return pdf_filename

if __name__=="__main__":
    api_task(["file1", "file2", "file3", "file4", "file5", "file6", "file7", "file8", "file9", "file10", "file11", "file12", "file13", "file14", "file15", "file16", "file17", "file18", "file19", "file20", "file21", "file22"])