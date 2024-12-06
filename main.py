import requests
import random
import os
import datetime
import pickle
import json


def get_all_books(start_url, cache_file_name, max_count):
    url = start_url
    current_list = requests.get(url)
    all_books = []
    count = max_count  # keep this from running forever or attracting too much scrutiny
    while current_list.ok and count > 0:
        all_books.extend(current_list.json()["results"])
        url = current_list.json()["next"]
        current_list = requests.get(url)
        count -= 1
    with open(cache_file_name, "wb") as file_handle:
        pickle.dump(book_list, file_handle)
    return all_books


def is_stale_cache(cache_file_name):
    try:
        cache_last_written = datetime.datetime.fromtimestamp(os.path.getmtime(cache_file_name))
    except OSError:
        cache_last_written = None
    return (
            not cache_last_written
            or (cache_last_written - datetime.datetime.now()).seconds > books_stale_after_secs
    )


def write_title_and_sentence(book_list):
    written = False
    while not written:
        book = book_list[random.randint(0, len(book_list)-1)]
        try:
            sentence_list = requests.get(
                book['formats'][book_format]
            ).text.split('.')
            print(book['title'],
                  sentence_list[random.randint(0, len(sentence_list)-1)]+'.')
            written = True
        except KeyError:
            written = False


if __name__ == '__main__':
    with open("config.json") as config_handle:
        config = json.load(config_handle)
        cache_file_name = config["cache"]
        book_format = config["book_format"]
        books_url = config["books_url"]
        books_stale_after_secs = int(config["books_stale_after_secs"])
        books_list_max_page_count = int(config["books_list_max_page_count"])

    if is_stale_cache(cache_file_name):
        book_list = get_all_books(books_url, cache_file_name, books_list_max_page_count)
    else:
        with open(cache_file_name, "rb") as fhandle:
            book_list = pickle.load(fhandle)
    if not book_list:
        raise OSError

    write_title_and_sentence(book_list)
