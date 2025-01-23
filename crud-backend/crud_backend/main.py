from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus

from crud_backend.routes import clients, projects, tasks
from crud_backend.schemas.schemas import Message

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root() -> Message:
    return Message(message="Hello World!")


app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(
    projects.router, prefix="/clients/{client_id}/projects", tags=["projects"]
)
app.include_router(tasks.router, prefix="/projects/{project_id}/tasks", tags=["tasks"])
