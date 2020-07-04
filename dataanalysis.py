import collections
import glob
import os
import pandas as pd
import operator

import numpy as np
import matplotlib.pyplot as plt

from lib import logger
from os import path

data_file_path = 'output/articles_data.csv'
plots_output_path = 'output/plots/'
confidence_level = 0.4
no_of_tags_to_find_condifence = 5

script_filename = "(" + os.path.basename(__file__) + ")"


def delete_all_previous_plots():
    files = glob.glob(os.path.abspath(os.getcwd())+'/output/plots/*')
    for f in files:
        os.remove(f)


def find_confidence_level_tags(input_counted_list, full_tags_list):
    confidence_tag_list = []
    for tags in input_counted_list:
        tag = tags[0]
        frequency = tags[1]
        tag_list = []
        for tag_string in full_tags_list:
            if tag in tag_string:
                tag_list.append(tag_string.split(","))

        counted = collections.Counter([x for sublist in tag_list for x in sublist])
        max_frequency_tags = []
        for item in counted.items():
            max_frequency_tags.append(item)
        sorted_frequency_of_tags = sorted(max_frequency_tags, key=operator.itemgetter(1), reverse=True)

        confidence_tag = []
        for value in sorted_frequency_of_tags:
            if value[0] != tag and (int(value[1]) / int(frequency) >= 0.4):
                value = [value[0], round((int(value[1]) / int(frequency)) * 100)]
                confidence_tag.append(value)
        confidence_tag_list.append([tag, confidence_tag])
    return confidence_tag_list


def split_strings_in_list(input_list):
    output_list = []
    for item in input_list:
        output_list.append(str(item).split(","))
    return output_list


def read_data_from_csv_file():
    logger.info(script_filename + "Reading data from csv file to list")
    data = []
    if path.exists(data_file_path):
        try:
            reader = pd.read_csv(data_file_path, header=None, )
            reader = reader.dropna()
            data = reader.values.tolist()
        except Exception as e:
            logger.info(script_filename + "File is empty")
            logger.report(e)
            print(e)
    return data


def calculate_tag_frequency_and_sort(data_tags_list):
    logger.info(script_filename + "Calculating tags frequency and sorting them")
    counted = collections.Counter([x for sublist in data_tags_list for x in sublist])
    logger.info(script_filename + "Tags frequency calculated")
    frequency_of_tags = []
    for item in counted.items():
        frequency_of_tags.append(item)
    freq_of_tags_sorted = sorted(frequency_of_tags, key=operator.itemgetter(1), reverse=True)
    logger.info(script_filename + "Tags sorted by frequency...Returning")
    return freq_of_tags_sorted


def plot_and_save_max_frequency_tags(tags):
    logger.info(script_filename + "Plotting tags with " + str(no_of_tags_to_find_condifence) + " maximum frequencies")
    tags_to_plot = [i[0] for i in tags]
    y_pos = np.arange(len(tags_to_plot))
    frequency_to_plot = [i[1] for i in tags]
    plt.figure(figsize=(10 + no_of_tags_to_find_condifence, 7))
    plt.bar(y_pos, frequency_to_plot, align='center', alpha=0.5)
    plt.xticks(y_pos, tags_to_plot)
    plt.ylabel('Frequency')
    plt.title('Tags frequency in Al-Jazeera articles')
    logger.info(script_filename + "Saving plot with " + str(no_of_tags_to_find_condifence) + " maximum frequencies")
    plt.savefig(plots_output_path + "max_frequency_tags.png")


def plot_and_save_confidence_tags(tags):
    logger.info(script_filename + "Plotting confidence of tags")
    for item in tags:
        logger.info(script_filename + "Plotting confidence of " + str(item))
        tags_to_plot = [i[0] for i in item[1]]
        y_pos = np.arange(len(tags_to_plot))
        frequency_to_plot = [i[1] for i in item[1]]
        plt.figure(figsize=(5 + len(item[1]), 7))
        plt.bar(y_pos, frequency_to_plot, align='center', alpha=0.5)
        plt.xticks(y_pos, tags_to_plot)
        plt.ylabel('Confidence')
        plt.title('Frequency Confidence with tag "' + item[0] + '"')
        logger.info(script_filename + "Saving confidence plot of " + str(item))
        plt.savefig(plots_output_path + item[0] + ".png")


if __name__ == '__main__':

    delete_all_previous_plots()

    logger.set_custom_log_info('output/analysis_error.log')

    logger.info("..............................#######################################..............................")
    logger.info(script_filename + "########### Starting Execution, Logger Set ###########")

    data = read_data_from_csv_file()

    input_data = [i[3] for i in data]
    data_tags_list = split_strings_in_list(input_data)

    frequency_of_tags_sorted = calculate_tag_frequency_and_sort(data_tags_list)

    top_frequency_tags = frequency_of_tags_sorted[:no_of_tags_to_find_condifence]

    confidence_tag = find_confidence_level_tags(top_frequency_tags, input_data)

    plot_and_save_max_frequency_tags(top_frequency_tags)

    plot_and_save_confidence_tags(confidence_tag)

    logger.info(script_filename + "#### Execution Ended, Scrapping Done ####")
    logger.info("..............................#######################################..............................")
