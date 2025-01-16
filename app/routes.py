# from flask import Blueprint, jsonify, request, current_app
# from datetime import datetime

# main = Blueprint("main", __name__)

# # Webhook endpoint
# @main.route("/webhook", methods=["POST"])
# def webhook():
#     data = request.json

#     # Parse GitHub webhook payload
#     action = data.get("action")
#     repository = data.get("repository", {})
#     sender = data.get("sender", {})

#     # Determine action type and format data
#     if action in ["push", "pull_request", "merge"]:
#         payload = {
#             "action": action.capitalize(),
#             "author": sender.get("login"),
#             "from_branch": data.get("pull_request", {}).get("head", {}).get("ref", ""),
#             "to_branch": data.get("pull_request", {}).get("base", {}).get("ref", ""),
#             "timestamp": datetime.utcnow().isoformat()
#         }

#         # Save to MongoDB
#         try:
#             db = current_app.mongo
#             db.events.insert_one(payload)
#             return jsonify({"message": "Event stored successfully"}), 201
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500
#     else:
#         return jsonify({"message": "Unsupported action"}), 400

# # Fetch events
# @main.route("/events", methods=["GET"])
# def get_events():
#     try:
#         db = current_app.mongo
#         events = list(db.events.find({}, {"_id": 0}))
#         return jsonify(events), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

import hmac
import hashlib
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

main = Blueprint("main", __name__)

# GitHub secret (add to your config.py for better security)
GITHUB_SECRET = "job123"

# Webhook endpoint
@main.route("/webhook", methods=["POST"])
def webhook():
    # Verify GitHub signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not is_valid_signature(request.data, signature):
        return jsonify({"error": "Invalid signature"}), 401

    data = request.json

    # Parse event type
    event = request.headers.get("X-GitHub-Event")
    if event == "push":
        payload = {
            "action": "Push",
            "author": data["pusher"]["name"],
            "from_branch": "",
            "to_branch": data["ref"].split("/")[-1],  # Extract branch name
            "timestamp": datetime.utcnow().isoformat()
        }
    elif event == "pull_request":
        action = data["action"]
        if action == "opened" or action == "reopened":
            payload = {
                "action": "Pull Request",
                "author": data["pull_request"]["user"]["login"],
                "from_branch": data["pull_request"]["head"]["ref"],
                "to_branch": data["pull_request"]["base"]["ref"],
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return jsonify({"message": "Event ignored"}), 200
    else:
        return jsonify({"message": "Event type not supported"}), 400

    # Store the payload in MongoDB
    try:
        db = current_app.mongo
        db.events.insert_one(payload)
        return jsonify({"message": "Event stored successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def is_valid_signature(payload, signature):
    if not signature:
        return False
    secret = bytes(GITHUB_SECRET, "utf-8")
    hash = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    expected_signature = f"sha256={hash}"
    return hmac.compare_digest(expected_signature, signature)
