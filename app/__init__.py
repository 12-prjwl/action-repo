# # from flask import Flask
# # from flask_cors import CORS
# from pymongo import MongoClient
# # from config import Config

# # def create_app():
# #     app = Flask(__name__)
# #     app.config.from_object(Config)

# #     # MongoDB setup
# #     mongo_client = MongoClient(app.config["MONGO_URI"])
# #     app.mongo = mongo_client["your_database_name"]  # Replace "your_database_name" with the actual name of your database

# #     # Enable CORS
# #     CORS(app)

# #     # Register routes
# #     from .routes import main
# #     app.register_blueprint(main)

# #     return app


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pymongo
# import datetime

# app = Flask(__name__)
# CORS(app)

# # MongoDB configuration
# client = MongoClient(app.config["MONGO_URI"])
# db = client['github_actions']
# collection = db['webhook_events']

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     data = request.json
#     if 'pusher' in data:  # Push event
#         event = {
#             "author": data['pusher']['name'],
#             "to_branch": data['ref'].split('/')[-1],
#             "action": "Push",
#             "timestamp": datetime.datetime.utcnow()
#         }
#     elif 'pull_request' in data:  # Pull Request event
#         event = {
#             "author": data['pull_request']['user']['login'],
#             "from_branch": data['pull_request']['head']['ref'],
#             "to_branch": data['pull_request']['base']['ref'],
#             "action": "Pull Request",
#             "timestamp": datetime.datetime.utcnow()
#         }
#     else:
#         return jsonify({"message": "Unhandled event type"}), 400

#     collection.insert_one(event)
#     return jsonify({"message": "Event received and stored"}), 200

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # MongoDB setup
    client = MongoClient(app.config["MONGO_URI"])
    app.mongo = client["your_database_name"]  # Replace with the name of your database

    # Enable CORS
    CORS(app)

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app
