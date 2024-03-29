import os

from pymongo import MongoClient


class MongoConnection:

    def __init__(self, **kwargs):

        super().__init__()

        user = kwargs.get('user', os.environ.get("MONGODB_USER"))
        password = kwargs.get('password', os.environ.get("MONGODB_PASSWORD"))

        db_name = kwargs.get('database', os.environ.get("MONGODB_DATABASE"))
        collection_name = kwargs.get('collection', os.environ.get("MONGODB_COLLECTION"))

        self.connection = MongoClient()

        self.database = self.connection[db_name]

        if user or password:
            self.database.authenticate(user, password)

        self.collection = self.database[collection_name]
