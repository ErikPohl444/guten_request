import requests
import random


def get_sentence(contents, marker):
    new_sentence = ''
    while contents[marker] != '.':
        new_sentence += contents[marker]
        marker += 1
    new_sentence += contents[marker]
    marker += 1
    return new_sentence, marker


if __name__ == '__main__':
    books = requests.get('https://www.gutenberg.org/cache/epub/42324/pg42324.txt')
    index = 0
    count = random.randint(0, 3286)
    sentence = ''
    while count >= 0:
        print(count)
        sentence, index = get_sentence(books.text, index)
        count -= 1
    print(sentence)
