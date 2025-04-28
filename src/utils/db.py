import pymysql
import pymongo
from utils.mod_config import get_config

def get_mysql_db():
    return pymysql.connect(host=get_config("database-mysql","MYSQL_HOST"), port=int(get_config("database-mysql","MYSQL_PORT")), user=get_config("database-mysql","MYSQL_USERNAME"),
                         passwd=get_config("database-mysql","MYSQL_PASSWORD"), db=get_config("database-mysql","MYSQL_DB"))


def get_mongo_db():
    host = get_config("database-mongo","MONGO_HOST")
    port = int(get_config("database-mongo","MONGO_PORT"))
    username = get_config("database-mongo","MONGO_USER")
    password = get_config("database-mongo","MONGO_PWD")
    db_name = get_config("database-mongo","MONGO_DB")
    client = pymongo.MongoClient(host=host,port=int(port),username=username,password=password)
    db = client[db_name]
    return db

# def get_mongo_db():
#     client = pymongo.MongoClient("mongodb://iasroot:123abc!!#ABC@123.249.95.163:27110")
#     # client = pymongo.MongoClient("mongodb://iasroot:123abc!!#ABC@123.249.95.163:27110")
#     return client[get_config("database-mongo","MONGO_DB")]