import requests
import random


if __name__ == '__main__':
    sentence_list = requests.get(
        'https://www.gutenberg.org/cache/epub/42324/pg42324.txt'
    ).text.split('.')
    print(sentence_list[random.randint(0, len(sentence_list)-1)])
