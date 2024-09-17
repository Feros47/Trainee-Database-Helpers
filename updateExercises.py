import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("ServiceAccount.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Define the collection name
collection_name = 'exercises'

# Function to delete all exercises in Firestore
def delete_all_exercises():
    try:
        exercises_ref = db.collection(collection_name)
        docs = exercises_ref.stream()

        for doc in docs:
            doc.reference.delete()
            logging.info(f"Deleted exercise with ID: {doc.id}")

    except Exception as e:
        logging.error(f"An error occurred while deleting exercises: {e}")

# Function to add new exercises from JSON file to Firestore
def add_new_exercises_from_json(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Extract the list of exercises from the "exercises" key
        new_exercises = data.get("exercises", [])

        if not isinstance(new_exercises, list):
            raise ValueError("The 'exercises' key should contain a list of exercises")

        exercises_ref = db.collection(collection_name)
        
        for exercise in new_exercises:
            if not isinstance(exercise, dict):
                raise ValueError("Each exercise should be a dictionary")
            exercises_ref.add(exercise)
            logging.info(f"Added exercise: {exercise.get('name', 'Unnamed')}")

    except ValueError as ve:
        logging.error(f"Value error: {ve}")
    except json.JSONDecodeError as jde:
        logging.error(f"JSON decode error: {jde}")
    except Exception as e:
        logging.error(f"An error occurred while adding new exercises: {e}")

if __name__ == "__main__":
    # Path to your JSON file
    json_file_path = 'exercises.json'
    
    # Delete all existing exercises
    delete_all_exercises()

    # Add new exercises from JSON file
    add_new_exercises_from_json(json_file_path)
