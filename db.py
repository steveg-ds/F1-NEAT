from pymongo import MongoClient

class MongoDB:
    def __init__(self, host='localhost', port=27017, db_name='mydatabase', collection_name='mycollection'):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def open_connection(self):
        """Open connection to MongoDB."""
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def close_connection(self):
        """Close connection to MongoDB."""
        if self.client:
            self.client.close()

    def create_collection(self, collection_name=None):
        """Create a new collection."""
        collection_name = collection_name or self.collection_name
        self.db.create_collection(collection_name)
        print(f"Collection '{collection_name}' created successfully.")

    def truncate_collection(self, collection_name=None):
        """Truncate (remove all documents from) a collection."""
        collection_name = collection_name or self.collection_name
        self.db[collection_name].delete_many({})
        print(f"Collection '{collection_name}' truncated successfully.")

    def insert_document(self, document):
        """Insert a single document into the collection."""
        self.collection.insert_one(document)
        # print("Document inserted successfully.")

    def insert_documents(self, documents):
        """Insert multiple documents into the collection."""
        self.collection.insert_many(documents)
        print("Documents inserted successfully.")

    def find_documents(self, query={}):
        """Retrieve documents from the collection based on a query."""
        cursor = self.collection.find(query)
        documents = list(cursor)
        return documents

    def aggregate(self, pipeline):
        """Perform an aggregation query on the collection."""
        result = self.collection.aggregate(pipeline)
        return list(result)
