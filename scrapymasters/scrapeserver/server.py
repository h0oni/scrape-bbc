#!/usr/bin/env python
import web
# import sys
# sys.path.insert(0, '/Users/maxwittman/Workspaces/Python/scrapymasters/scrapymasters')

# sys.path.append(path)
# import sys
# sys.path.append("..")
# import scrapymasters.common.ConfigFiles
# import scrapymasters.common.MongoUtils

# import scrapymasters.common.ConfigFiles
# import scrapymasters.common.MongoUtils

# from common.ConfigFiles import ConfigFiles
# from common.MongoUtils import MongoUtils

from scrapymasters.common.ConfigFiles import ConfigFiles
from scrapymasters.common.MongoUtils import MongoUtils

# from ..common.ConfigFiles import ConfigFiles
# from ..common.MongoUtils import MongoUtils

# from common.ConfigFiles import ConfigFiles
# from common.MongoUtils import MongoUtils

urls = (
    '/articles', 'Articles'
    # '/users/(.*)', 'get_user'
)

# def run(self, port=8080, *middleware):
#         func = self.wsgifunc(*middleware)
#         return web.httpserver.runsimple(func, ('0.0.0.0', port))

app = web.application(urls, globals())


class Articles:
    def __init__(self):
        self.config = ConfigFiles.config()

    def GET(self):
        client = MongoUtils.create_client_from_config(self.config)
        db = client.scrape
        articles = db.articles.find()
        client.close()
        return articles

    def PUT(self):
        return "putting articles"

# class get_user:
#     def GET(self, user):
# 	for child in root:
# 		if child.attrib['id'] == user:
# 		    return str(child.attrib)

if __name__ == "__main__":
    app.run()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Get article by url
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# db.articles.aggregate([
#     {$unwind : "$articles"},
#     {$match : {"articles.url" : "http://localhost:8090/world-latin-america-35565085.html"}},
#     {$project : {_id : 0,
#                  url : "$articles.url",
#                  body : "$articles.body",
#                  tags : "$articles.tags",
#                  summary : "$articles.summary",
#                  title : "$articles.title"}}
# ])
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# "index": {
#   "limited": ["http://localhost:8090/world-australia-35339947.html"],
#   "leighton": ["http://localhost:8090/in-pictures-35472652.html"],
#   "teleconnection": ["http://localhost:8090/science-environment-35566151.html"], }