from flask import Flask, request
from pymongo import MongoClient
import os 

app = Flask(__name__)
mongo_str = os.getenv('mongo_str')
client = MongoClient(mongo_str)
feed_collection = client['heroku_tdwqwm9s']['feedback']

@app.route('/rating/create', methods=['POST'])
def submit_rating(): 
    req_data = request.get_json()

    user_id = req_data['id']
    rating = req_data['rating']

    if type(rating) is not int: 
        return 'Invalid rating', 400

    user_in_db = feed_collection.findone({"user_id" : user_id}); 

    if user_in_db is None: 
        db_entry = { "user_id" : user_id, "rating" : rating }
        feed_collection.insert_one(db_entry)
    
    feed_collection.find_and_modify(query={'user_id':user_id}, update={"$set": {'rating': rating}}, upsert=False, full_response= True)

    return 'OK', 200

@app.route('/issue/create', methods=['POST'])
def submit_issue():
    req_data = request.get_json()

    user_id = req_data['id']
    issue = req_data['issue']

    user_in_db = feed_collection.findone({"user_id" : user_id}); 

    if user_in_db is None: 
        db_entry = { "user_id" : user_id, "issue" : issue }
        feed_collection.insert_one(db_entry)
    
    feed_collection.find_and_modify(query={'user_id':user_id}, update={"$set": {'issue': issue}}, upsert=False, full_response= True)

    return 'OK', 200

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
