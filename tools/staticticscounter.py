from tqdm import tqdm
import os
import pandas as pd
from collections import Counter


class StaticticsCounter:

    corpus_dir = 'data'

    def count(self):

        counter_dict = {'chars': 0, 'words': 0, 'files': 0, 'authors': 0, 'agencies': 0, 'categories': 0}

        files = os.listdir(self.corpus_dir)
        counter_dict['files'] = len(files) // 2

        authors = []
        agencies = []
        categories = []

        for filename in tqdm(files):
            if filename.endswith('.txt'):
                chars, words = self.count_words(os.path.join(self.corpus_dir, filename))
                counter_dict['chars'] += chars
                counter_dict['words'] += words

            if filename.endswith('.csv'):
                data = pd.read_csv(os.path.join(self.corpus_dir, filename), sep=',')
                authors.append(data['author'][0])
                if not pd.isnull(data['agency'][0]):
                    agencies.append(data['agency'][0])
                if not pd.isnull(data['category'][0]):
                    categories.append(data['category'][0])

        authors_counter = Counter(authors)
        if 'unknown' in authors_counter:
            authors_counter.pop('unknown')
        print(authors_counter)
        counter_dict['authors'] = len(authors_counter) - 1  # one is 'unknown'

        agencies_counter = Counter(agencies)
        print(agencies_counter)
        counter_dict['agencies'] = len(agencies_counter)

        categories_counter = Counter(categories)
        print(categories_counter)
        counter_dict['categories'] = len(categories_counter)

        return counter_dict

    def count_words(self, filename):
        with open(filename, 'r') as file:
            content = file.read()
            chars_count = len(content)
            words_count = len(content.split(' '))
        return  chars_count, words_count


if __name__ == "__main__":
    counter = StaticticsCounter()
    print(counter.count())
