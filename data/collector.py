import requests
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
import logging
from logging.handlers import RotatingFileHandler

class DataCollector:
    def __init__(self):
        self.cwd = os.getcwd() # getting current working directory
        self.logger = logging.getLogger('model.data_collector')
        self.logger.propagate = False
        self.logger.setLevel(logging.INFO)
        # handler for errors
        self.err = RotatingFileHandler(f'{self.cwd}/logs/collector_log_errs.log', maxBytes=1024*1024, backupCount=5)  # Max file size: 1MB, keep 5 backup files
        self.err.setLevel(logging.ERROR)
        # handler for info messages
        self.info = RotatingFileHandler(f'{self.cwd}/logs/collector_log_info.log', maxBytes=1024*1024, backupCount=5)
        self.info.setLevel(logging.INFO)
        # handler to print messages in console as ordinary print
        self.stream = logging.StreamHandler()
        self.stream.setLevel(logging.INFO)
        # formatter is a class which explains the way to write messages into log files
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_formatter = logging.Formatter('%(asctime)s - %(message)s')
        self.err.setFormatter(formatter)
        self.info.setFormatter(formatter)
        self.stream.setFormatter(stream_formatter)
        # adding in main logger new handlers with params
        self.logger.addHandler(self.stream)
        self.logger.addHandler(self.err)
        self.logger.addHandler(self.info)

    def collect(self, name, url) -> list:
        self.logger.info(f'{name.capitalize()} STARTED')
        bs_obj = bs(requests.get(url).text, features="html.parser")
        lists_of_objects = bs_obj.find(class_='grid-col-1').find_all('div') # it gets sections by letters and store into list
        if not lists_of_objects: # some authors are ranged by letters as Mandelsham, others aren't
            lists_of_objects = bs_obj.find(class_='grid-col-3').find_all('div')

        if lists_of_objects:
            self.logger.info('List of objects was successfully created')

        else:
            self.logger.error(f'Some trouble occured while trying to extract list of objects | {name.capitalize()}')

        new_links = [link.find_all('a') for link in lists_of_objects] # here we got the blocks to extract links
        poems_links = []

        # extracting links
        for link in new_links:
            for sublink in link:
                poems_links.append(sublink.get('href').split('/')[-2])

        poems_links = list(set(poems_links)) # if there are any duplicates, they'll be removed
        self.logger.info('Function collect() is finished')
        return poems_links

    def saving(self, links, name, url) -> None:
        # creating dir and saving file into it
        os.mkdir(f'{self.cwd}/data/html_poems')

        def parse(link: str):
            with open(link, 'r') as f:
                file = f.read()

            bs_obj = bs(file, features="html.parser")
            poem = bs_obj.find(class_='grid-col-3').text.split('\n')[3:-3]

            # joining whole poem into one string
            return ' '.join(poem)

        try: # If something happens, program will inform us, that something happened
            parsed_poems = {}

            for i in range(len(links)):
                path = f'{self.cwd}/data/html_poems/{links[i]}.html' # path to file with html page of poem
                with open(path, 'w') as f:
                    f.write(requests.get(f'{url}/{links[i]}/').text)

                parsed_poems[links[i]] = parse(path)

                os.remove(path)
                if os.path.exists(path):
                    self.logger.error(f'Some error occured, therefore {links[i]} isn`t deleted | {name.capitalize()}')

            path_to_csv = f'{self.cwd}/data/poems/{name}_poems.csv'
            parsed_df = pd.DataFrame.from_dict(data = parsed_poems, orient='index').reset_index()
            parsed_df = parsed_df.rename(columns={'index': 'title_of_poem'})
            parsed_df.to_csv(path_to_csv)
            os.rmdir(f'{self.cwd}/data/html_poems')
            if os.path.exists(path_to_csv):
                self.logger.info('The csv file with all poems is created')

            else:
                self.logger.error(f'Some trouble occured while saving poems into file | {name.capitalize()}')

            return path_to_csv

        except Exception as ex:
            self.logger.error(ex)
            os.rmdir(f'{self.cwd}/data/html_poems')
            raise ex

    def fit(self, url, name) -> None: # to avoid calling logger multiple times, i decided to move all arguments here
        poem_links = self.collect(name, url)
        path = self.saving(poem_links, name, url)

        return path

