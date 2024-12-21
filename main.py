import requests
import random
import os
import datetime
import pickle
import json


def get_all_books(start_url, cache_file_name, max_count):
    all_books = []
    current_list = requests.get(start_url)
    while current_list.ok:
        for _ in range(max_count, 0, -1):
            all_books.extend(current_list.json()["results"])
            url = current_list.json()["next"]
            current_list = requests.get(url)
    with open(cache_file_name, "wb") as file_handle:
      pickle.dump(book_list, file_handle)
    return all_books


def is_stale_cache(cache_file_name):
    try:
        return (
                datetime.datetime.fromtimestamp(os.path.getmtime(cache_file_name)) -
                datetime.datetime.now()
        ).seconds > books_stale_after_secs
    except OSError:
        return False


def output_title_and_random_sentence(book_list):
    written = False
    while not written:
        book = book_list[random.randint(0, len(book_list)-1)]
        try:
            sentence_list = requests.get(
                book['formats'][book_format]
            ).text.split('.')
            print(f'{book["title"]} {sentence_list[random.randint(0, len(sentence_list)-1)]}.')
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
        with open(cache_file_name, "rb") as cache_handle:
            book_list = pickle.load(cache_handle)
    if not book_list:
        raise OSError

    output_title_and_random_sentence(book_list)
