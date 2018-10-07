from tqdm import tqdm
import os
import pandas as pd


class Counter:
    corpus_dir = 'data'

    def count(self):
        counter_dict = {'chars': 0, 'words': 0, 'files': 0, 'authors': }
        files = os.listdir(self.corpus_dir)
        counter_dict['files'] = len(files)

        for filename in tqdm(files):
            if filename.endswith('.txt'):
                chars, words = self.count_words(os.path.join(self.corpus_dir, filename))
                counter_dict['chars'] += chars
                counter_dict['words'] += words

            if filename.endswith('.csv'):
                data = pd.read_csv(filename, sep=',')



        counter_dict['words'] = 3055589  # REMOVE
        return counter_dict

    def count_words(self, filename):
        with open(filename, 'r') as file:
            chars_count = len(file.read())
            #words_count = len(file.read().split(' '))
            words_count = 0  # REMOVE
        return chars_count, words_count


if __name__ == "__main__":
    counter = Counter()
    print(counter.count())
