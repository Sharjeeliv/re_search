import time
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rq import get_current_job

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
    
    # Path where PDFs will be saved
    pdf_directory = 'pdfs'  # Ensure this directory exists or create it
    os.makedirs(pdf_directory, exist_ok=True)
    
    for index, file in enumerate(files):
        result = sub_task(file)
        results.append(result)
        # Update progress
        job.meta['progress'] = (index + 1) / total_files * 100
        job.save_meta()
    
    # Generate PDF with the filenames
    pdf_filename = 'file_names.pdf'
    pdf_path = os.path.join(pdf_directory, pdf_filename)
    generate_pdf(results, pdf_path)
    
    # Return the path or URL of the generated PDF
    return pdf_filename