class FileManager:
    """Функции общие для классов, работающих с файлами"""
    @staticmethod
    def count_lines(file_name: str, chunk_size=1 << 13):
        with open(file_name) as file:
            return sum(chunk.count('\n')
                       for chunk in iter(lambda: file.read(chunk_size), ''))