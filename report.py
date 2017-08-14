from submission import Submission
import textract

class Report(Submission):
    def __init__(self, submission):
        super().__init__(submission)
        self._text = ""
        self._extract_text()

    def _extract_text(self):
        text = ""
        report_extension = self.get_type()
        if report_extension == "pdf":
            try:
                text = textract.process(self._submission).decode()
            except UnicodeDecodeError:
                text = ""
        elif report_extension == "docx":
            text = ""
            # raise NotImplementedError("Docx has not be implemented yet")
        else:
            raise TypeError("Invalid Report File Type")
        
        self._text = self._format_text(text)

    # This is required because parsing of the text can
    # produce odd results. By lowercasing everything and
    # removing spaces you have a higher chances of parsing
    # the information you were looking for
    def _format_text(self, text):
        return text.replace(" ","").lower()

    def contains_string(self, string):
        return self._text.find(string) != -1
