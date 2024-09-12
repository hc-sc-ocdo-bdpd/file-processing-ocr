class OCRError(Exception):
    """Base exception for OCR related issues."""


class OCRProcessingError(OCRError):
    """Raised when there's an issue during OCR processing."""


class NotOCRApplicableError(OCRError):
    """Raised when attempting OCR on a file type that doesn't support it."""


class TesseractNotFound(OCRError):
    """Raised when Tesseract is either not installed or not added to PATH."""
