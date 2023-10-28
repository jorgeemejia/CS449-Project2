# course-manager api

## (1) create a venv ativate it then install the requirements

`python -m venv myenv`

`source myenv/bin/activate`

`pip install -r requirements.txt`


## (2) in the working directory run this command to run the uvicorn server

`foreman start`

## (3) populate the database with some sample data by running populate.py

`python populate.py`

## **Note that all enrollment services now enforce role based authentication

## (4) In order to obtain an access token you must first login: 

#### To obtain an access token for the student role
``` http://localhost:8080/api/login POST username="jamessmith" password="password" ```
#### To obtain an access token for the instructor role
``` http://localhost:8080/api/login POST username="INSTRUCTOR_USERNAME" password="password" ```
#### To obtain an access token for the registrar role
``` http://localhost:8080/api/login POST username="REGISTRAR_USERNAME" password="password" ```

## (5) To use the access token, include it within the Authorization header
#### For example,  
```http GET http://localhost:8080/api/students/1/classes Authorization:"Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6InNpbTIifQ.eyJleHAiOjE3MzU2ODk2MDAsImp0aSI6Im1uYjIzdmNzcnQ3NTZ5dWlvbW5idmN4OThlcnR5dWlvcCIsInJvbGVzIjpbImFkbWluIl19.s5qlgDpy0JkGOQMYq9H1c9pOGYiaqe95KqjJILLSeR4"```

## To see all available endpoints, visit 
`http://localhost:5300/docs` 

## if you want to view what was populated in the db run test_queries.py

`python test_queries.py`

# Testing variables
- student_id 1 is on 3 waitlists (class_id: 8, 4, 13)
- class_id 2 (with instructor_id 2) has 4 dropped students
- class_id 4, 6, 8, 13, 14 are all full, but have open waitlists
- class_id 12 is fully enrolled, with a full waitlist
- all classes have a default max_enroll value of 30
- there are 500 student_ids, with upwards of 300 of them currently being used
- there are 100 instructor_ids, with only ~14 of them being used

# windows execution policy
- if you are running this on a windows machine you may have to set the execution policy to run your virutal enviroment

` Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
