# main.py

from fastapi import FastAPI, HTTPException, Body, status
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import os
# from openai import OpenAI, openai
import openai
from schemas import Note


# Initialize FastAPI app
app = FastAPI()

# MongoDB connection URI
MONGO_URI = os.environ.get("mongodb+srv://likithprince:Lucifer@1996@cluster0.mjxrwzx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Connect to MongoDB Atlas
client          = MongoClient(MONGO_URI)
db              = client["notes"]
collection      = db["notes"]

# Pydantic data model for Note


# Routes
@app.get("/notes", status_code=status.HTTP_200_OK)
async def get_notes():
    notes = list(collection.find())
    for note in notes:
        note['_id'] = str(note['_id'])
    return notes


@app.post("/notes", status_code=status.HTTP_201_CREATED)
async def create_note(note: Note):
    note_data = note.dict()
    note_data["createdAt"] = datetime.now()
    result = collection.insert_one(note_data).inserted_id
    return {"message": "Note created successfully", "id": str(result)}


@app.get("/notes/{note_id}", status_code=status.HTTP_200_OK)
async def get_note(note_id: str):
    note = collection.find_one({"_id": ObjectId(note_id)})
    if note:
        note["_id"] = str(note["_id"])
        return note
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@app.put("/notes/{note_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_note(note_id: str, updated_note: Note):
    updated_note_data = updated_note.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(note_id)}, {"$set": updated_note_data})
    if result.modified_count == 1:
        return {"message": "Note updated successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@app.delete("/notes/{note_id}", status_code=status.HTTP_200_OK)
async def delete_note(note_id: str):
    result = collection.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 1:
        return {"message": "Note deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# client = OpenAI()
# @app.post("/generate-text", status_code=status.HTTP_201_CREATED)
# async def generate_text(prompt: str = Body(...)):
#     response = client.completions.create(
#     model="davinci-002",
#     prompt=prompt
#     )
#     return response.choices[0].text.strip()

@app.post("/generate-text")
async def generate_text(prompt: str = Body(...)):
    response = openai.Completion.create(
        engine="babbage-002",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()
