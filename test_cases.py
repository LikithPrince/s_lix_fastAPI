# test_main.py

from fastapi.testclient import TestClient
from main import app
import pytest
from pymongo import MongoClient
import os
from main import MONGO_URI


# Initialize test client
client = TestClient(app)

# Test MongoDB connection
@pytest.fixture(scope="module")
def mongo_client():
    # Connect to test MongoDB Atlas
    client = MongoClient(MONGO_URI)
    db = client["test_db"]
    yield db
    client.drop_database("test_db")

def test_get_notes():
    # Test retrieving all notes
    response = client.get("/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_note():
    # Test creating a new note
    response = client.post("/notes", json={"title": "Test Note", "content": "This is a test note"})
    assert response.status_code == 201
    assert "id" in response.json()


def test_get_note():
    # Test retrieving a specific note
    response = client.post("/notes", json={"title": "Test Note", "content": "This is a test note"})
    note_id = response.json()["id"]
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 202
    assert response.json()["title"] == "Test Note"

def test_update_note():
    # Test updating a note
    response = client.post("/notes", json={"title": "Test Note", "content": "This is a test note"})
    note_id = response.json()["id"]
    response = client.put(f"/notes/{note_id}", json={"content": "Updated content"})
    assert response.status_code == 202

def test_delete_note():
    # Test deleting a note
    response = client.post("/notes", json={"title": "Test Note", "content": "This is a test note"})
    note_id = response.json()["id"]
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200

# Test OpenAI API integration
def test_generate_text():
    # Test text generation
    response = client.post("/generate-text", json={"prompt": "Once upon a time"})
    assert response.status_code == 201
    assert len(response.text) > 0
