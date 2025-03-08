file_path = 'data.txt'


def extract_data(path):
    def extract_helper(content):
        lines = content.split('\n')
        words = [
            word.strip().replace(',', '').replace('.', '')
            for line in lines
            for word in line.split(' ')
        ]
        chars = [
            char
            for word in words
            for char in word
        ]
        return {
            'lines': {
                'content': lines,
                'count': len(lines)
            },
            'words': {
                'content': words,
                'count': len(words)
            },
            'chars': {
                'content': chars,
                'count': len(chars)
            }
        }


    try:
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
            paragraphs = list(map(extract_helper, text.split('\n\n')))

            return paragraphs

    except FileNotFoundError:
        print(f'file:{file_path} could not be found')


score_data, car_data, number_data = extract_data(file_path)
