class FileProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._count()

    def _count(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                num_lines = len(lines)
                num_words = sum(len(line.split()) for line in lines)
                num_chars = sum(len(line) for line in lines)

                data = {
                    "lines": num_lines,
                    "words": num_words,
                    "characters": num_chars
                }

                with open("file_stats.txt", "w", encoding="utf-8") as stats_file:
                    stats_file.write(str(data))

                return data

        except FileNotFoundError:
            print(f"Error: The file '{self.filename}' is missing.")
            return None

# usage
file_processor = FileProcessor("data.txt")
if file_processor.data:
    print(file_processor.data)
