import csv
from pymongo import MongoClient
import os
data_path = os.path.abspath('.')+'/data/'

url = "mongodb+srv://benjaminquartiermeister:MTFlTzPWbNEEdiCJ@cluster0.bf8xk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(url)
db = client['Pokedex']
collection = db['Collection_1']

csv_file_path = data_path + 'pokedex.csv'

with open(csv_file_path, mode='r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
        collection.insert_one(row)
