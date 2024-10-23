import os
import io
import random
import sys
import psutil
import time
from PIL import Image, ImageDraw
from PyPDF2 import PdfWriter, PdfReader
from pypdf import PdfWriter as PyPdfWriter, PdfReader as PyPdfReader
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas  # FIX: Ensure this import is correct!
from reportlab.lib.pagesizes import letter
import tempfile

PDF_PAGE_SIZE = (612, 792)  # Letter size in points

### Utility Functions ###

def print_memory_usage():
    """Prints the current memory usage of the process."""
    process = psutil.Process(os.getpid())
    rss = process.memory_info().rss
    print(f"Memory usage: {rss / (1024 * 1024):.2f} MB")

def measure_time(func, *args, **kwargs):
    """Measures and prints the time taken to execute a function."""
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start_time
    print(f"Time taken: {elapsed:.2f} seconds")
    return result

### Image Generation ###

def generate_noise_images(page_count):
    """Generates a list of random noise images."""
    print(f"Generating {page_count} random noise images...")
    images = []
    for _ in range(page_count):
        img = Image.new('RGB', PDF_PAGE_SIZE)
        draw = ImageDraw.Draw(img)
        for x in range(PDF_PAGE_SIZE[0]):
            for y in range(PDF_PAGE_SIZE[1]):
                draw.point((x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        images.append(img)
    print("Image generation complete.")
    return images

def save_images_as_temp_files(images):
    """Saves images as temporary PNG files and returns their paths."""
    temp_files = []
    for img in images:
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        img.save(temp_file, format='PNG')
        temp_files.append(temp_file.name)
        temp_file.close()
    return temp_files

### PDF Conversion Helper ###

def convert_image_to_pdf(image_path):
    """Converts a PNG image to a single-page PDF."""
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)  # FIX: Ensure correct usage of canvas
    c.drawImage(image_path, 0, 0, width=PDF_PAGE_SIZE[0], height=PDF_PAGE_SIZE[1])
    c.showPage()
    c.save()
    pdf_buffer.seek(0)  # Reset the buffer position
    return pdf_buffer

### PDF Creation Implementations ###

def create_pdf_with_pypdf2(image_files, output_file):
    """Creates a PDF using PyPDF2."""
    print(f"Creating PDF using PyPDF2: {output_file}")
    writer = PdfWriter()
    for image_path in image_files:
        img_pdf_buffer = convert_image_to_pdf(image_path)
        reader = PdfReader(img_pdf_buffer)
        writer.add_page(reader.pages[0])
    with open(output_file, 'wb') as f:
        writer.write(f)

def create_pdf_with_pypdf(image_files, output_file):
    """Creates a PDF using pypdf."""
    print(f"Creating PDF using pypdf: {output_file}")
    writer = PyPdfWriter()
    for image_path in image_files:
        img_pdf_buffer = convert_image_to_pdf(image_path)
        reader = PyPdfReader(img_pdf_buffer)
        writer.add_page(reader.pages[0])
    with open(output_file, 'wb') as f:
        writer.write(f)

def create_pdf_with_pymupdf(image_files, output_file):
    """Creates a PDF using PyMuPDF."""
    print(f"Creating PDF using PyMuPDF: {output_file}")
    doc = fitz.open()  # Create a new empty PDF

    for image_path in image_files:
        # Convert the PNG image to a one-page PDF using ReportLab
        pdf_buffer = convert_image_to_pdf(image_path)
        img_doc = fitz.open(stream=pdf_buffer, filetype="pdf")  # Open the buffer as a PDF

        # Insert the single-page PDF into the main document
        doc.insert_pdf(img_doc)

    doc.save(output_file)
    doc.close()

def create_pdf_with_reportlab(image_files, output_file):
    """Creates a PDF using ReportLab."""
    print(f"Creating PDF using ReportLab: {output_file}")
    c = canvas.Canvas(output_file, pagesize=letter)
    for image_path in image_files:
        c.drawImage(image_path, 0, 0, width=PDF_PAGE_SIZE[0], height=PDF_PAGE_SIZE[1])
        c.showPage()
    c.save()

### Main Execution Flow ###

def main():
    print_memory_usage()

    # Determine the number of pages from the command line, default to 20
    page_count = int(sys.argv[1]) if len(sys.argv) > 1 else 20

    # Step 1: Generate Noise Images
    images = measure_time(generate_noise_images, page_count)

    # Step 2: Save Images as Temporary Files
    image_files = measure_time(save_images_as_temp_files, images)

    # Step 3: Create PDFs using all four libraries
    pdf_filename_pypdf2 = 'pypdf2.pdf'
    pdf_filename_pypdf = 'pypdf.pdf'
    pdf_filename_pymupdf = 'pymupdf.pdf'
    pdf_filename_reportlab = 'reportlab.pdf'

    measure_time(create_pdf_with_pypdf2, image_files, pdf_filename_pypdf2)
    print_memory_usage()

    measure_time(create_pdf_with_pypdf, image_files, pdf_filename_pypdf)
    print_memory_usage()

    measure_time(create_pdf_with_pymupdf, image_files, pdf_filename_pymupdf)
    print_memory_usage()

    measure_time(create_pdf_with_reportlab, image_files, pdf_filename_reportlab)
    print_memory_usage()

    # Cleanup: Remove temporary files
    print("Cleaning up temporary files...")
    for file in image_files:
        os.remove(file)

if __name__ == '__main__':
    main()
