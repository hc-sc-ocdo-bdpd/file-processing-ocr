import sys
import io
from pathlib import Path
import getpass
import pypdf
import pytesseract
from PIL import Image
from file_processing_ocr.errors import OCRProcessingError, TesseractNotFound
import os

# Define the error message once to reduce redundancy
error = "Tesseract could not be found or is not installed. Please install Tesseract or check the path."

# Ensure that Tesseract is correctly located, depending on the operating system.
try:
    pytesseract.get_tesseract_version()
except:
    if sys.platform == 'win32':
        possible_paths = [
            "C:/Program Files/Tesseract-OCR/tesseract.exe",
            "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe",
            Path('C:/Users') / getpass.getuser() / 'AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
        ]
        found = False
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                found = True
                break
        if not found:
            raise TesseractNotFound("Tesseract could not be found or is not installed. Please install Tesseract or check the path.")
            raise TesseractNotFound(error)
    elif sys.platform == 'linux':
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
            raise TesseractNotFound("Tesseract could not be found or is not installed. Please install Tesseract or check the path.")
        linux_path = '/usr/bin/tesseract'
        if os.path.exists(linux_path):
            pytesseract.pytesseract.tesseract_cmd = linux_path
        else:
            raise TesseractNotFound(error)
    elif sys.platform == 'darwin':
        macos_path = '/usr/local/bin/tesseract'
        if os.path.exists(macos_path):
            pytesseract.pytesseract.tesseract_cmd = macos_path
        else:
            raise TesseractNotFound(error)
    else:
        raise TesseractNotFound("Tesseract could not be found or is not installed. Please install Tesseract or check the path.")
        raise TesseractNotFound(error)

    # Attempt to call get_tesseract_version again after setting the path
    try:
        pytesseract.get_tesseract_version()
    except:
        raise TesseractNotFound(error)

class OCRDecorator:
    def __init__(self, processor, ocr_path: str = None) -> None:
        """Initializes the OCRDecorator with a given file processor."""
        if ocr_path:
            pytesseract.pytesseract.tesseract_cmd = ocr_path
        self._processor = processor
    def process(self) -> None:
        """Processes the file using the wrapped processor and then applies OCR."""
        self._processor.process()
        ocr_text = self.extract_text_with_ocr()
        self._processor.metadata['ocr_text'] = ocr_text
    def extract_text_with_ocr(self) -> str:
        """Extracts text from the file using OCR."""
        extension = self._processor.extension
        if extension == ".pdf":
            return self._ocr_pdf()
        else:
            return self._ocr_image()