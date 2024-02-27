from flask import Flask, request, jsonify  
from bson import ObjectId   
from pymongo import MongoClient
from flask_cors import CORS
import json
from bson.json_util import dumps
from flask_bcrypt import Bcrypt
import jwt

app = Flask(__name__)  
bcrypt = Bcrypt(app) 
CORS(app)    
    
client = MongoClient("mongodb://127.0.0.1:27017")  
db = client.mymongodb    #Select the database    
todos = db.todo #Select the collection name    
user_collection =  db['users']
app.config['SECRET_KEY'] = 'kuntimalla'
      
      
#  add todo,
#  view todos,
#  update todo
#  delete todo  
# todo = {
#     todo: string,
#     completed: boolean,
# }

# { todo: "" }


@app.route('/signup',methods=['POST'])
def signup():
   # called payload this part
    username = request.json['username']
    password=request.json['password']
    email=request.json['email']
    print(username, email, password)
    # Encrypting the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    print(hashed_password,"hashed_password")
    # checking part here goes on
    account = user_collection.find_one({'$or': [{'username': username}, {'email': email}]})
    if account is not None:
    # is not NONE means its having both username and password
        msg =  'Account already Exists!'
        return jsonify(success=False, message=msg), 200
    
    account_id = user_collection.insert_one(dict(username=username, password=hashed_password, email=email)).inserted_id
    print(account_id)
    return  jsonify(success=True, id=str(account_id), message="User registered successfully"), 200


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user_detail = user_collection.find_one({'email': email})
    # Checking if the user is registered
    if user_detail is None:
        msg = 'User Not registered'
        return jsonify(success=False, message=msg), 200

    # Checking the password
    if not bcrypt.check_password_hash(user_detail['password'], password):
        msg = 'Password Does not match'
        return jsonify(success=False, message=msg), 200

    # Generating JWT token
    token_payload = {
        'user_id': str(user_detail['_id']),
    }
    token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify(success= True, message="Successful login", token=token)



@app.route('/todos', methods=["POST"])
def create_todo():
    todo = request.json["todo"]
    # in the database the todo_item and iscompleted are the ref keys for the collections
    todo_id = todos.insert_one({"todo_item": todo, "isCompleted": False}).inserted_id
    todo = todos.find_one({"_id": ObjectId(todo_id)})
    print("todo",todo)
    # the json.load(dump) working as the python object converting into a json formatted 
    # because the db is storing the details in the form of json only
    parsed_todo = json.loads(dumps(todo))
    
    return jsonify(success=True, message="Task has been added", todo=parsed_todo), 201
# Getting the all todos
@app.route('/todos', methods=["GET"])
def retrieve_todos():
    data = todos.find()
    print (data,"data")
    parsed_todos = json.loads(dumps(data))
    print("todos", parsed_todos)
    return jsonify(success=True, todos=parsed_todos), 200

# deleting the todo item
@app.route('/remove/<todo_id>',methods=['DELETE'])
def remove_item(todo_id):
    todos.delete_one({"_id": ObjectId(todo_id)})
    return jsonify(success = True,message = "Item is removed" ),200

# updating the item
@app.route('/update/<todo_id>',methods=['PUT'])
def  update_item(todo_id):
    new_task = request.json['new_task']
    query = { "_id": ObjectId(todo_id) }
    new_values = { "$set": { "todo_item": new_task } }
    todos.update_one(query, new_values)
    return jsonify(success = True, message = "Item is Updated"), 200

# completing the task
@app.route('/complete/<todo_id>', methods=['PUT'])
def complete_task(todo_id):
    is_completed = request.json['isCompleted']
    query = { "_id": ObjectId(todo_id) }
    new_values = { "$set": { "isCompleted": is_completed } }
    todos.update_one(query, new_values)
    return jsonify(success = True, message = "Item is Updated"), 200
    

# Endpoint to get the current todo list
@app.route('/todo', methods=['GET'])
def get_todo_list():
    return jsonify({'todo_list': todos})


    
if __name__ == "__main__":    
    app.run(debug=True)   