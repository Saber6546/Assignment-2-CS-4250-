#-------------------------------------------------------------------------
# AUTHOR: Ethan Ko
# FILENAME: db_connection_mongo_solution.py
# SPECIFICATION: This program manages documents in a MongoDB database and generates an inverted index based on term frequencies. It includes functions to create, update, and delete documents, as well as generate an inverted index. 
# The user can interact with the database through a simple menu-driven interface, making it easy to manage and query documents.
# FOR: CS 4250- Assignment #2
# TIME SPENT: 10+ hours
#-----------------------------------------------------------*/
from pymongo import MongoClient

def connectDataBase():
    # Create a MongoClient to connect to MongoDB running on localhost:27017
    client = MongoClient('mongodb://localhost:27017/')
    # Access or create a database named 'mydatabase'
    db = client['mydatabase']
    return db

def createDocument(col, docId, docText, docTitle, docDate, docCat):
    # Create a dictionary to count term frequencies
    term_count = {}
    # Split the text into terms, convert to lowercase, and count frequencies
    terms = docText.lower().split()
    for term in terms:
        if term in term_count:
            term_count[term] += 1
        else:
            term_count[term] = 1
    
    # Prepare the document object
    document = {
        "id": docId,
        "text": docText,
        "title": docTitle,
        "date": docDate,
        "category": docCat,
        "term_count": term_count  # Include term frequency in the document
    }
    
    # Insert the document into the collection
    col.insert_one(document)
    print("Document inserted successfully.")

def deleteDocument(col, docId):
    # Delete the document with the given docId from the collection
    result = col.delete_one({"id": docId})
    if result.deleted_count > 0:
        print(f"Document with id {docId} deleted successfully.")
    else:
        print(f"No document found with id {docId}.")

def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    # Update the document with the given docId
    # First, delete the existing document
    deleteDocument(col, docId)
    # Then, create a new document with the updated information
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):
    # Query the collection to generate the inverted index
    inverted_index = {}
    cursor = col.find({})
    
    for document in cursor:
        terms = document['term_count']
        for term, count in terms.items():
            if term in inverted_index:
                inverted_index[term] += f",{document['title']}:{count}"
            else:
                inverted_index[term] = f"{document['title']}:{count}"
    
    return inverted_index
