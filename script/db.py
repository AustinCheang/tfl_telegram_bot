from pymongo import MongoClient
from dotenv import load_dotenv
import os


class Mongodb:

    def __init__(self):
        load_dotenv()
        self._DB_PW = os.getenv("MONGO_DB_PW")
        self.cluster = MongoClient(
            f"mongodb+srv://austincheang:{self._DB_PW}@cluster0.s6udzp8.mongodb.net/?retryWrites=true&w=majority"
        )
        self.db = self.cluster["bot_user_db"]
        self.bot_user_collection = self.db["bot_user"]
        self.scheduled_user_collection = self.db["scheduled_user"]

    # ------------------ User DB -------------------------

    def register_user(self, message, subscribed_stations=[], schedule=None):
        self.bot_user_collection.insert_one({
            "_id": message.from_user.id,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "subscribed_stations": subscribed_stations,
            "schedule": schedule
        })
        print(
            f"registered {message.from_user.first_name} with id: {message.from_user.id} successfully"
        )

    def check_exisiting_user(self, message):
        user = self.bot_user_collection.find_one(message.from_user.id)
        return True if user != None else False

    # ---------------- Schedule DB ----------------------

    def register_user_schedule(self, message, stations):
        self.scheduled_user_collection.insert_one({
            "_id":
            message.from_user.id,
            "first_name":
            message.from_user.first_name,
            "last_name":
            message.from_user.last_name,
            "scheduled_stations":
            stations
        })

    def update_user_schedule(self, message, stations):
        self.scheduled_user_collection.update_one(
            {'_id': message.from_user.id},
            {"$set": {
                'scheduled_stations': stations
            }})

    def get_all_scheduled_users(self):
        documents = self.scheduled_user_collection.find({})
        users_dict = []
        for document in documents:
            user_dict = {}
            user_dict['_id'] = document['_id']
            user_dict['first_name'] = document['first_name']
            user_dict['last_name'] = document['last_name']
            user_dict['scheduled_stations'] = document['scheduled_stations']
            users_dict.append(user_dict)

        return users_dict

    def delete_schedule(self, message):
        self.scheduled_user_collection.delete_one(
            {'_id': message.from_user.id})

    def check_exisiting_scheduled_user(self, message):
        user = self.scheduled_user_collection.find_one(message.from_user.id)
        return True if user != None else False
