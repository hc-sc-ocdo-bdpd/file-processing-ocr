import sys
import io
from pathlib import Path
import getpass
import pypdf
import pytesseract
from PIL import Image
from file_processing_ocr.errors import OCRProcessingError, TesseractNotFound

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
            raise TesseractNotFound(error)
    elif sys.platform == 'linux':
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

    def _ocr_image(self) -> str:
        try:
            ocr_result = pytesseract.image_to_string(str(self._processor.file_path))
            return ocr_result
        except Exception as e:
            raise OCRProcessingError(f"Error during OCR processing: {e}")

    def _ocr_pdf(self) -> str:
        ocr_text = ''

        try:
            with open(self._processor.file_path, 'rb') as pdf_file_obj:
                reader = pypdf.PdfReader(pdf_file_obj)
                num_pages = len(reader.pages)

                for i in range(num_pages):
                    page_obj = reader.pages[i]

                    # OCR on embedded images only, no text extraction
                    for image in page_obj.images:
                        ocr_text += pytesseract.image_to_string(
                            Image.open(io.BytesIO(image.data)))

                return ocr_text

        except Exception as e:
            raise OCRProcessingError(f"Error during OCR processing: {e}")

    # Properties to expose metadata for easier access
    @property
    def file_name(self) -> str:
        return self._processor.file_name

    @property
    def extension(self) -> str:
        return self._processor.extension

    @property
    def owner(self) -> str:
        return self._processor.owner

    @property
    def size(self) -> str:
        return self._processor.size

    @property
    def modification_time(self) -> str:
        return self._processor.modification_time

    @property
    def access_time(self) -> str:
        return self._processor.access_time

    @property
    def creation_time(self) -> str:
        return self._processor.creation_time

    @property
    def parent_directory(self) -> str:
        return self._processor.parent_directory

    @property
    def permissions(self) -> str:
        return self._processor.permissions

    @property
    def is_file(self) -> bool:
        return self._processor.is_file

    @property
    def is_symlink(self) -> bool:
        return self._processor.is_symlink

    @property
    def absolute_path(self) -> str:
        return self._processor.absolute_path

    @property
    def metadata(self) -> dict:
        return self._processor.metadata
