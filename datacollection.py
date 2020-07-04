import os
import time

from pathlib import Path
from lib import logger
from lib import sitescrapper
from lib import helper

script_filename = "(" + os.path.basename(__file__) + ")"

limit_pages = 3
limit_articles = 10
create_menu_list = True
create_url_list = True
extract_data = True

if __name__ == '__main__':
    Path(os.getcwd()+"\\output\\plots\\").mkdir(parents=True, exist_ok=True)
    Path(os.getcwd()+"\\output\\html\\").mkdir(parents=True, exist_ok=True)
    # Define log file location
    logger.set_custom_log_info('output/collection_error.log')

    logger.info("..............................#######################################..............................")
    logger.info(script_filename + "########### Starting Execution, Logger Set ###########")
    # SSL or HTTPS ISSUE
    # helper.verify_https_issue()

    # create scraping object
    aljazeera_scrap = sitescrapper.Scrapper(sitescrapper.site_url, logger)

    data = helper.read_data_from_file('output/articles.csv')
    aljazeera_scrap.articles = list(filter(None, data))

    data = helper.read_data_from_file('output/articles_data.csv')
    aljazeera_scrap.articles_data = list(filter(None, data))

    data = helper.read_data_from_file('output/menu_url.csv')
    aljazeera_scrap.menu_url_list = list(filter(None, data))

    if helper.check_cache(sitescrapper.raw_html, sitescrapper.scrap_interval):
        aljazeera_scrap.retrieve_webpage()
        aljazeera_scrap.write_webpage_as_html()

    aljazeera_scrap.read_webpage_from_html()
    aljazeera_scrap.convert_data_to_bs4()

    if create_menu_list:
        logger.info(script_filename + "####---------- Starting to scrap menu list data ----------####")
        aljazeera_scrap.parse_soup_to_find_main_pages()

    if create_url_list:
        logger.info(script_filename + "####---------- Starting to scrap url list data ----------####")
        aljazeera_scrap.parse_soup_to_extract_urls()
        count = 1
        total_articles_menu = len(aljazeera_scrap.menu_url_list)
        for link in aljazeera_scrap.menu_url_list:
            total_articles_menu -= 1
            print("Reading Article Menu: " + str(count) + "/" + str(total_articles_menu))
            logger.info(script_filename + "Reading Article Menu: " + str(count) + "/" + str(total_articles_menu))
            logger.info(script_filename + "Verifying article link to be correct..........")
            if helper.validate_link(link):
                count += 1
                index = aljazeera_scrap.menu_url_list.index(link)
                aljazeera_scrap.menu_url_list[index][1] = 1
                aljazeera_scrap.change_url(link[0])
                time.sleep(sitescrapper.request_interval)
                if not aljazeera_scrap.http_exception:
                    aljazeera_scrap.retrieve_webpage()
                    aljazeera_scrap.write_webpage_as_html()

                    aljazeera_scrap.read_webpage_from_html()
                    aljazeera_scrap.convert_data_to_bs4()
                    aljazeera_scrap.parse_soup_to_extract_urls()
            if count > limit_pages:
                break

    if extract_data:
        logger.info(script_filename + "####---------- Starting to scrap article data ----------####")
        count = 1
        total_articles = len(aljazeera_scrap.articles)
        for article in aljazeera_scrap.articles:
            total_articles -= 1
            print("Reading Article : " + str(count) + "/" + str(total_articles))
            logger.info(script_filename + "Reading Article : " + str(count) + "/" + str(total_articles))
            logger.info(script_filename + "Verifying article link to be correct..........")
            if helper.validate_article_url_read(article):
                count += 1
                index = aljazeera_scrap.articles.index(article)
                aljazeera_scrap.articles[index][1] = 1
                aljazeera_scrap.change_url(article[0])
                time.sleep(sitescrapper.request_interval)
                aljazeera_scrap.retrieve_webpage()
                if not aljazeera_scrap.http_exception:
                    aljazeera_scrap.write_webpage_as_html()
                    aljazeera_scrap.read_webpage_from_html()
                    aljazeera_scrap.convert_data_to_bs4()
                    try:
                        aljazeera_scrap.parse_soup_to_extract_data()
                    except Exception as e:
                        print(e)
                        logger.report(e)
                        logger.report("Url", article)
            if count > limit_articles:
                break

    aljazeera_scrap.write_menu_list_to_file()

    helper.write_data_to_file(aljazeera_scrap.articles, "output/articles.csv", "scrapped article urls")

    helper.write_data_to_file(aljazeera_scrap.articles_data, "output/articles_data.csv", "scrapped articles data")

    logger.info(script_filename + "#### Execution Ended, Scrapping Done ####")
    logger.info("..............................#######################################..............................")
