import requests
import random


def get_all_books():
    url = 'https://gutendex.com/books'
    current_list = requests.get(url)
    long_list = []
    count = 10  # keep this from running forever or attracting too much scrutiny
    while current_list.status_code == 200 and count > 0:
        long_list.extend(current_list.json()["results"])
        url = current_list.json()["next"]
        current_list = requests.get(url)
        count -= 1
    return long_list


if __name__ == '__main__':
    book_list = get_all_books()
    book = book_list[random.randint(0, len(book_list)-1)]
    sentence_list = requests.get(
        book['formats']['text/plain; charset=us-ascii']
    ).text.split('.')
    print(book['title'], sentence_list[random.randint(0, len(sentence_list)-1)])
