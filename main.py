from fastapi import FastAPI
from routes import router 
from users_routes import users_router 
import sys

app = FastAPI()

app.include_router(router)
app.include_router(users_router)

if __name__ == "__main__":
    import uvicorn
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    uvicorn.run(app, host="0.0.0.0", port=port)