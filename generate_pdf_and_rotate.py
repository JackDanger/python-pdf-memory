import os
import io
import random
import sys
import psutil
import time
from PIL import Image, ImageDraw
from PyPDF2 import PdfWriter, PdfReader
from pypdf import PdfReader as PyPdfReader, PdfWriter as PyPdfWriter
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile

# Function to create a random noise image
def create_noise_image(width, height):
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    for x in range(width):
        for y in range(height):
            draw.point((x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    return image

# Measure current memory usage
def print_memory_usage():
    process = psutil.Process(os.getpid())
    rss = process.memory_info().rss
    print(f"Memory usage: {rss / (1024 * 1024):.2f} MB")

# Measure elapsed time
def measure_time(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    elapsed = time.time() - start_time
    print(f"Time taken: {elapsed:.2f} seconds")
    return elapsed

# Create a 500-page PDF with random noise images
def generate_pdf(filename, page_count):
    print(f"Generating a {page_count}-page PDF")
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    for _ in range(page_count):
        img = create_noise_image(612, 792)

        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img_file:
            img.save(temp_img_file, format='PNG')
            temp_img_file_name = temp_img_file.name

        # Draw the image from the temporary file path
        c.drawImage(temp_img_file_name, 0, 0, width=612, height=792)
        c.showPage()
        os.remove(temp_img_file_name)

        print('.', end='', flush=True)
    print('')

    print_memory_usage()

    c.save()

    # Save PDF to file
    with open(filename, 'wb') as f:
        print_memory_usage()
        f.write(pdf_buffer.getvalue())

# Rotate PDF using PyPDF2
def rotate_pdf_pypdf2(input_file, output_file):
    print("Rotating PDF using PyPDF2")
    reader = PdfReader(input_file)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(90)
        writer.add_page(page)
    with open(output_file, 'wb') as f:
        writer.write(f)

# Rotate PDF using pypdf
def rotate_pdf_pypdf(input_file, output_file):
    print("Rotating PDF using pypdf")
    reader = PyPdfReader(input_file)
    writer = PyPdfWriter()
    for page in reader.pages:
        page.rotate(90)
        writer.add_page(page)
    with open(output_file, 'wb') as f:
        writer.write(f)

# Rotate PDF using PyMuPDF (fitz)
def rotate_pdf_pymupdf(input_file, output_file):
    print("Rotating PDF using PyMuPDF")
    doc = fitz.open(input_file)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        page.set_rotation(90)  # Rotate the page 90 degrees
    doc.save(output_file)
    doc.close()

def main():
    print_memory_usage()

    # Step 1: Generate the PDF
    pdf_filename = 'random_noise.pdf'
    if len(sys.argv) > 1:
        page_count = int(sys.argv[1])
    else:
        page_count = 50

    print("\nGenerating PDF...")
    measure_time(generate_pdf, pdf_filename, page_count)
    print_memory_usage()

    # Step 2: Rotate using PyPDF2
    rotated_pdf_filename_1 = 'rotated_random_noise_pypdf2.pdf'
    print("\nRotating using PyPDF2...")
    measure_time(rotate_pdf_pypdf2, pdf_filename, rotated_pdf_filename_1)
    print_memory_usage()

    # Step 3: Rotate using pypdf
    rotated_pdf_filename_2 = 'rotated_random_noise_pypdf.pdf'
    print("\nRotating using pypdf...")
    measure_time(rotate_pdf_pypdf, pdf_filename, rotated_pdf_filename_2)
    print_memory_usage()

    # Step 4: Rotate using PyMuPDF
    rotated_pdf_filename_3 = 'rotated_random_noise_pymupdf.pdf'
    print("\nRotating using PyMuPDF...")
    measure_time(rotate_pdf_pymupdf, pdf_filename, rotated_pdf_filename_3)
    print_memory_usage()

if __name__ == '__main__':
    main()
