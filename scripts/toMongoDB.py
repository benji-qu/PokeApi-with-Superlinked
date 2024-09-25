import csv
from pymongo import MongoClient
import os
data_path = os.path.abspath('.')+'/data/'

# MongoDB connection
client = MongoClient('')
db = client['poke_db']
collection = db['your_collection']

# CSV file path
csv_file_path = data_path + 'pokedex_updated.csv'

with open(csv_file_path, mode='r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        collection.insert_one(row)