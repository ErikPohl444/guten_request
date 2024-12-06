import requests
import random
import os
import datetime
import pickle
import json


def get_all_books(start_url):
    url = start_url
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
    with open("config.json") as chandle:
        config = json.load(chandle)
        cache_fname = config["cache"]
        book_format = config["book_format"]
        books_url = config["books_url"]
        books_stale_after_secs = int(config["books_stale_after_secs"])


    mtime_datetime = None
    try:
        mtime = os.path.getmtime(cache_fname)
        mtime_datetime = datetime.datetime.fromtimestamp(mtime)
    except OSError:
        mtime = None

    now = datetime.datetime.now()

    if not mtime or (mtime_datetime - now).seconds > books_stale_after_secs :
        book_list = get_all_books(books_url)
        with open(cache_fname, "wb") as fhandle:
            pickle.dump(book_list, fhandle)
    else:
        with open(cache_fname, "rb") as fhandle:
            book_list = pickle.load(fhandle)
    if not book_list:
        raise OSError
    written = False
    while not written:
        book = book_list[random.randint(0, len(book_list)-1)]
        sentence_list = requests.get(
            book['formats'][book_format]
        ).text.split('.')
        print(book['title'], sentence_list[random.randint(0, len(sentence_list)-1)])
        written = True
