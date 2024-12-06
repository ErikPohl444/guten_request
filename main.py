import requests
import random


if __name__ == '__main__':
    frankenstein_gutenberg_text = requests.get('https://www.gutenberg.org/cache/epub/42324/pg42324.txt')
    sentence_list = frankenstein_gutenberg_text.text.split('.')
    print(sentence_list[random.randint(0, len(sentence_list)-1)])
