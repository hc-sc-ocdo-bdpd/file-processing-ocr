import pytest
from file_processing_ocr.ocr_decorator import OCRDecorator

@pytest.fixture
def mock_image_processor():
    """Fixture to set up a mock image processor."""
    class MockProcessor:
        def __init__(self):
            self.file_path = "path/to/image.jpg"
            self.extension = ".jpg"
            self.metadata = {}

        def process(self):
            pass

    return MockProcessor()

@pytest.fixture
def mock_pdf_processor():
    """Fixture to set up a mock PDF processor."""
    class MockProcessor:
        def __init__(self):
            self.file_path = "path/to/document.pdf"
            self.extension = ".pdf"
            self.metadata = {}

        def process(self):
            pass

    return MockProcessor()

@pytest.fixture
def ocr_decorator(mock_image_processor):
    """Fixture to set up OCRDecorator with a mock processor."""
    return OCRDecorator(mock_image_processor)
