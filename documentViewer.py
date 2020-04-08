class DocumentViewer:
    """Содержит инструментарий для работы с текстом"""

    def __init__(self, text_name: str):
        self._text_name = text_name

    def get_lines(self):
        with open(self._text_name, 'r') as file:
            for line in file:
                yield line
