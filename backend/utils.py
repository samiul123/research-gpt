from io import BytesIO
from pathlib import Path
from llama_index.readers.file import PDFReader, PyMuPDFReader
from pathlib import Path
from typing import BinaryIO, Dict, List, Optional, Union

from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
import re


class PyMuPDFReader_v2(BaseReader):
    """Read PDF files using PyMuPDF library."""

    def load_data(
        self,
        file_path: Union[Path, str] = None,
        stream: BytesIO = None,
        metadata: bool = True,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
        """Loads list of documents from PDF file and also accepts extra information in dict format."""
        return self.load(file_path, stream=stream, metadata=metadata, extra_info=extra_info)

    def load(
        self,
        file_path: Union[Path, str] = None,
        stream: BytesIO = None,
        metadata: bool = True,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
        """Loads list of documents from PDF file and also accepts extra information in dict format.

        Args:
            file_path (Union[Path, str]): file path of PDF file (accepts string or Path).
            metadata (bool, optional): if metadata to be included or not. Defaults to True.
            extra_info (Optional[Dict], optional): extra information related to each document in dict format. Defaults to None.

        Raises:
            TypeError: if extra_info is not a dictionary.
            TypeError: if file_path is not a string or Path.

        Returns:
            List[Document]: list of documents.
        """
        import pymupdf
        import fitz

        if not file_path and not stream:
            raise ValueError("Either file_path or stream must be provided.")
        # check if file_path is a string or Path
        if file_path and not isinstance(file_path, str) and not isinstance(file_path, Path):
            raise TypeError("file_path must be a string or Path.")

        # open PDF file
        doc = pymupdf.open(file_path) if file_path else fitz.open(stream=stream)

        # if extra_info is not None, check if it is a dictionary
        if extra_info:
            if not isinstance(extra_info, dict):
                raise TypeError("extra_info must be a dictionary.")

        # if metadata is True, add metadata to each document
        if metadata:
            if not extra_info:
                extra_info = {}
            extra_info["total_pages"] = len(doc)
            extra_info["file_path"] = str(file_path)
            filtered_metadata = {k: v for k, v in doc.metadata.items() if v is not None and v != ""}
            
            extra_info = dict(extra_info, **filtered_metadata)
            
            # return list of documents
            return [
                Document(
                    text=self.clean_up_text(page.get_text()),
                    extra_info=dict(
                        extra_info,
                        **{
                            "page": f"{page.number+1}",
                        },
                    ),
                )
                for page in doc
            ]

        else:
            return [
                Document(
                    text=self.clean_up_text(page.get_text()), extra_info=extra_info or {}
                )
                for page in doc
            ]
    
    def clean_up_text(self, content: str) -> str:
        """
        Remove unwanted characters and patterns in text input.

        :param content: Text input.
        
        :return: Cleaned version of original text input.
        """

        # Fix hyphenated words broken by newline
        content = re.sub(r'(\w+)-\n(\w+)', r'\1\2', content)

        # Remove specific unwanted patterns and characters
        unwanted_patterns = [
            "\\n", "  —", "——————————", "—————————", "—————",
            r'\\u[\dA-Fa-f]{4}', r'\uf075', r'\uf0b7'
        ]
        for pattern in unwanted_patterns:
            content = re.sub(pattern, "", content)

        # Fix improperly spaced hyphenated words and normalize whitespace
        content = re.sub(r'(\w)\s*-\s*(\w)', r'\1-\2', content)
        content = re.sub(r'\s+', ' ', content)

        return content

