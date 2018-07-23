from flask import Flask, jsonify
from flask.json import JSONEncoder
from flask_restful import Api, Resource, abort

import scrapy, json
from scrapy.crawler import CrawlerProcess
from tyspider.spiders import tyspd

def start_process(crawler):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(tyspd.TySpider)
    process.start()
    print 'fin'



class CrawlerItem:
    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            'name': self.name
        }

crawler_dict = {
    'TySpider': CrawlerItem('TySpider')
}

class CrawlerItemJSONEncoder(JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, CrawlerItem):
            return json.dumps(obj.__dict__)
        else:
            return JSONEncoder.default(self, obj)

class Crawler(Resource):
    def get(self, name=None):
        if name:
            if crawler_dict.has_key(name):
                return jsonify(crawler_dict[name])
            else:
                abort(404, message='Crawler {0} doesn\'t exist'.format(name))
        else:
            return jsonify(crawler_dict.values())

app = Flask(__name__)
api = Api(app)
app.json_encoder = CrawlerItemJSONEncoder
api.add_resource(Crawler, '/crawlers', '/crawlers/<string:name>', endpoint='crawlers')

if __name__ == '__main__':
    app.run(debug=True)
