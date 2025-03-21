# test_pymongo.py
try:
    from pymongo import MongoClient
    print("pymongo imported successfully!")
except ImportError:
    print("pymongo import failed!")
