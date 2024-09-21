import logging
import os
from urllib.error import URLError
from urllib.request import urlretrieve


def remove_quotes(text: str):
    if len(text) > 2 and text[0] == '"' and text[-1] == '"':
        res = text[1:-1]
    else:
        res = text
    return res


def download_image(image_url, file_dir):
    try:
        directory = os.path.dirname(file_dir)
        if not os.path.exists(directory):
            os.makedirs(directory)
        urlretrieve(image_url, file_dir)  # TODO: make sure it’s saved
        logging.info(f"Image={image_url} was saved in {file_dir}")
        return True
    except URLError as e:
        logging.error(f"Image={image_url} was not saved in {file_dir}")
        logging.exception(e)
        return False
