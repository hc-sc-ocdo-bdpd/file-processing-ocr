import sys
import io
import os
from pathlib import Path
import getpass
import pypdf
import pytesseract
from PIL import Image
from file_processing_ocr.errors import OCRProcessingError, TesseractNotFound

# Define a common error message for missing Tesseract installations.
error_message = "Tesseract could not be found or is not installed. Please install Tesseract or check the path."

# Attempt to locate Tesseract based on the operating system.
try:
    pytesseract.get_tesseract_version()
except:
    if sys.platform == 'win32':
        possible_paths = [
            "C:/Program Files/Tesseract-OCR/tesseract.exe",
            "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe",
            Path('C:/Users') / getpass.getuser() / 'AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
        ]
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
        else:
            raise TesseractNotFound(error_message)
    elif sys.platform == 'linux':
        linux_path = '/usr/bin/tesseract'
        if not os.path.exists(linux_path):
            raise TesseractNotFound(error_message)
        pytesseract.pytesseract.tesseract_cmd = linux_path
    elif sys.platform == 'darwin':
        macos_path = '/usr/local/bin/tesseract'
        if not os.path.exists(macos_path):
            raise TesseractNotFound(error_message)
        pytesseract.pytesseract.tesseract_cmd = macos_path
    else:
        raise TesseractNotFound(error_message)

class OCRDecorator:
    """
    A decorator class that adds OCR capabilities to file processors.
    
    This class is designed to wrap around file processors in the `file-processing`
    suite, adding the ability to extract text content from images and PDFs using OCR.

    Attributes:
        _processor: The underlying file processor to which OCR capabilities are added.
    """

    def __init__(self, processor, ocr_path: str = None) -> None:
        """
        Initializes the OCRDecorator with a given file processor.

        Args:
            processor: The file processor to which OCR functionality will be added.
            ocr_path (str, optional): Optional path to the Tesseract executable.
        """
        if ocr_path:
            pytesseract.pytesseract.tesseract_cmd = ocr_path
        self._processor = processor

    def process(self) -> None:
        """
        Processes the file using the wrapped processor and applies OCR to extract text content.

        This method first processes the file using the original processor, then
        applies OCR if supported, and stores the OCR text in the file's metadata.
        """
        self._processor.process()
        ocr_text = self.extract_text_with_ocr()
        self._processor.metadata['ocr_text'] = ocr_text

    def extract_text_with_ocr(self) -> str:
        """
        Extracts text from the file using OCR, based on file type.

        Returns:
            str: The extracted OCR text.
        """
        extension = self._processor.extension
        if extension == ".pdf":
            return self._ocr_pdf()
        return self._ocr_image()

    def _ocr_image(self) -> str:
        """
        Applies OCR to an image file.

        Returns:
            str: OCR text extracted from the image file.

        Raises:
            OCRProcessingError: If an error occurs during OCR processing.
        """
        try:
            return pytesseract.image_to_string(str(self._processor.file_path))
        except Exception as e:
            raise OCRProcessingError(f"Error during OCR processing: {e}")

    def _ocr_pdf(self) -> str:
        """
        Applies OCR to a PDF file.

        Extracts text from images embedded within PDF pages, if available.

        Returns:
            str: OCR text extracted from images within the PDF.

        Raises:
            OCRProcessingError: If an error occurs during OCR processing.
        """
        ocr_text = ''
        try:
            with open(self._processor.file_path, 'rb') as pdf_file_obj:
                reader = pypdf.PdfReader(pdf_file_obj)
                for page in reader.pages:
                    for image in page.images:  # Restore original image handling
                        ocr_text += pytesseract.image_to_string(
                            Image.open(io.BytesIO(image.data))
                        )
            return ocr_text
        except Exception as e:
            raise OCRProcessingError(f"Error during OCR processing: {e}")

    @property
    def file_name(self) -> str:
        """Returns the file name."""
        return self._processor.file_name

    @property
    def extension(self) -> str:
        """Returns the file extension."""
        return self._processor.extension

    @property
    def owner(self) -> str:
        """Returns the file owner."""
        return self._processor.owner

    @property
    def size(self) -> str:
        """Returns the file size in bytes."""
        return self._processor.size

    @property
    def modification_time(self) -> str:
        """Returns the file modification time."""
        return self._processor.modification_time

    @property
    def access_time(self) -> str:
        """Returns the file access time."""
        return self._processor.access_time

    @property
    def creation_time(self) -> str:
        """Returns the file creation time."""
        return self._processor.creation_time

    @property
    def parent_directory(self) -> str:
        """Returns the file's parent directory path."""
        return self._processor.parent_directory

    @property
    def permissions(self) -> str:
        """Returns the file permissions."""
        return self._processor.permissions

    @property
    def is_file(self) -> bool:
        """Returns True if the path is a file."""
        return self._processor.is_file

    @property
    def is_symlink(self) -> bool:
        """Returns True if the path is a symbolic link."""
        return self._processor.is_symlink

    @property
    def absolute_path(self) -> str:
        """Returns the absolute path of the file."""
        return self._processor.absolute_path

    @property
    def metadata(self) -> dict:
        """Returns the metadata dictionary of the file."""
        return self._processor.metadata
