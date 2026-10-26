"""
CRUD_Python_Module.py

Reusable CRUD module for the Austin Animal Center (AAC) outcomes data.
Provides an AnimalShelter class that other Python scripts can import to
create, read, update, and delete documents in a MongoDB collection
using PyMongo.
"""

from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter:
    """CRUD operations for the animals collection in the aac MongoDB database."""

    def __init__(self, username, password, host="localhost", port=27017,
                 database="aac", collection="animals"):
        """
        Connect to MongoDB and select the database and collection.

        Credentials are passed in by the caller rather than hardcoded,
        so the same class can be reused with different accounts or servers.
        """
        # Escape special characters so the credentials are safe inside the URI
        uri = "mongodb://%s:%s@%s:%d" % (
            quote_plus(username), quote_plus(password), host, port
        )

        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # MongoClient connects lazily; ping forces a round trip so a bad
            # password or unreachable server fails here instead of later
            self.client.admin.command("ping")
        except PyMongoError as error:
            raise ConnectionError(
                "Could not connect to MongoDB: %s" % error
            ) from error

        self.database = self.client[database]
        self.collection = self.database[collection]

    def create(self, data):
        """
        Insert one document into the collection (the C in CRUD).

        :param data: dictionary of key/value pairs to insert
        :return: True if the insert succeeded, otherwise False
        """
        # Reject anything that is not a non-empty dictionary before
        # touching the database
        if not isinstance(data, dict) or not data:
            print("Create failed: data must be a non-empty dictionary.")
            return False

        try:
            # Insert a copy so PyMongo does not add an _id field to the
            # caller's original dictionary
            result = self.collection.insert_one(dict(data))
            # acknowledged is True when the server confirms the write
            return result.acknowledged
        except PyMongoError as error:
            print("Create failed: %s" % error)
            return False

    def read(self, query):
        """
        Query the collection for matching documents (the R in CRUD).

        :param query: dictionary of key/value pairs to match with find()
        :return: list of matching documents, or an empty list on failure
        """
        # find() requires a dictionary filter
        if not isinstance(query, dict):
            print("Read failed: query must be a dictionary.")
            return []

        try:
            # find() returns a Cursor; list() iterates it and collects
            # every matching document
            return list(self.collection.find(query))
        except PyMongoError as error:
            print("Read failed: %s" % error)
            return []

    def update(self, query, new_values, multiple=True):
        """
        Change documents that match a query (the U in CRUD).

        :param query: dictionary of key/value pairs that selects documents
        :param new_values: update document for the MongoDB driver, such as
                           {"$set": {"outcome_type": "Transfer"}}. A plain
                           dictionary with no operators is wrapped in $set.
        :param multiple: True uses update_many(); False uses update_one()
        :return: number of documents modified, or 0 on failure
        """
        # Both arguments must be dictionaries, and the update cannot be empty
        if not isinstance(query, dict):
            print("Update failed: query must be a dictionary.")
            return 0
        if not isinstance(new_values, dict) or not new_values:
            print("Update failed: new_values must be a non-empty dictionary.")
            return 0

        # The driver requires update operators such as $set. If the caller
        # passed plain field values, wrap them in $set so existing fields
        # are changed instead of the whole document being rejected
        if not any(key.startswith("$") for key in new_values):
            new_values = {"$set": new_values}

        try:
            if multiple:
                result = self.collection.update_many(query, new_values)
            else:
                result = self.collection.update_one(query, new_values)
            # modified_count only counts documents whose values actually
            # changed, not every document the query matched
            return result.modified_count
        except PyMongoError as error:
            print("Update failed: %s" % error)
            return 0

    def delete(self, query, multiple=True):
        """
        Remove documents that match a query (the D in CRUD).

        :param query: dictionary of key/value pairs that selects documents
        :param multiple: True uses delete_many(); False uses delete_one()
        :return: number of documents removed, or 0 on failure
        """
        if not isinstance(query, dict):
            print("Delete failed: query must be a dictionary.")
            return 0

        # An empty filter matches every document, so refuse it to prevent
        # accidentally wiping the whole collection
        if not query:
            print("Delete failed: an empty query would remove every document.")
            return 0

        try:
            if multiple:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count
        except PyMongoError as error:
            print("Delete failed: %s" % error)
            return 0

    def close(self):
        """Close the connection to MongoDB."""
        self.client.close()