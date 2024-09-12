from setuptools import setup, find_packages

setup(
    name='file-processing-ocr',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pytesseract',
        'Pillow',
        'pypdf',
    ],
    entry_points={
        'file_processing.plugins': [
            'ocr = file_processing_ocr.ocr_decorator:OCRDecorator',
        ],
    },
)
