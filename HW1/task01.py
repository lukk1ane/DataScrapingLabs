def process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            num_lines = len(lines)
            num_words = sum(len(line.split()) for line in lines)
            num_chars = sum(len(line) for line in lines)

        data = {
            "lines": num_lines,
            "words": num_words,
            "characters": num_chars
        }

        save_data(data)
        
        return data

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
        return None

def save_data(data, output_file="file_stats.txt"):
    with open(output_file, "w", encoding="utf-8") as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")

filename = "data.txt"
result = process_file(filename)

if result:
    print("File Statistics:")
    print(result)
