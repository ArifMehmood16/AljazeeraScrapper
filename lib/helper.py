import os
import pandas as pd

from datetime import datetime
from . import logger

script_filename = "(" + os.path.basename(__file__) + ") "


def read_data_from_file(filename):
    logger.info(script_filename + ".... Reading the file" + filename + " to list ....")
    data = []
    if os.path.exists(filename):
        try:
            reader = pd.read_csv(filename, header=None, )
            data = reader.values.tolist()
        except Exception as e:
            logger.info(script_filename + "File is empty")
            logger.report(e)
            print(e)
    return data


def write_data_to_file(data, filename, log):
    logger.info(script_filename + ".... Writing the " + log + " to file ....")
    try:
        pdwrite = pd.DataFrame(data)
        pdwrite.to_csv(filename, encoding='utf-8', header=False, index=False)
        logger.info(script_filename + ".... Writing the " + log + " to file...Complete ....")
    except Exception as e:
        print(e)
        logger.report(e)


def validate_link(link):
    url = link[0]
    return ("comhttps:" not in url) and ("comhttp:" not in url) and ("#" not in url) and (str(link[1]) == '0')


def validate_article_url_read(article):
    url = article[0]
    return ("comhttps:" not in url) and ("comhttp:" not in url) and ("#" not in url) and (str(article[1]) == '0') and (
            ".html" in url)


def write_webpage_as_html(filename, data=''):
    logger.info(script_filename + "Write html to file.....filename: " + filename)
    try:
        with open(filename, 'wb') as fobj:
            fobj.write(data)
    except Exception as e:
        print(e)
        logger.report(e)
        return False
    else:
        logger.info(script_filename + "Write html to file.....Done.....filename: " + filename)
        return True


def read_webpage_from_html(filename):
    logger.info(script_filename + "Reading html file.....filename: " + filename)
    try:
        with open(filename, encoding="utf8") as fobj:
            data = fobj.read()
    except Exception as e:
        print(e)
        logger.report(e)
        return False
    else:
        logger.info(script_filename + "Reading html file.....Done.....filename: " + filename)
        return data


def get_last_scraped_time(filename):
    logger.info(script_filename + "Getting time for last scrapping")
    if not os.path.exists(filename):
        logger.info(script_filename + "File doesn't exist, First time scrapping")
        return -1  # file doesn't exist

    file_time = os.path.getmtime(filename)
    now = datetime.timestamp(datetime.now())
    diff = now - file_time
    # print(file_time, now, diff)
    minutes = int(round(diff))
    return minutes


def check_cache(filename, cache_time):
    logger.info(script_filename + "Checking cache duration.....")
    # getting last scarping time info
    scraping_time = get_last_scraped_time(filename)

    # check caching duration
    if scraping_time < 0 or scraping_time > cache_time:
        logger.info(script_filename + "Checking cache duration.....Valid")
        return True

    return False
