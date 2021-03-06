import os
import socket
import pymongo

original_socket = socket.socket

url = os.getenv("DATABASE_URL")
passwd = os.getenv("DATABASE_PASSWORD")
user = os.getenv("DATABASE_USERNAME")
database = os.getenv("DATABASE_NAME")

def check_db_options():
    """ Just to check whether database
    parameters are loaded
    """
    if not (url and passwd and user and database):
        print("Could not load Database Configurations")
        return 1

def saveToDatabase(links):
    """
    Connects to a MongoDB
    Create Mongo Collection
    Add the links to the collection
    Args:
        url (string) = url of the mongo server
        database (string) = data that is being stored in the database
        user (string) = username to login into Mongo
        passwd (string) = password of Mongo
        link (list) = URLs from the crawler
    """
    if not url and not database:
        print("URL and DATABASE are null")
        print("Links are not stored into database")
        exit()
    socket.socket = original_socket
    if not user and not passwd:
        client = pymongo.MongoClient(url)
    elif url and database and user and passwd:
        client = pymongo.MongoClient(url,
                                     username=user,
                                     password=passwd,
                                     authSource=database,
                                     authMechanism='SCRAM-SHA-256')
    else:
        print("Insufficient information to connect to Mongo")
        exit()
    try:
        db_con = client[database]
        db_con['torbot'].create_index('link', unique=True)
        for link in links:
            try:
                db_con['torbot'].insert_one({'link':link})
            except pymongo.errors.DuplicateKeyError:
                continue
    except Exception as e:
        print("Not able to Connect/Write to Mongo server.\nException: %s" % e)
        exit()
    print("Links added to Database")
    client.close()
