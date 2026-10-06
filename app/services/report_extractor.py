from pathlib import Path


class ReportExtractor:

    SUPPORTED_EXTENSIONS = {".txt"}

    def extract_text(self, file_path: Path) -> str:

        # --------------------------------------------------
        # Validate file
        # --------------------------------------------------

        if not file_path.exists():
            raise FileNotFoundError(
                f"Report file not found: {file_path}"
            )

        if not file_path.is_file():
            raise ValueError(
                f"Report path is not a file: {file_path}"
            )

        extension = file_path.suffix.lower()

        # --------------------------------------------------
        # Validate extension
        # --------------------------------------------------

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Text extraction is not supported for "
                f"{extension or 'files without an extension'} yet"
            )

        # --------------------------------------------------
        # Extract TXT
        # --------------------------------------------------

        if extension == ".txt":

            try:
                text = file_path.read_text(
                    encoding="utf-8-sig"
                )

            except UnicodeDecodeError as exc:
                raise ValueError(
                    "The report could not be decoded as UTF-8 text"
                ) from exc

            except OSError as exc:
                raise ValueError(
                    "The report could not be read"
                ) from exc

            # Remove leading/trailing whitespace
            text = text.strip()

            # Reject empty reports
            if not text:
                raise ValueError(
                    "The report does not contain readable text"
                )

            return text

        # Defensive fallback
        raise ValueError(
            "Unsupported report format"
        )


report_extractor = ReportExtractor()