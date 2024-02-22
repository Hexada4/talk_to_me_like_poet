import os
import re
import pandas as pd


class Cleaner:

    def load(self, path) -> pd.DataFrame:
        return pd.read_csv(path)



    # just preparation
    def first_cleaning(self, df) -> pd.DataFrame:
        df = df.drop(['Unnamed: 0'], axis=1)
        df = df.rename(columns={'0': 'text_of_poem'})
        return df


    # main cleaning
    def basic_text_preparation(self, text_prep: list) -> list:
        result = []
        for i in text_prep:
            cleaned_text = re.sub(r'[А-ЯЁ]\.', ' ', i)  # removes every letter followed by a dot
            cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # removes punctuation
            cleaned_text = re.sub("[^а-яА-ЯёЁ]+", " ", cleaned_text)  # deletes latin letters
            cleaned_text = re.sub(r'[0-9]', " ", cleaned_text)  # deletes numbers
            cleaned_text = re.sub(r'"([^"]*)"', r'\1', cleaned_text) # removes inverted commas

            result.append(cleaned_text)

        return list(set(result))

    def main_work_with_poem(self, df: pd.DataFrame) -> list:
        prepared_poems = []
        for i in df['text_of_poem']:
            text_prep = re.findall('[А-Я][^А-Я]*', i)
            # to get rid of footsteps in last phrase I`m compelled to delete it,
            # which looks like that: some last phrase. May 1234 page 43
            last_string = text_prep[-1][:text_prep[-1].find('.')]
            text_prep.pop()
            text_prep.append(last_string)

            text_prep = self.basic_text_preparation(text_prep=text_prep)
            text_prep = [a.lower() for a in text_prep]  # converts it to lower case
            text_prep = [a.rstrip() for a in text_prep]  # removes spaces from left and right sides
            text_prep = [a.lstrip() for a in text_prep]

            # now we should remove tiny sentences, because they won't have a good influence on our model
            # and we should remove empty strings if there're
            clean_text = []
            for idx, val in enumerate(text_prep):  # removing empty strings
                if text_prep[idx] in ['', ' ']:
                    pass
                else:
                    clean_text.append(val)

            text_prep = []
            for val in clean_text:  # removing string having less than 10 letters
                if len(val) <= 10:
                    pass
                else:
                    text_prep.append(val)

            text_prep_str = '\n'.join(text_prep)
            prepared_poems.append(text_prep_str)

        return prepared_poems

    def fit(self, path, name):
        df = self.load(path=path)
        df = self.first_cleaning(df=df)
        prepared_poems = self.main_work_with_poem(df=df)
        prepared_df = pd.DataFrame()
        prepared_df['text'] = prepared_poems

        os.remove(path=path)
        path = f'{os.getcwd()}/data/poems/prepared_{name}.csv'
        prepared_df.to_csv(path, index=False, encoding='utf-8')

        return path

# if __name__ == "__main__":
#     link = Cleaner(path='poems.csv', name='mandelsham').fit()
#     print(link)