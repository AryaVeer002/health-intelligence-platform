from pathlib import Path


class ReportExtractor:
    def extract_text(self, file_path: Path) -> str:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Report file not found: {file_path}"
            )

        extension = file_path.suffix.lower()

        if extension == ".txt":
            return file_path.read_text(
                encoding="utf-8-sig"
            )

        raise ValueError(
            f"Text extraction is not supported for {extension} yet"
        )


report_extractor = ReportExtractor()