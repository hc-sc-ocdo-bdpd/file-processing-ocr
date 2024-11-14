class OCRError(Exception):
    """Base exception for OCR-related issues in the file-processing-ocr library."""

class OCRProcessingError(OCRError):
    """
    Exception raised when an issue occurs during OCR processing.

    This could be due to file format issues, processing errors, or issues
    with the Tesseract OCR engine.
    """

class NotOCRApplicableError(OCRError):
    """
    Exception raised when OCR is attempted on a file type that does not support it.

    This error is useful for indicating that the file type does not contain
    visual elements suitable for OCR.
    """

class TesseractNotFound(OCRError):
    """
    Exception raised when Tesseract OCR is not found on the system.

    This may indicate that Tesseract is either not installed or is not added to the PATH.
    Users are advised to install Tesseract or configure its PATH.
    """
