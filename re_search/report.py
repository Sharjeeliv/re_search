import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import red
from reportlab.lib.units import inch

def generate_pdf(filenames, output_path):
    # Document setup
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    # Custom Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Normal'],
        fontSize=12,
        textColor=red,
        leading=14,
        spaceAfter=4,
        alignment=0,  # Left alignment
        fontName="Helvetica-Bold"
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        leading=14,
        spaceAfter=4,
        alignment=0  # Left alignment
    )
    italic_body_style = ParagraphStyle(
        'ItalicBody',
        parent=styles['Normal'],
        spaceAfter=12,
        fontName='Helvetica-Oblique'
    )
    
    # Flowables to hold document content
    flowables = [
        Paragraph("File Automation Failure", title_style),
        Paragraph(("Failure can be caused by the article lacking a DOI, "
                   "the DOI could not be extracted, verification failed, "
                   "or the upload failed."), italic_body_style)
    ]
    # Add the filenames with numbering
    for idx, filename in enumerate(filenames, start=1):
        flowables.append(Paragraph(f"{idx}. {filename}", body_style))
        
    # Build the document
    doc.build(flowables)

def task():
    results = [
        "Forsyth (2006)_intro to group dynamics chapter.pdf",
        "Klein _ Kozlowski (2000)_micro-to-meso, multilevel rsch steps.pdf",
        "Klein et al (1994)_AMJ - Levels.pdf",
        "Kozlowski _ Klein (2000)_multilevel intro chapter.pdf",
        "Levine (1999)_Review of Solomon Asch.pdf",
        "Morgeson _ Hofmann (1999)_collective constructs, AMR.pdf",
        "Hofmann (1997)_HLM intro.pdf",
        "Klein et al (1999). Multilevel theory building- Benefits, barriers, and new developments. .pdf",
        "Murphy (1949)_gestalt _ field theory.pdf",
        "Hollenbeck et al (1995)_JAP - Multilevel Theory of Team Decision Making- Decision Performance in Teams Incorporating Distributed Expertise.pdf",
        "Hackman (1992)_group influences on indivs.pdf",
        "Rouseesau (1985) - Issues of level in organizational research- Multi-level and cross-level perspectives.pdf",
        "Hofmann (2002)_multilevel theory, measurement, analysis.pdf",
        "Gonzalez-Roma _ Hernandez (2017)_AnnRevOB - Multilevel Modeling- Research-Based Lessons for Substantive Researchers.pdf",
        "Argyris (1960)_theory and method, understanding OB.pdf",
        "Smith et al (2006)_meso OB.pdf",
        "Marks et al (2001)_JAP - A Temporally Based Framework and Taxonomy of Team Processes.pdf",
        "Chan (1998)_levels, composition models.pdf",
        "Festinger (1954) - A theory of social comparison processes.pdf",
        "Kozlowski _ Ilgen (2006) - Enhancing the Effectiveness of Work Groups and Teams.pdf",
        "Johns. (2006). The essential impact of context on organizational behavior.pdf",
    ]
    
    # Failure report
    out_dir, out_name = 'reports', 'failures.pdf'
    os.makedirs(out_dir, exist_ok=True)
    report_path = os.path.join(out_dir, out_name)
    generate_pdf(results, report_path)

    # Return the path to the failure report
    return out_name

if __name__ == "__main__":
    task()