import qrcode
import os
import uuid

def generate_qr_code(data_string, output_dir="static/qrcodes"):
    """
    Generates a QR code for the given data string and saves it as a PNG file.
    Returns the relative path to the saved QR code.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(output_dir, filename)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)
    
    # Return path relative to the app root (e.g. for serving statically)
    return f"/{output_dir}/{filename}"
