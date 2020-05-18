from flask import Flask, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import os 

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

mongo_str = os.getenv('mongo_str')
client = MongoClient(mongo_str)
feed_collection = client['heroku_tdwqwm9s']['feedback']

@app.route('/rating/create', methods=['POST'])
@cross_origin()
def submit_rating(): 
    user_id = ''
    rating = 0

    try: 
        user_id = request.args.get('id')
        rating = int(request.args.get('rating'))
    except: 
        return 'Bad Req', 400 

    user_in_db = feed_collection.findone({"user_id" : user_id}); 

    if user_in_db is None: 
        db_entry = { "user_id" : user_id, "rating" : rating }
        feed_collection.insert_one(db_entry)
    
    feed_collection.find_and_modify(query={'user_id':user_id}, update={"$set": {'rating': rating}}, upsert=False, full_response= True)

    return 'OK', 200

@app.route('/issue/create', methods=['POST'])
@cross_origin()
def submit_issue():
    user_id = ''
    issue = ''

    try: 
        user_id = request.args.get('id')
        issue = request.args.get('issue')
    except: 
        return 'Bad Req', 400 

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
