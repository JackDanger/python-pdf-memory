# How much RSS memory does a PDF use?

```
$ python generate_pdf_and_rotate.py 20
Initial Memory usage: 61.33 MB
Generating 20 random noise images...
Image generation complete.
Time taken: 8.52 seconds
Time taken: 1.13 seconds

Testing create_pdf_with_pypdf2...
Creating PDF using PyPDF2: random_noise_pypdf2.pdf
Time taken: 4.54 seconds
After create_pdf_with_pypdf2 Memory usage: 199.12 MB
Forcing garbage collection...
Tracked objects: 60194

Testing create_pdf_with_pypdf...
Creating PDF using pypdf: random_noise_pypdf.pdf
Time taken: 4.56 seconds
After create_pdf_with_pypdf Memory usage: 269.03 MB
Forcing garbage collection...
Tracked objects: 60320

Testing create_pdf_with_pymupdf...
Creating PDF using PyMuPDF: random_noise_pymupdf.pdf
Time taken: 4.54 seconds
After create_pdf_with_pymupdf Memory usage: 342.38 MB
Forcing garbage collection...
Tracked objects: 60320

Testing create_pdf_with_reportlab...
Creating PDF using ReportLab: random_noise_reportlab.pdf
Time taken: 4.53 seconds
After create_pdf_with_reportlab Memory usage: 415.38 MB
Forcing garbage collection...
Tracked objects: 60320
```
