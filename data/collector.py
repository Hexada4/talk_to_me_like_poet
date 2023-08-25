import requests
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
import logging


class DataCollector:
    def __init__(self):
        self.url = "https://slova.org.ru/mandelshtam/"
        self.cwd = os.getcwd() # getting current working directory
        self.logger = logging.getLogger('model.data_collector')
        self.logger.setLevel(logging.INFO)
        # handler for errors
        self.err = logging.FileHandler(f'{self.cwd}/collector_log_errs.log')
        self.err.setLevel(logging.ERROR)
        # handler for info messages
        self.info = logging.FileHandler(f'{self.cwd}/collector_log_info.log')
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

    def collect(self) -> list:
        bs_obj = bs(requests.get(self.url).text, features="html.parser")
        lists_of_objects = bs_obj.find(class_='grid-col-1').find_all('div') # it gets sections by letters and store into list
        if lists_of_objects:
            self.logger.info('List of objects was successfully created')
            
        else:
            self.logger.error('Some trouble occured while trying to extract list of objects')

        new_links = [link.find_all('a') for link in lists_of_objects] # here we got the blocks to extract links
        poems_links = []

        # extracting links
        for link in new_links:
            for sublink in link:
                poems_links.append(sublink.get('href').split('/')[-2])

        poems_links = list(set(poems_links)) # if there are any duplicates, they'll be removed
        self.logger.info('Function collect() is finished')
        return poems_links

    def saving(self, links: list = None, path_to_save: str = 'path') -> None:
        # creating dir and saving file into it
        os.mkdir(f'{self.cwd}/html_poems')

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
                path = f'{self.cwd}/html_poems/{links[i]}.html' # path to file with html page of poem
                with open(path, 'w') as f:
                    f.write(requests.get(f'{self.url}/{links[i]}/').text)

                self.logger.info(f'{links[i]} is installed')
                parsed_poems[links[i]] = parse(path)

                os.remove(path)
                if not os.path.exists(path):
                    self.logger.info(f'{links[i]} is deleted after extracting data')

                else:
                    self.logger.error(f'Some error occured, therefore {links[i]} isn`t deleted')

            parsed_df = pd.DataFrame.from_dict(data = parsed_poems, orient='index').reset_index()
            parsed_df = parsed_df.rename(columns={'index': 'title_of_poem',
                                                  '0': 'text_of_poem'})
            parsed_df.to_csv(path_to_save)
            os.rmdir('/home/jollyreap/talk_to_me_like_poet/data/html_poems')
            if os.path.exists(f'{self.cwd}/poems.csv'):
                self.logger.info('The csv file with all poems is created')

            else:
                self.logger.error('Some trouble occured while saving poems into file')

        except Exception as ex:
            self.logger.error(ex)
            os.rmdir('/home/jollyreap/talk_to_me_like_poet/data/html_poems')
            raise ex

    def main(self, path: str = None) -> None:
        poem_links = self.collect()
        if path:
            self.saving(poem_links, path_to_save=path)

        else:
            self.saving(poem_links, path_to_save=f'{self.cwd}/poems.csv')


# test
if __name__ == '__main__':
    class_ = DataCollector()
    print(DataCollector.main(class_))