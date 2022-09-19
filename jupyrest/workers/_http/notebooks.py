from fastapi import APIRouter, Depends

router = APIRouter()

from typing import Protocol, Optional, Dict
from pydantic import BaseModel, Json
from nbformat import NotebookNode

class NotebookConfig(BaseModel):
    input: Optional[Dict]
    output: Optional[Dict]

class NotebookResource(Protocol):

    def get_notebook(self) -> NotebookNode:
        ...

    def get_config(self) -> NotebookConfig:
        ...

class NotebookNotFound(Exception):
    pass

class NotebookReader(Protocol):

    async def get(self, id: str) -> NotebookResource:
        ...

def notebook_reader() -> NotebookReader:
    raise NotImplemented

@router.get("/{id}")
async def get_notebook(id: str):
    reader = notebook_reader()
    await reader.get(id)