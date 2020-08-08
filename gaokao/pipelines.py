# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json 


class GaokaoPipeline:
    def process_item(self, item, spider):
        json_str=json.dumps(item)
        print(item['name'])
        with open('universities.json','a') as f:
            f.write(json_str+str(','))

