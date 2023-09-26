# course-manager api

how to get course manager api running

- create a venv ativate it then install the requirements

`python -m venv myenv`

`myenv\Scripts\activate`

`pip install -r requirements.txt`


- then in the working directory run this command to run the uvicorn server

`uvicorn main:app --host 0.0.0.0 --port 8000`

- finally go to the following link to test the api

`http://localhost:8000/docs` 

- to populate the database with some sample data run populate.py
`python3 populate.py`


- Optional
- if you are running this on a windows machine you may have to set the execution policy to run your virutal enviroment

` Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
