import pymysql
import pymongo
from mod_config import get_config

def get_mysql_db():
    return pymysql.connect(host=get_config("database-mysql","MYSQL_HOST"), port=int(get_config("database-mysql","MYSQL_PORT")), user=get_config("database-mysql","MYSQL_USERNAME"),
                         passwd=get_config("database-mysql","MYSQL_PASSWORD"), db=get_config("database-mysql","MYSQL_DB"))


def get_mongo_db():
    client = pymongo.MongoClient(host=get_config("database-mongo","MONGO_HOST"),port=int(get_config("database-mongo","MONGO_PORT")),password=(get_config("database-mongo","MONGO_PWD")))
    return client[get_config("database-mongo","MONGO_DB")]

# def get_mongo_db():
#     client = pymongo.MongoClient("mongodb://iasroot:123abc!!#ABC@123.249.95.163:27110")
#     # client = pymongo.MongoClient("mongodb://iasroot:123abc!!#ABC@123.249.95.163:27110")
#     return client[get_config("database-mongo","MONGO_DB")]