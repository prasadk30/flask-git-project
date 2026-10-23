from flask import Flask, jsonify, render_template, request
import json
import os
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection (database: todo_db, collection: items)
mongo_client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/"),
                           serverSelectionTimeoutMS=3000)
todo_collection = mongo_client["todo_db"]["items"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():
    with open("data.json") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/todo")
def todo():
    return render_template("todo.html")


# ---- More routes can be added below this line ----


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    # Works with both HTML form data and JSON
    data = request.get_json(silent=True) or request.form
    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"error": "itemName and itemDescription are required"}), 400

    try:
        todo_collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description,
        })
    except Exception as e:
        return jsonify({"error": "Could not save to MongoDB", "details": str(e)}), 500

    return jsonify({"message": "To-Do item saved successfully"}), 201


# ---- Run the app ----
if __name__ == "__main__":
    app.run(debug=True)
    
