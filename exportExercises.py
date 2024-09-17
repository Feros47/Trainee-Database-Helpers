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

# Function to fetch all exercises from Firestore
def fetch_exercises():
    try:
        exercises_ref = db.collection(collection_name)
        docs = exercises_ref.stream()

        exercises = []
        for doc in docs:
            exercise = doc.to_dict()
            exercise['id'] = doc.id  # Include document ID if needed
            exercises.append(exercise)

        return exercises
    except Exception as e:
        logging.error(f"An error occurred while fetching exercises: {e}")
        return []

# Function to write exercises data to a JSON file
def write_to_json(data, filename='exercises.json'):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info(f"Data successfully exported to {filename}")
    except Exception as e:
        logging.error(f"An error occurred while writing to JSON: {e}")

if __name__ == "__main__":
    exercises = fetch_exercises()
    if exercises:  # Only write to JSON if data was fetched successfully
        write_to_json(exercises)
