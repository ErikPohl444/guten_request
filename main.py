import requests
import random
import os
import datetime
import pickle


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
    mtime_datetime = None
    try:
        mtime = os.path.getmtime('books.pkl')
        mtime_datetime = datetime.datetime.fromtimestamp(mtime)
    except OSError:
        mtime = None

    now = datetime.datetime.now()

    if not mtime or (mtime_datetime - now).seconds > 24*60*60:
        # print("pickle file does not exist or is too stale")
        book_list = get_all_books()
        with open("books.pkl", "wb") as fhandle:
            pickle.dump(book_list, fhandle)
    else:
        # print("shortcut: reading from relevant pickle file")
        with open('books.pkl', "rb") as fhandle:
            book_list = pickle.load(fhandle)
    if not book_list:
        raise OSError
    written = False
    while not written:
        book = book_list[random.randint(0, len(book_list)-1)]
        sentence_list = requests.get(
            book['formats']['text/plain; charset=us-ascii']
        ).text.split('.')
        print(book['title'], sentence_list[random.randint(0, len(sentence_list)-1)])
        written = True
