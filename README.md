# file-processing-ocr

The **file-processing-ocr** library is an extension of the [`file-processing`](https://github.com/hc-sc-ocdo-bdpd/file-processing/tree/main) library, designed to add Optical Character Recognition (OCR) functionality to the core file processing capabilities. This library is built as a decorator, allowing it to wrap around relevant file types (e.g., images and PDFs) to extract text content when OCR is required.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **OCR Text Extraction**: Extracts text from images and PDF files, storing the results as part of the file’s metadata.
- **Decorator Pattern**: Designed as a decorator to seamlessly add OCR functionality to the base `File` class in `file-processing`.
- **Lazy Import**: Loaded by `file-processing` only when needed, ensuring lightweight usage when OCR is not required.
- **Error Handling**: Includes custom error handling for missing dependencies and OCR processing issues.

---

## Installation

To install the `file-processing-ocr` library from GitHub, use the following command:

```bash
pip install git+https://github.com/hc-sc-ocdo-bdpd/file-processing-ocr.git
```

Ensure that [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) is installed and correctly configured in your system path, as it’s required for OCR processing.

---

## Quick Start

To begin using `file-processing-ocr` with `file-processing`, initialize a `File` object and apply OCR using the `OCRDecorator` class:

```python
from file_processing import File
from file_processing_ocr.ocr_decorator import OCRDecorator

# Initialize a File object
file = File('path/to/your/image_or_pdf_file.pdf')

# Wrap the file processor with OCR capabilities
ocr_file = OCRDecorator(file)

# Process the file and extract OCR text
ocr_file.process()

# Access the OCR text
print(ocr_file.metadata.get('ocr_text', 'No OCR text extracted'))
```

---

## Architecture

The `file-processing-ocr` library applies the **Decorator Pattern** by wrapping an existing `File` processor to add OCR functionality. It leverages the Tesseract OCR engine to extract text content from images and PDFs and stores this text within the file metadata.

### How It Works

- **Image Files**: Directly applies OCR to image file formats (e.g., .png, .jpg) using `pytesseract`.
- **PDF Files**: Applies OCR to embedded images within PDF pages via `pypdf` and `pytesseract`.
- **Fallback Handling**: If Tesseract is not installed, the decorator raises a custom `TesseractNotFound` error.

---

## Error Handling

- **OCRProcessingError**: Raised if an issue occurs during OCR processing.
- **TesseractNotFound**: Raised if Tesseract OCR is not found in the expected system path.

### Custom Error Example

```python
from file_processing_ocr.errors import TesseractNotFound, OCRProcessingError

try:
    ocr_file.process()
except TesseractNotFound as e:
    print(f"Tesseract OCR not found: {e}")
except OCRProcessingError as e:
    print(f"Error during OCR processing: {e}")
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**: Create your fork on GitHub.
2. **Create a Feature Branch**: Work on your feature in a separate branch.
3. **Write Tests**: Ensure any changes are covered by tests.
4. **Submit a Pull Request**: When ready, submit a PR for review.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For questions or support, please contact:

- **Email**: [ocdo-bdpd@hc-sc.gc.ca](mailto:ocdo-bdpd@hc-sc.gc.ca)

--- 

*Explore our file-processing suite and extend its capabilities with OCR!*