import os


def process_file(filename):
    data = {"lines": 0, "words": 0, "characters": 0}

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' is missing.")
        return None

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            data["lines"] = len(lines)
            data["words"] = sum(len(line.split()) for line in lines)
            data["characters"] = sum(len(line) for line in lines)

        print(
            f"Lines: {data['lines']}, Words: {data['words']}, "
            f"Characters: {data['characters']}"
        )
        return data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


extracted_data = process_file("data.txt")

if extracted_data:
    with open("file_stats.txt", "w") as stats_file:
        stats_file.write(str(extracted_data))
