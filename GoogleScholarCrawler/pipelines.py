# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from itemadapter import ItemAdapter

from GoogleScholarCrawler import config


class PaperCitationPipeline:

    def __init__(self):
        self.mysql, self.table = config.get_mysql()
        self.conn = pymysql.connect(**self.mysql)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['status'] == 'OK':
            self.cursor.execute(f'UPDATE `{self.table}` SET citation=%s, finished=1 WHERE id=%s',
                                (adapter['citation'], adapter['paper_id']))
        elif adapter['status'] == 'blocked':
            self.cursor.execute(f'UPDATE `{self.table}` SET finished=2 WHERE id=%s',
                                adapter['paper_id'])
        elif adapter['status'] == 'not found':
            self.cursor.execute(f'UPDATE `{self.table}` SET finished=3 WHERE id=%s',
                                adapter['paper_id'])
        self.conn.commit()
        return item
