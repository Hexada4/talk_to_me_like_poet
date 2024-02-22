import os
import pandas as pd
from collector import DataCollector
from cleaner import Cleaner
import argparse
from config import LINKS
import re

"""
This file is used to extract poems from all links given in .env
"""


def filter_text(df: pd.DataFrame, path: str): # function which will determine whether there aren't \n in every line and delete where there aren't
    indexes = []
    for i, value in enumerate(df.text.values):
        if len(re.findall('\n', value)) == 0:
            indexes.append(i)

    if len(indexes) == 0:
        return False

    df = df.drop(index=indexes)
    os.remove(path)
    df.to_csv(path, index=False, encoding='utf-8')
    return True


def merge_into_csv():
    path_to_poems = f'{os.getcwd()}/data/poems/'
    poems = []

    for poem in os.listdir(path_to_poems):
        df = pd.read_csv(f'data/poems/{poem}')
        if filter_text(df, path=f'data/poems/{poem}'):
            poems.append(pd.read_csv(f'data/poems/{poem}')) # it looks like we update file, idk how to do it in other way
        else:
            poems.append(df)

        os.remove(f'data/poems/{poem}')

    df = pd.concat(poems)

    # df = df.drop(['Unnamed: 0'], axis = 1)
    df.to_csv(f'{os.getcwd()}/data/all_poems.csv', index=False, encoding='utf-8')
    return "Poems are merged into one file in data/poems/"


def parse(args):
    cwd = os.getcwd()
    dvc_repo_path = f'{cwd}/data/poems'

    if args.one_file:
        links = [args.one_file[0]]

    elif args.links:
        links = args.links

    if os.path.exists(f'{cwd}/data/poems'):
        return # just leave out

    os.mkdir(f'{cwd}/data/poems')

    collector = DataCollector()
    cleaner = Cleaner()

    for link in links:
        name = link.split('/')[-2] # example of link: https://slova.org.ru/adamovich/
        path = collector.fit(url=link, name=name)
        path_to_csv = cleaner.fit(path=path, name=name)

        if os.path.exists(path_to_csv) and len(pd.read_csv(path_to_csv)) > 0:
            print(f"{name} poems is created and saved")


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--one_file', nargs=1, help="If you'd like to get poems from your own link")
    parser.add_argument('--links', nargs='+', default=LINKS, help='Links which will be parsed. You can put yours')

    args = parser.parse_args()

    parse(args)
    merge_into_csv()


if __name__ == '__main__':
    cli()