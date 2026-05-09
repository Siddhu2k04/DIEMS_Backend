import os
import uuid
# Note: In a real production environment, you might use ReportLab or a similar library to generate real PDFs.
# For this project, we'll mock the certificate generation by returning a dummy URL.

def generate_certificate(user_name, event_title, date, output_dir="static/certificates"):
    """
    Mocks the generation of a certificate.
    Returns a URL/path to the generated certificate.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filename = f"cert_{uuid.uuid4().hex}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    # Mocking the PDF generation
    with open(filepath, 'w') as f:
        f.write(f"Certificate of Participation\n\nThis is to certify that {user_name} has successfully participated in {event_title} on {date}.")
        
    return f"/{output_dir}/{filename}"
