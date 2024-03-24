# FastAPi CRUD Operation for Notes
### This repo is responsible for creating, Updating, deleting and fetching the notes.

Python Version - ` 3.9 `
Used pipenv to manage package versions.

To activate environment:
`pipenv shell`

Install required modules by running the below command:
`pipenv install -r requirements.txt`

Set up MongoDB Atlas and obtain your connection URI.

Set up your OpenAI API key as an environment variable.
To run the Application:
`uvicorn main:app --reload`

Refer the below link for more details:
link: ` https://www.pythontutorial.net/python-basics/install-pipenv-windows/ `


To run the Unit test cases:
`pytest test_cases.py`


### API Endpoints
The following API endpoints are available:

* GET /notes: Retrieve all notes.
* POST /notes: Create a new note.
* GET /notes/{id}: Retrieve a note by ID.
* PUT /notes/{id}: Update a note by ID.
* DELETE /notes/{id}: Delete a note by ID.
* POST /generate-text: Generate text using OpenAI API.


#### Usage Examples:

1. Retrieve all notes:
GET /notes


2. Create a new note:
POST /notes
Request Body:
{
    "title": "Note Title",
    "content": "Note Content"
}


3. Retrieve a note by ID:
GET /notes/{id}


4. Update a note by ID:
PUT /notes/{id}
Request Body:
{
    "title": "Updated Title",
    "content": "Updated Content"
}


5. Delete a note by ID:
DELETE /notes/{id}


6. Generate text using OpenAI API:
POST /generate-text
Request Body:
{
    "prompt": "Prompt Text"
}
