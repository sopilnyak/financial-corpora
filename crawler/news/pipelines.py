import os
import csv


class NewsPipeline(object):

    def process_item(self, item, spider):

        if len(item) == 0:
            return item

        # Save to file
        output_directory = '../data'
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        filename = '{}-{}-{}'.format(spider.name, item['date'], item['id'])

        # .txt file with text itself
        with open(os.path.join(output_directory, filename + '.txt'), 'w') as file:
            file.write('\n'.join(item['paragraphs']))

        # .csv file with meta information
        with open(os.path.join(output_directory, filename + '.csv'), 'w') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(['language', 'url', 'title', 'timestamp', 'agency', 'author', 'category', 'image_url', 'image_alt'])
            writer.writerow([item['language'], item['url'], item['title'], item['timestamp'], item['agency'],
                             item['author'], item['category'], item['image_url'], item['image_alt']])

        spider.logger.info('Saved files {} and {}'.format(filename + '.txt', filename + '.csv'))

        return item
