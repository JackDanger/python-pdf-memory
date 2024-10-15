import os
import io
import random
import sys
import psutil
from PIL import Image, ImageDraw
from PyPDF2 import PdfWriter, PdfReader
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


# Measure current memory usage, cross-platform
def print_memory_usage():
    process = psutil.Process(os.getpid())
    rss = process.memory_info().rss
    print(f"Memory usage {rss / (1024 * 1024):.2f} MB")  # noqa


# Create a 500-page PDF with random noise images
def generate_pdf(filename, page_count):
    print(f"Generating a {page_count}-page PDF")
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    for _ in range(page_count):
        img = create_noise_image(612, 792)  # PDF letter size in pixels

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
    # Remove the temporary image file after use

    c.save()

    # Save PDF to file
    with open(filename, 'wb') as f:
        print_memory_usage()
        f.write(pdf_buffer.getvalue())


# Rotate all pages 90 degrees to the right
def rotate_pdf(input_file, output_file):
    print("Rotating each page of PDF")
    reader = PdfReader(input_file)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(90)
        writer.add_page(page)
    with open(output_file, 'wb') as f:
        writer.write(f)


def main():
    print_memory_usage()
    # Step 1: Generate the PDF
    pdf_filename = 'random_noise.pdf'

    if len(sys.argv) > 1:
        page_count = int(sys.argv[1])
    else:
        page_count = 50

    generate_pdf(pdf_filename, page_count=page_count)
    print_memory_usage()

    # Step 2: Rotate all pages and save the new PDF
    rotated_pdf_filename = 'rotated_random_noise.pdf'
    rotate_pdf(pdf_filename, rotated_pdf_filename)
    print_memory_usage()


if __name__ == '__main__':
    main()
