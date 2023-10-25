# web: uvicorn main:app --host 0.0.0.0 --port $PORT --reload
# krakend: krakend run -c krakend.json
# enroll_1: uvicorn main:app --host 0.0.0.0 --port 5000 --reload
# enroll_2: uvicorn main:app --host 0.0.0.0 --port 5001 --reload
# enroll_3: uvicorn main:app --host 0.0.0.0 --port 5002 --reload
# primary: bin/litefs mount -config etc/primary.yml
# secondary_1: bin/litefs mount -config etc/secondary_1.yml
# secondary_2: bin/litefs mount - config etc/secondary_2.yml
enrollment_1: uvicorn --port $PORT main:app --reload
enrollment_2: uvicorn --port $PORT main:app --reload
enrollment_3: uvicorn --port $PORT main:app --reload
krakend:  echo krakend.json | entr -nrz krakend run --config krakend.json --port $PORT
