import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
#Create mongo client
conn_str = os.getenv("DATABASE_URL")
client  = MongoClient(conn_str)

dbs = client.list_database_names()
NoteHub = client.NoteHub
collections = NoteHub.list_collection_names()

db = client["NoteHub"]
collection = db["Tasks"]

def show_menu():
    print("Task Manager Menu:")
    print("1. Add a task")
    print("2. List all tasks")
    print("3. Delete a task")
    print("4. Update a task")
    print("5. Exit")

def add_task():
    title = input("Enter task title: ") or "undefined"
    description = input("Enter task description: ") or "undefined"
    time = input("Enter the time where the tasks needs to be completed: ") or "undefined"
    
    folderid = '648abb902b12f0d5bec984e0'

    document = {
    "title": title,
    "description": description,
    "time": time,
    "folderid": {"$oid": folderid}
    }

    collection.insert_one(document)
    print("Sucessfully added task")


def list_tasks():
    x= 0
    for Task in collection.find():
        x+=1
        print(str(x)+". "+Task["title"])
        print("Description: "+Task["description"])
        print("Time: "+Task["time"])
        print("")
    

def delete_task():
    x= 0
    for Task in collection.find():
        x+=1
        print(str(x)+". "+Task["title"])
    id = input("Enter which number you want to delete: ")

        
    try: 
        # Retrieve the second document in ascending order
        document = collection.find({}, skip=int(id)-1, limit=1).next()
        object_id = document["_id"]

        # Delete the document that matches the filter
        filter = {"_id": object_id}
        collection.delete_one(filter)
        print("Sucessfully deleted")
    except ValueError:
        print("Invalid input only Integers accepted.")
    except:
        print("Couldn't delete. It's might be out of bounds.")
    


    
def update_task():
    x= 0
    for Task in collection.find():
        x+=1
        print(str(x)+". "+Task["title"])
    document = None    
    try:
        id = input("Enter which number you want to update: ")

        document = collection.find({}, skip=int(id)-1, limit=1).next()
        object_id = document["_id"]
    except ValueError:
        print("Invalid input only Integers accepted.")
    except: 
        print("Out of bounds. Enter a valid number again.")
        update_task()
    
    try: 
        title = input("Enter title to update default"+"("+document['title']+")" ) or document['title']
        description = input("Enter description to update default"+"("+document['description']+")" ) or document['description']
        time = input("Enter time to update default"+"("+document['time']+")" ) or document['time']
        folderid = input("Enter folderid to change the folder location"+"("+str(document['folderid'])+")" ) or document['folderid']
        
        filter = {"_id": object_id}
        update = {
        "$set": {
            "title": title,
            "description": description,
            "time": time,
            "folderid": {"$oid": folderid}
        }
        }
        collection.update_one(filter, update)
        print("Update was successful")
    except: 
        print("Couldn't update")
    
    
# Main program loop
while True:
    
    show_menu()
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        add_task()
        print("")
    elif choice == "2":
        list_tasks()
        print("")
    elif choice == "3":
        delete_task()
        print("")
    elif choice == "4":
        update_task()
        print("")

    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
