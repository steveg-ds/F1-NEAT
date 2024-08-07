from pymongo import MongoClient

class MongoDB:
    """
    A class for interacting with a MongoDB database.

    Attributes:
        host (str): The MongoDB server host (default is 'localhost').
        port (int): The MongoDB server port (default is 27017).
        db_name (str): The name of the database (default is 'mydatabase').
        collection_name (str): The name of the collection (default is 'mycollection').
        client (MongoClient): The MongoDB client instance.
        db (Database): The MongoDB database instance.
        collection (Collection): The MongoDB collection instance.
    """

    def __init__(self, host='localhost', port=27017, db_name='mydatabase', collection_name='mycollection'):
        """
        Initialize MongoDB connection parameters.

        Args:
            host (str): The MongoDB server host.
            port (int): The MongoDB server port.
            db_name (str): The name of the database.
            collection_name (str): The name of the collection.
        """
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def open_connection(self):
        """
        Open a connection to the MongoDB server and select the database and collection.
        """
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def close_connection(self):
        """
        Close the connection to the MongoDB server.
        """
        if self.client:
            self.client.close()

    def create_collection(self, collection_name=None):
        """
        Create a new collection in the database.

        Args:
            collection_name (str): The name of the new collection. If None, the default collection_name is used.
        """
        collection_name = collection_name or self.collection_name
        self.db.create_collection(collection_name)
        print(f"Collection '{collection_name}' created successfully.")

    def truncate_collection(self, collection_name=None):
        """
        Remove all documents from a collection.

        Args:
            collection_name (str): The name of the collection to truncate. If None, the default collection_name is used.
        """
        collection_name = collection_name or self.collection_name
        self.db[collection_name].delete_many({})
        print(f"Collection '{collection_name}' truncated successfully.")

    def insert_document(self, document):
        """
        Insert a single document into the collection.

        Args:
            document (dict): The document to insert.
        """
        self.collection.insert_one(document)
        print("Document inserted successfully.")

    def insert_documents(self, documents):
        """
        Insert multiple documents into the collection.

        Args:
            documents (list of dict): A list of documents to insert.
        """
        self.collection.insert_many(documents)
        print("Documents inserted successfully.")

    def find_documents(self, query={}):
        """
        Retrieve documents from the collection based on a query.

        Args:
            query (dict): The query to filter documents. Defaults to an empty query, which retrieves all documents.

        Returns:
            list of dict: A list of documents that match the query.
        """
        cursor = self.collection.find(query)
        documents = list(cursor)
        return documents

    def aggregate(self, pipeline):
        """
        Perform an aggregation query on the collection.

        Args:
            pipeline (list): The aggregation pipeline stages.

        Returns:
            list of dict: The results of the aggregation query.
        """
        result = self.collection.aggregate(pipeline)
        return list(result)
