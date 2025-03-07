import os

def process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            num_lines = len(lines)
            num_words = sum(len(line.split()) for line in lines)
            num_chars = sum(len(line) for line in lines)
            result = f"lines: {num_lines}, words: {num_words}, characters: {num_chars}"

            with open("/Users/ninobendianishvili/Documents/py_ttf_1/DataScrapingLabs/week1/results.txt", "w") as output:
                output.write(str(result))
            return result

    except FileNotFoundError:
        print(f"Error: '{filename}' is missing.")
        return None

file = process_file("/Users/ninobendianishvili/Documents/py_ttf_1/DataScrapingLabs/week1/data.txt")

if file:
    print("File processed successfully:", file)
