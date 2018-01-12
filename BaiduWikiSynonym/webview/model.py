import pymongo

PAGE_SIZE = 12
MONGODB_URI = 'mongodb://root:YLQ-kahsolt@kahsolt.tk'
MONGODB_DATABASE = 'NG'

mongo = pymongo.MongoClient(MONGODB_URI)
db = mongo[MONGODB_DATABASE]


def getCollections():
    return db.collection_names()

def getCollection(coll, page=0, pageSize=PAGE_SIZE):
    cur = db[coll].find().skip(page*pageSize).limit(pageSize)
    count = db[coll].count()
    docs = []
    for d in cur:
        docs.append(d)

    return docs, count, int(count/PAGE_SIZE)