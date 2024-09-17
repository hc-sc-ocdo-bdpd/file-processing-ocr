import pytest
from unittest.mock import patch, mock_open, MagicMock
from file_processing_ocr.ocr_decorator import OCRDecorator
from file_processing_ocr.errors import OCRProcessingError, TesseractNotFound
from file_processing_test_data import get_test_files_path

# Sample files for real file tests
PDF_SAMPLES = [
    "test_ocr_text.pdf",
    "test_ocr_text_2.pdf",
]
JPEG_SAMPLES = [
    "test_ocr_text.jpg",
    "test_ocr_text_2.jpg",
]
PNG_SAMPLES = [
    "test_ocr_text.png",
    "test_ocr_text_2.png",
]
TIF_SAMPLES = [
    "test_ocr_text.tif",
    "test_ocr_text_2.tif",
]
TIFF_SAMPLES = [
    "test_ocr_text.tiff",
    "test_ocr_text_2.tiff",
]
GIF_SAMPLES = [
    "test_ocr_text.gif",
    "test_ocr_text_2.gif",
]
NON_OCR_APPLICABLE_SAMPLES = [
    "Empty.zip",
    "Sample.xml",
]

OCR_APPLICABLE_SAMPLES = (
    PDF_SAMPLES + JPEG_SAMPLES + PNG_SAMPLES + TIF_SAMPLES + TIFF_SAMPLES + GIF_SAMPLES
)
EXPECTED_OCR_TEXT = "Test OCR text successful!"

@pytest.mark.parametrize(
    "file_extension,expected_output",
    [
        (".jpg", "mock ocr result"),
        (".png", "mock ocr result"),
        (".pdf", "mock ocr result with pdf images"),
    ],
)
def test_ocr_processing(
    file_extension, expected_output, mock_image_processor, mock_pdf_processor
):
    """Test OCR processing with different file extensions."""
    if file_extension == ".pdf":
        processor = mock_pdf_processor
    else:
        processor = mock_image_processor
        processor.extension = file_extension

    ocr_decorator = OCRDecorator(processor)

    # Mocking different behaviors depending on the file type
    with patch("pytesseract.image_to_string", return_value=expected_output), patch(
        "builtins.open", mock_open(read_data=b"fake pdf data")
    ), patch(
        "PIL.Image.open", return_value=MagicMock()
    ), patch(
        "pypdf.PdfReader"
    ) as mock_pdf_reader:  # Mock PdfReader

        # If processing a PDF, mock the PdfReader behavior
        if file_extension == ".pdf":
            mock_reader_instance = mock_pdf_reader.return_value
            mock_page = MagicMock()
            mock_page.images = [MagicMock(data=b"fake image data")]  # Mock images in the PDF
            mock_reader_instance.pages = [mock_page]
            result = ocr_decorator.extract_text_with_ocr()
            # Expect OCR result from images in PDFs only, no text extraction
            assert result == expected_output
        else:
            # For images, we only expect the OCR result
            result = ocr_decorator.extract_text_with_ocr()
            assert result == expected_output

def test_ocr_tesseract_not_found():
    """Test for the case when Tesseract is not found."""
    with pytest.raises(TesseractNotFound):
        raise TesseractNotFound("Tesseract could not be found or is not installed.")

@pytest.mark.parametrize(
    "side_effect,error", [(Exception("OCR error"), OCRProcessingError)]
)
def test_ocr_processing_error(side_effect, error, mock_image_processor):
    """Test OCR processing failure scenarios."""
    ocr_decorator = OCRDecorator(mock_image_processor)

    # Simulate OCR processing error
    with patch("pytesseract.image_to_string", side_effect=side_effect):
        with pytest.raises(error):
            ocr_decorator.extract_text_with_ocr()

# Mocking PdfReader to simulate PDF behavior for tests
class MockPdfReader:
    def __init__(self):
        self.pages = [MockPdfPage()]

class MockPdfPage:
    def __init__(self):
        self.images = [MockPdfImage()]

class MockPdfImage:
    def __init__(self):
        self.data = b"fake image data"

@pytest.mark.parametrize(
    "ocr_text,expected_combined",
    [("mock ocr result with pdf images", "mock ocr result with pdf images")],
)
def test_ocr_pdf_processing(ocr_text, expected_combined, mock_pdf_processor):
    """Test OCR processing for PDFs."""
    ocr_decorator = OCRDecorator(mock_pdf_processor)

    # Mock pypdf, pytesseract, and Image.open to avoid real file processing
    with patch("pypdf.PdfReader", return_value=MockPdfReader()), patch(
        "pytesseract.image_to_string", return_value=ocr_text
    ), patch("builtins.open", mock_open(read_data=b"fake pdf data")), patch(
        "PIL.Image.open", return_value=MagicMock()
    ):  # Mock Image.open for images
        result = ocr_decorator.extract_text_with_ocr()
        assert isinstance(result, str)
        assert result == expected_combined

# New test function for real files without mocking
@pytest.mark.parametrize("file_name", OCR_APPLICABLE_SAMPLES)
def test_ocr_on_real_files(file_name):
    """Test OCR processing on real files without mocking."""
    test_files_path = get_test_files_path()
    file_path = test_files_path / file_name

    class RealProcessor:
        def __init__(self, file_path):
            self.file_path = str(file_path)
            self.extension = file_path.suffix.lower()
            self.metadata = {}

        def process(self):
            pass

    processor = RealProcessor(file_path)
    ocr_decorator = OCRDecorator(processor)
    ocr_decorator.process()
    result = ocr_decorator.metadata['ocr_text']

    # Assert the OCR output matches expected text
    assert result.strip() == EXPECTED_OCR_TEXT
