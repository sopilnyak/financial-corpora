import os
import csv
import spacy


class NewsPipeline(object):

    output_directory = '../data'

    def open_spider(self, spider):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        self.tokenizer = spacy.load('en_core_web_sm')

    def process_item(self, item, spider):
        if len(item) == 0:
            return item

        # Save to file
        filename = '{}-{}-{}'.format(spider.name, item['date'], item['id'])

        text = '\n'.join(item['paragraphs'])

        # .txt file with text itself
        with open(os.path.join(self.output_directory, filename + '.txt'), 'w', encoding='utf-8') as file:
            file.write(text)

        # .csv file with meta information
        with open(os.path.join(self.output_directory, filename + '.csv'), 'w') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(['language', 'url', 'title', 'timestamp', 'agency',
                             'author', 'category', 'image_url', 'image_alt'])
            writer.writerow([item['language'], item['url'], item['title'], item['timestamp'], item['agency'],
                             item['author'], item['category'], item['image_url'], item['image_alt']])

        doc = self.tokenizer(text)
        with open(os.path.join(self.output_directory, filename + '.tokens'), 'w', encoding='utf-8') as file:
            file.write("(id, start_pos, end_pos, text)\n")
            file.write('\n'.join([str((token.i, token.idx, token.idx + len(token.text), token.text)) for token in doc]))

        with open(os.path.join(self.output_directory, filename + '.segments'), 'w', encoding='utf-8') as file:
            file.write("(id, start_token, end_token, text)\n")
            file.write('\n'.join([str((i, s.start, s.end, s.text)) for i, s in enumerate(doc.sents)]))

        spider.logger.info('Saved files {} and {}'.format(filename + '.txt', filename + '.csv'))

        return item
