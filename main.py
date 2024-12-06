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
    frankenstein_gutenberg_text = requests.get('https://www.gutenberg.org/cache/epub/42324/pg42324.txt')
    index = 0
    count = random.randint(0, frankenstein_gutenberg_text.text.count('.') - 1)
    sentence = ''
    while count >= 0:
        sentence, index = get_sentence(frankenstein_gutenberg_text.text, index)
        count -= 1
    print(sentence)
